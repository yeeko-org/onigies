---
name: flow
description: validation-flow engine (`flow` app) — Status roles, transitions,
  propagation, content-edit permissions, the IES-vs-reviewer model, and the
  frontend flow components (`useFlow`/`useFlowActions`, FlowStatusActions). Use
  for status changes, the review workflow, comments/timeline, who-can-edit, or
  anything under `api/flow/` or `nuxt/app/components/dashboard/flow/`.
---

# flow — ONIGIES validation-flow engine

The `flow` app is a generic, data-driven state machine shared by three groups:
**bp** (Buenas Prácticas), **cp** (Cuestionario principal), **gen** (Generales).
Design source of truth: `docs/records/2026-06-05-diseno-del-motor-de-flujo.md`.

## The one rule: `role` = whose turn it is

Each `Status` has a nullable `role` = **who may execute the outgoing
transitions of that status**:

- `role='ies'` → the institution acts.
- `role='reviewer'` → the reviewer (staff) acts.
- `role=None` → terminal; nobody moves it.

`obj.status` is the **name string** (`"bp_draft"`), so the frontend resolves
the role via the catalog (`flowStore.getStatus(obj.status)?.role`) and decides
everything from it. **Never hardcode a status name in UI logic** — the motor
owns the rules.

### Two permissions: transition vs. content-edit

`role` answers "whose turn to *transition*". Editing the *content* is a
separate, stricter question answered by the **root** ancestor plus a per-status
flag. The frontend helper (`app/store/flow.js`):

```js
canEditContent(obj, root = obj) =
  ownStatus(obj).content_editable && rootStatus(root).role === auth.flow_role
```

`root` defaults to `obj` (for roots like the package); for children/grandchildren
the caller passes the root explicitly (it already holds the nested tree). The
**root governs** descendants: once the package/axis is sent (`root.role` flips to
`reviewer`), the IES can't edit any descendant — even one still in an IES-turn
status. `content_editable` separates "my turn to edit" (`bp_completed`,
`bp_adjusted` — editable bookmarks before send) from "my turn to only
transition" (`bp_discarded`, terminal/review states).

The server mirror is `user_can_edit_flow_content` (`api/flow/permissions.py`), which adds a third condition the client helper does not know: the root's optional `content_lock_errors(user)` hook (duck typing, like `validate_flow_transition`). `AxisValue` uses it to close all cp content — typed answers, the initial boolean, attachments — while the answer gate is closed (see cp below); the frontend gets that state as `cp_capture` in the axis payload instead.

The same "root governs" idea applies to **reviewer transitions** in gen, bp and cp: a child reaches a reviewer-role status (`gen_completed`, `bp_completed`, `cp_completed`…) before the IES sends the root, and the motor only checks the object's own role. `flow.permissions.root_turn_errors` (called from the children's `validate_flow_transition` hooks: `GeneralGroupResponse`, `GoodPractice`, `ObservableResponse`, `GroupResponse`) rejects reviewer transitions while the root is still in the IES's turn, with the message the root names in its `root_not_sent_message` (exposed to the frontend as `not_sent_message` in the root serializers); `flowStore.getRootNotInTurn(root)` is its client mirror, applied by `useFlowActions` when given `options.root`.

## Status model (`api/flow/models.py`)

PK is `name` (CharField, e.g. `bp_draft`). Key fields:

| field | meaning |
|---|---|
| `role` | whose turn; `None` = terminal |
| `group` | `bp` / `cp` / `gen` |
| `public_name` | the **state** the chip shows ("Enviado a revisión") |
| `action_name` | the **verb** of the button/menu that transitions INTO it ("Enviar a revisión"), shown by `FlowTransitionMenu`; `None` when never a manual target |
| `content_editable` | turn-holder may edit content here (vs. only transition) |
| `color`, `icon` | display (chip/button) |
| `is_default` | one per group (DB constraint); auto-assigned on create |
| `is_public` | record shows on the public site in this status |
| `comment_type` | `none` / `optional` / `required` — whether the transition INTO it asks for a comment; only `required` is enforced by the motor |
| `comment_prompt` | label of the comment box in that dialog; empty → generic text |
| `propagates_up` | on assignment, recursively set the parent to it too |
| `propagates_down` | on assignment, recursively set all descendants to it too |
| `auto_on_first_save` | assigned automatically on the object's first save |
| `hint` | next-step guidance shown by `FlowStatusActions` to the role whose turn it is — below the chip (`hint="box"`) or inside the chip tooltip (`hint="tooltip"`) (≠ `description`, the chip tooltip's base text) |
| `hint_wait` | variant of `hint` for the role that is *waiting*; empty falls back to `hint`. Unused on terminals |
| `priority` | urgency for ordering (higher = first); used to sort status summaries, e.g. `SurveyHeader`'s group counts |
| `requires_confirmation` + `confirm_title` / `confirm_text` | the frontend asks for an explicit confirmation before transitioning INTO it; empty title → derived from `action_name` |
| `entry_rules` | JSON list of `flowRules` names that must pass to move INTO this status — a **UX gate**, enforced client-side only; the motor does NOT check it |
| `next_statuses` (M2M self) | allowed outgoing transitions |
| `valid_child_statuses` (M2M self) | to move a PARENT here, ALL children must be in one of these |
| `applicable_models` (M2M ContentType) | which models this status applies to |

## Hierarchy & registry (`api/flow/registry.py`)

```
bp:   GoodPracticePackage → GoodPractice
cp:   AxisValue → ObservableResponse → GroupResponse
gen:  GeneralPackage → GeneralGroupResponse
```

**Every parent-child edge is a real FK**: `GoodPractice.package`, `ObservableResponse.axis_value`, `GroupResponse.observable_response`, `GeneralGroupResponse.general_package`. The roots (`GoodPracticePackage`, `AxisValue`, `GeneralPackage`) are created eager in `Institution.save`, and so are the whole cp tree below each axis: `ObservableResponse` and `GroupResponse` (`answer.models.provision_cp_responses`, idempotent, born in `cp_pre_start` — set there because `bulk_create` skips the flow signal — except the groups without capture, born in `cp_approved`). Only the typed answers are lazy.

Topology lives **on each model, not a central dict**: a participating model
inherits the `FlowParticipant` mixin (a marker, no fields → no migration) and
declares `flow_parent = '<fk field>'` (roots leave the default `None`). The
children side is **not** declared — `get_children` derives the reverse accessor
from the child's `flow_parent` FK, so each edge is written once.
`ComponentValue` does **not** participate.

Helpers: `get_parent(obj)`, `get_children(obj)`, `is_flow_participant(model)`.

## The motor (`api/flow/services.py`)

`validate_transition(user, obj, target, comment)` checks, in order:
`target ∈ current.next_statuses` → `target` applies to the model → `user` role
matches `current.role` → children rule (`_check_children_rule`: all children in
`target.valid_child_statuses`) → `comment_type == 'required'` → the model's own hook, if it
defines one: `obj.validate_flow_transition(user, target)` returns a list of
errors (duck typing, so the motor stays generic — e.g. the bp/gen packages veto
the send when the period is closed).

`execute_transition` validates, writes a `FlowEvent`, updates `obj.status`, then propagates: `_propagate_up` when `target.propagates_up`, `_propagate_down` when `target.propagates_down`. Propagation is automatic (no role/comment check) and only touches objects where the status applies (`applicable_models`) and that don't already have it. **Every manual status change goes through `execute_transition`**, so `valid_child_statuses` is always enforced before propagation; the only doors that skip it are the two domain services below (`assign_auto_status`, `assign_status_tree`), which no menu reaches.

Every status write — the object's own and the propagated ones — goes through
`_save_status(obj)`, a **full `obj.save()`** on purpose: with
`update_fields=['status']` anything the model's `save()` derives from the status
was silently dropped (that is how `sent_at` never persisted). Hooks in `save()`
therefore just work, with nothing to register in `flow`. Safe because the row was
re-read under `select_for_update()` inside the transaction.

`get_available_transitions` filters by role + `next_statuses` +
`applicable_models` (NOT the children rule — that is POST-only). All three inputs
are in the catalog + auth, so the **frontend computes available transitions
client-side**; there is no `GET transitions/` endpoint.

`assign_auto_status(user, obj)` assigns the group's `auto_on_first_save` status when the object has none or sits in the group default (called from the view on first save; it propagates up when the status does).

`assign_status_tree(user, obj, status)` is the **domain door, not a menu transition**: it forces `status` on `obj` and every descendant, skipping role, `next_statuses` and the children rule, one `FlowEvent` per object changed, no upward propagation, no `transition_executed` signal. Only `answer.services` uses it, when the initial answer of an observable decides its groups' fate (`cp_not_present` and back to `cp_filling`, or to `cp_approved` for the groups without capture).

## Status normalization + client catalog

Model serializers expose `status` as the **name string**
(`PrimaryKeyRelatedField(read_only=True)`), not a nested object — same for
`FlowEvent.from_status`/`to_status`. There is no `StatusBriefSerializer`.

The **timeline travels embedded**: each participating model has a
`GenericRelation('flow.FlowEvent')` named `flow_events`; the Full/detail
serializers nest it (`FlowEventSerializer(many=True, read_only=True)`,
prefetched in the viewset). The frontend reads `obj.flow_events` and appends the
event each POST returns — it never fetches the history separately.

The catalog is the **whole Status row** (`StatusSerializer`, `fields = '__all__'`:
display, `hint`/`hint_wait`, `priority`, `comment_type`/`comment_prompt`, the
confirmation texts, `entry_rules`, `next_statuses`, `valid_child_statuses`,
`applicable_models`) and loads **once** via `middleware/dashboard.js` into `useFlowStore` (`app/store/flow.js`) from
`GET /flow/statuses/`. Never re-denormalize the status onto each row.

- `flowStore.getStatus(name)` → the catalog status object (or `null`).
- `flowStore.canEditContent(obj, root)` → the content-edit permission (above).
- `flowStore.getAvailableTransitions(currentName, appLabel, modelName)` → mirrors
  the motor's role + `next_statuses` ∩ `applicable_models` filter.
- `flowStore.getChildrenNotReady(record, target, modelName)` → the children rule read client-side (`CHILD_REGISTRY` says where the children hang — for cp, `observable_responses` on the axis and `group_responses` on the observable, the field names of the Full serializers), as reasons in Spanish for the blocked dialog. UX only; the motor still enforces it on POST.
- `flowStore.getRootNotInTurn(root)` → mirror of `root_turn_errors` (above).
- `auth.flow_role` → `'reviewer'` if `is_superuser || is_staff || reviewer`, else
  `'ies'` (mirrors backend `User.is_reviewer`).

## Frontend (`nuxt/app/components/dashboard/flow/`)

**Write plumbing → `useFlow(appLabel, modelName, pk)`**
(`app/composables/useFlow.js`): builds `/flow/{app}/{model}/{pk}/` and returns
`sending`, `addComment(text)`, `transition(name, comment)` — each wraps
`notifyApiError` and returns the created `FlowEvent`. The three ids may be
values, refs or getters (`toValue`). It does not fetch history.

**Transition orchestration → `useFlowActions(record, appLabel, modelName, options)`**
(`app/composables/useFlowActions.js`): the headless kernel holding available
`transitions`, the `entry_rules` + children gate → `FlowBlockedDialog`, the
confirmation/comment dialog (`requires_confirmation || comment_type !== 'none'`,
one dialog for both), and `runTransition` with in-place mutation + snackbar.
Consumers only provide the **activator**. Key bits: `onSelect(t)` returns the
`FlowEvent` on a real transition, `null` if it opened a dialog or failed (the
caller closes its own dialog only when an event came back); `block(title,
reasons)` opens the blocked dialog manually; each entry of `transitions` carries
`blocked` (the reasons, when any) so the menu can pre-disable it — `onSelect`
re-checks anyway, since the record may have changed since the render.

`options.onTransitioned(ev)` is awaited after the mutation and the snackbar: for when the mutation in place isn't enough and the consumer must refetch — e.g. `GoodPracticeList` reloads to get `sent_at`, `GeneralGroupList` recomputes which panels stay open. `options.root` (value, ref or getter) is the flow root when `record` is a descendant: its reasons from `getRootNotInTurn` go first in each transition's `blocked` and `onSelect` rechecks them. It wraps `useFlow`.

**Record-as-model.** `FlowStatusActions` and `FlowComments` take the whole record
via `defineModel` (not derived props); on transition/comment they **mutate it in
place** (`record.status = ev.to_status`, `record.flow_events.push(ev)`). The
shared object reference carries the update back — no `@transitioned`/`@commented`
handlers.

| component | use |
|---|---|
| `FlowStatusChip.vue` | display-only chip; `:status` is the **name string**, resolved via `flowStore.getStatus`. Props `label`, `size`, `variant`, `onlyIcon`/`xSmall`, `disabled`; tooltip = `public_name` + `description` + slot `tooltip`. Trailing `<slot/>` for appended content. |
| `FlowStatusActions.vue` | **unified status control** — thin assembly over `useFlowActions`: chip activator (`v-menu`) + `FlowTransitionMenu` + `FlowTransitionDialogs`. `v-model` = record; props `appLabel/modelName`, `size`, `variant`, `hint: 'box' \| 'tooltip'` (default `box`). On the user's turn with transitions the chip is a menu activator, else plain. `box` shows the status `hint` below the chip; `tooltip` puts it in the chip tooltip plus a small `flag` icon when it is the user's turn — cp uses `tooltip` on observable and group (three levels would stack boxes) and `box` on the axis. |
| `FlowTransitionMenu.vue` | **presentational** `v-list` of transitions; `:transitions`, emits `@select(t)`; `:title` uses `action_name || public_name`. Reused by chip-menu and split-button carets. |
| `FlowTransitionDialogs.vue` | **presentational** confirmation/comment dialog (title from `confirm_title`, body `confirm_text`, comment label `comment_prompt`; embeds `FlowTimeline`) + `FlowBlockedDialog`, bound via `:actions="useFlowActions(...)"`. Every activator that isn't `FlowStatusActions` (split-buttons) must mount it itself. |
| `FlowTimeline.vue` | **presentational** read-only history (status changes + comments), chronological; `:events` (no fetch). Reused by `FlowComments` and `FlowTransitionDialogs`. |
| `FlowComments.vue` | yellow "sticky note" card only when `commentCount > 0` (status changes without text don't count), otherwise a «Comentar» button when the user may comment; either opens a dialog with `FlowTimeline` + add-comment box. `v-model` = record; props `appLabel/modelName`, `width`, `readonly` (hides the capture even on the user's turn). |
| `FlowSaveMenu.vue` | **presentational** split-button «Guardar ▾»: lead item «Guardar y mantener como {status}», then `FlowTransitionMenu`; plain «Guardar» when there are no transitions. Props `transitions`, `currentStatus`, `loading`, `disabled`, `saveDisabled`, and optional `saveLabel` (replaces the lead item's text when saving does not keep the status: cp's first save auto-promotes, so `CpGroupCard` drops that transition from the menu and labels the lead «Guardar y pasar a …»); emits `save` and `select(t)`. The parent saves-then-transitions and mounts `FlowTransitionDialogs`. Used by gen (`GeneralGroupPanel`), bp (`GoodPracticeEditSimple`) and cp (`CpGroupCard`). |
| `FlowBlockedDialog.vue` | generic "transition blocked" dialog. Presentational: `v-model` (open), `title`, `reasons: string[]` (failed `entry_rules` + children not ready). |

**Split-buttons (alternative activator).** Where a prominent action beats the
chip-menu, a split-button (`FlowSaveMenu` for save-then-transition) drives the same transitions
and the chip degrades to display-only (`FlowStatusChip`); no caret when
`transitions.length === 0`:

- `GoodPracticeEditSimple` (IES): `FlowSaveMenu` — "Guardar" (`saveSimple`) + items that
  **save then transition** — `saveAndTransition(t)` = `await persist();
  onSelect(t)`, closing only if `onSelect` returned an event. `persist` is split
  from the close so the save doesn't dismiss the dialog before the transition.
- `GoodPracticeList` (IES): "Enviar a revisión" runs through the full kernel — `useFlowActions` on the package (`FlowTransitionDialogs`), with `onTransitioned` reloading the practices. The real gate is the children rule (`getChildrenNotReady`, every practice `bp_completed`), so before `onSelect` it syncs `record.good_practices` with the live list: the children gate reads the embedded array, which goes stale after adds/deletes.

**Rule registry `app/composables/flowRules.js`** maps a rule name → a function returning the missing items; `runEntryRules(entryRules, obj)` → `{ ok, missing }`. The only rules are `practice_complete` (on `bp_completed`, reuses `good_practice_validation.js`) and `features_rated` (on `bp_for_ruling`: every marked feature carries the reviewer's rating).

## Endpoints (`api/flow/urls.py`, base `/flow/{app_label}/{model_name}/{pk}/`)

- `POST transitions/` → `{ target_status, comment }` executes one (validation +
  children rule enforced here).
- `GET events/` → timeline (`FlowEventSerializer`); the components read embedded
  `flow_events` instead.
- `POST events/` → `{ comment }` adds a pure comment.
- `attachments/` (list/upload, detail, `download/`) → files hung on the object; writing them follows the content-edit permission.
- `GET /flow/statuses/?group=bp` → read-only catalog (`StatusSerializer`).

Content is written outside `flow`, per group: bp and gen through their own viewsets; cp through `/axis_value/` (read-only collection, the axis with its whole questionnaire), `/observable_response/` (PATCH of the initial answer) and `/group_response/` (PATCH of one group's typed answers) — skill `cp-questionnaire`. Transitions, comments and attachments of cp objects still go through `/flow/answer/…` and `/flow/survey/axisvalue/…`.

## IES vs reviewer: keep them separate

Two audiences, two surfaces:

- **IES** → `/respuestas/[period]`. Answers content and runs its own transitions
  (mark a practice complete, send the package). IES-only fields like
  `has_good_practices` live only here.
- **Reviewer** → `/dashboard` collections. Scores/validates and runs reviewer
  transitions. **Never** show IES-only fields to the reviewer.

`has_good_practices` is **orthogonal to the flow** (a boolean on the package, not
a status). Two `GoodPracticePackageViewSet` actions
(`api/api/views/example/__init__.py`) combine it with a validated transition:

- `discard/` ("No"): `execute_transition(..., bp_discarded)` (validated), then
  sets `has_good_practices=False`. `bp_discarded.propagates_down` cascades to the
  practices. (Requires `bp_discarded ∈ next_statuses["bp_draft"]` in the seed.)
- `reopen/` ("Cambiar respuesta"): if in `bp_discarded`,
  `execute_transition(..., bp_draft)` (propagates `bp_draft` down); if already in
  `bp_draft` (answer was "Sí") there's nothing to revert, so it only clears
  `has_good_practices=None`. Both paths require the package in the IES's turn
  (`status.role == 'ies'`) and the period open.

Both return 400 with the motor's error list when invalid. `GoodPracticeList.vue`
shows "Respuesta registrada" + a "Cambiar respuesta" button (→ `reopen`) whenever
`has_good_practices != null`, gated by `canEditResponse` (`!isStaff &&
periodOpen && packageStatus.role === 'ies'`).

`sent_at` is set automatically by the package's `save()` (`GoodPracticePackage`,
`GeneralPackage`) when the status becomes `*_sent`/`*_resent` — don't set it from
the client.

## bp catalog (worked example)

P = `GoodPracticePackage`, G = `GoodPractice`.

| status | applies | role | note |
|---|---|---|---|
| `bp_draft` | P, G | ies | default; IES edits freely |
| `bp_completed` | G | reviewer | IES marked it complete; waits for the package send |
| `bp_sent` | P | reviewer | package in review |
| `bp_need_changes` | P, G | ies | reviewer asked for fixes |
| `bp_adjusted` | G | reviewer | fixes applied, awaiting re-review |
| `bp_resent` | P | reviewer | package resent |
| `bp_for_ruling` / `bp_rejected` | G | None | terminal per practice |
| `bp_finished` | P | None | terminal package |

Child rules (`valid_child_statuses`): `bp_sent ← bp_completed`; `bp_resent ← bp_adjusted, bp_completed`; `bp_finished ← bp_for_ruling, bp_rejected`. So sending the package (`bp_draft → bp_sent`) is blocked by the motor until every practice is `bp_completed`. The UX mirrors this client-side: `bp_completed.entry_rules = ['practice_complete']` blocks marking a practice complete until `good_practice_validation.js` passes; the send itself is gated only by the children rule, mirrored client-side by `getChildrenNotReady`. The hard children rules stay server-side.

The source of truth for every group's statuses, transitions and child rules is `api/flow/seed.py`; plan §3 (`docs/records/2026-06-05-diseno-del-motor-de-flujo.md`) keeps the design rationale.

## cp catalog

A = `AxisValue` (the unit of send), O = `ObservableResponse` (the unit of work), G = `GroupResponse` (the unit of save, one per question type). The IES's initial «No» on an observable sets `cp_not_present` — terminal by domain, not by the motor — on the observable and all its groups through `assign_status_tree`; the reviewer returns per group, and `root_turn_errors` keeps every reviewer transition waiting until the axis is sent. Status table, child rules and the guards on the «No»: [references/cp.md](references/cp.md).

## gen: the live surfaces

`gen` runs end to end (`GeneralPackage` → the 5 `GeneralGroupResponse`), and both
audiences share the **same dual-audience component**, which resolves role,
editability and available transitions by itself:

- **IES** → `/respuestas/[period]`, tab «Información base» →
  `components/dashboard/survey/GeneralGroupList.vue` + one `GeneralGroupPanel`
  per group: split-button "Guardar" + caret with the group's transitions, and the
  package send gated by `valid_child_statuses` (all five groups completed) plus
  the period lock (`Period.is_gen_submission_closed`, enforced in
  `GeneralPackage.validate_flow_transition`).
- **Reviewer** → dashboard collection «Cuestionarios de las IES» (`Survey`);
  `SurveyEditSimple` mounts the very same `GeneralGroupList` read-only, with the
  per-group and package transitions. The reviewer transitions and comments but
  **does not edit gen content**. A menu-less collection «Envíos de preguntas
  generales» (`GeneralPackage`) exists for direct access.

Two gen specifics: `gen_approved`/`gen_finished` are terminal in every direction
(no `next_statuses` out of them), and returning a group with `gen_need_changes`
does **not** propagate to the package — the reviewer transitions both. The
section's content is written against `Survey`, not the flow wrappers: skill
`gen-general-info`.

## cp: the live surfaces

One tree of components under `components/dashboard/answer/capture/` serves both audiences, the reviewer through a `review` prop (read-only content; transitions, comments and attachments stay). Save is per group, no autosave, and the axis payload's `cp_capture` drives the answer gate. The components per audience, the publication switch and the offered next steps: [references/cp.md](references/cp.md).

Seed: `flow/seed.py` / `seed_flow` command.