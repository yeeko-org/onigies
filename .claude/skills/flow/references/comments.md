# Comments and the timeline

Read when touching `FlowEvent`, the `events/` endpoints, `FlowComments`, `FlowTimeline`, `FlowCommentIcon`, or the reviewer's private note per bp criterion.

## Model

`FlowEvent` (`api/flow/models.py`): with `to_status` it is a status change, with an optional `comment`; with `to_status=None` it is a **pure comment**. `user` is a pk the frontend resolves against `mainStore.users_by_id`. There is no `edited_at`: a comment can only be edited within the round it was written in (below), before the counterpart gets the turn to read it, so edits leave no trace.

The timeline travels embedded in the record (`flow_events`, chronological order is resolved client-side) and each POST returns the event created; `GET events/` exists but no component uses it.

## Who may write

One check for the three writes — post, edit, delete — `user_holds_root_turn(user, obj)` ([permissions.md](permissions.md)): the root is on the user's side. A child in a reviewer-role status is not commented by the reviewer while the IES has not sent the package or the axis, and vice versa.

Edit and delete also require:

- the event on the requester's **side** (`get_user_flow_role(event.user)` equals the requester's), never its author: any reviewer fixes any reviewer comment, any user of the institution any IES comment;
- the event in the **current round**: created after the root last entered the requester's side, `round_started_at(root, role)` (`api/flow/permissions.py`) — the latest event on the root whose `to_status` has that role and whose `from_status` did not. Moves within one side (`cp_filling` propagated onto the axis, `cp_sent` → `cp_in_review`) do not open a round; a root that never changed side is in its first round, where everything on the side counts. What earlier rounds left is frozen once the counterpart has had it: 403 «Ese comentario es de una ronda anterior; ya no se puede modificar.».

Endpoints (`/flow/{app}/{model}/{pk}/…`):

- `POST events/` `{ comment }` (min 1 char) → 201 with the event; 403 outside the root turn.
- `PATCH events/<event_pk>/` `{ comment }` → 200 with the event; 403 on an admin change's reason unless `is_admin`.
- `DELETE events/<event_pk>/` → **204 and the row is gone** for a pure comment; **200 with the blanked event** for a transition's comment — the status change stays in the log. 404 when the event carries no comment.

The reason of an admin change ([admin-override.md](admin-override.md)) is a transition comment: only an `is_admin` account edits it, and its `DELETE` is a 403 for everyone (`flow.services.is_admin_event`) and the frontend hides the trash, so the timeline mark survives (deleting it would turn the event into an unlabeled off-graph write).

## The criterion note (bp)

`FeatureGoodPractice.comments` — the reviewer's private note per criterion — is not a `FlowEvent` but follows the same lock, in `FeatureGoodPracticeSerializer.validate`: a changed value from a reviewer outside the root's turn is a 403; an unchanged value does not count as a write (the reviewer resends the whole card when rating). An IES never writes it: the field is hidden from it (`hide_review_fields`) and its form resends it blank, so it is dropped silently instead of wiping the note.

## Frontend

`flowStore.eventSide(ev)`: `flowRoleOf` of the author in `users_by_id`; `'reviewer'` when the author is missing from the catalog (the IES only receives its own people plus the reviewers; anyone else is staff). `flowStore.canEditComment(ev, root)`: the event carries text, the root is in the viewer's turn, its side is the viewer's, it is not an admin reason unless `auth.is_admin`, and it is later than the round start computed from `root.flow_events` (`roundStartedAt`, the mirror of `round_started_at`). A root passed without `flow_events` falls back to turn and side, and the server's 403 catches an old comment.

- `FlowComments` (`v-model` = record; props `appLabel`, `modelName`, `width`, `readonly`, `root`): yellow sticky-note card only when `commentCount > 0` (status changes without text do not count), else a «Comentar» button when the user may comment; either opens a dialog with `FlowTimeline` plus the add box. `canComment` = `flowStore.rootRole(root ?? record) === auth.flow_role`, matching the POST guard, not the record's own role. `readonly` hides the capture even on the user's turn (a cp group under consultation, or with the gate closed). It calls `useFlow().addComment / editComment / deleteComment` and mutates `flow_events` in place: a 204 drops the event, a 200 replaces it. Every child surface passes `:root` (`GeneralGroupPanel`, `CpGroupCard`, `GoodPracticeEditSimple`, and the IES dialog through `GoodPracticeEditDialog :root`).
- `FlowTimeline` (`:events`, `:can-edit` (ev → boolean), `busy`): presentational, no fetch, oldest first. With `can-edit` it shows pencil and trash, edits inline, confirms the delete inline (no dialog over the dialog) and emits `edit(ev, text)` / `delete(ev)`; the parent confirms success by changing `events`. Draws an admin change with a `grey-darken-3` dot, the `admin_panel_settings` icon, an outlined «Cambio administrativo» chip, origin → destination chips and the comment prefixed «Motivo:»; same view for both audiences. Reused by `FlowComments`, `FlowTransitionDialogs`, `FlowAdminOverride` and `FlowCommentIcon`.
- `FlowCommentIcon` (`:events`): read-only badge for lists — count of events with text, tooltip renders `FlowTimeline` with those events; no writes.
