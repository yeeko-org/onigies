# The admin override («válvula de admin»)

Read when touching `admin-transitions/`, `FlowAdminOverride`, `useFlowAdminOverride`, or the «Cambio administrativo» mark in the timeline.

## What it is

The only exit from a terminal status, and the only off-graph move a person can make. It moves a **child or grandchild, never a root**, while the **root has role `reviewer`**, to any status of the group in `admin_target_names(group)`: the destinations of transitions leaving a reviewer-role status, plus the reviewer-role statuses themselves (to undo and hand the turn back to review), **minus the current status and its `next_statuses`**. Derived from the seeded graph — never a status only the IES sets, and no name written in code. The legal targets are excluded because the timeline mark is derived from «off-graph»: a valve change along a legal edge would render as a normal transition (no mark, deletable reason), so those go through the status menu.

Door: `User.is_admin` (`is_superuser or is_staff`), never `is_reviewer`.

## Backend (`api/flow/services.py`, `views.py`)

`validate_admin_transition` skips the origin's role and `next_statuses` (terminal origins included), rejects a no-op and rejects a legal target with 400 («'X' es una transición normal; usa el menú de estatus.»); it keeps `applicable_models`, the children rule, a **required** comment and the model's `validate_flow_transition` hook (its `root_turn_errors` cannot fire: the root is already reviewer). `execute_admin_transition` shares `execute_transition`'s effects through `_apply_transition`: `FlowEvent` with the comment, full save, propagation both ways, `transition_executed`.

`POST admin-transitions/` has the same body and response as `transitions/` (`{ target_status, comment }` → 201 with the event); 403 without `is_admin`, 400 with the motor's error list.

There is **no flag on the event**: the timeline labels «Cambio administrativo» any event whose `to_status` is not in its `from_status.next_statuses` **and** that carries a comment. The comment excludes the off-graph writes of `assign_status_tree` and the propagation cascades, which never carry one. `is_admin_event(event)` (`services.py`) is that predicate server-side, and `DELETE events/<pk>/` refuses it with 403: the reason can be corrected (`PATCH`), never removed, and only by an `is_admin` account — anyone else on the reviewer side gets 403 on the `PATCH` too.

The catalog (`StatusSerializer`) adds a computed `admin_targets` to **every status**: the group's set, identical for all statuses of the group and not filtered by model (one query per group, cached in the serializer context). The client crosses it with `applicable_models` and subtracts the current status and its `next_statuses` (the per-object part); it recomputes the group rule only as a fallback for a catalog older than the field, kept until the API and Netlify are both deployed.

## Frontend

`authStore.is_admin` is the only door; no component reads `is_staff`.

- `useFlowActions` returns `root()` and `afterTransition(ev)` (= `options.onTransitioned`), and `FlowStatusActions` mounts `FlowAdminOverride` whenever `actions.root()` exists — so every child surface that already passes `options.root` gets the valve without changes. The button is **not** an item of `FlowTransitionMenu` on purpose: the menu lists the legal flow and the valve there would read as an equivalent option.
- `FlowAdminOverride` (`v-model` record; props `appLabel`, `modelName`, `root`, `size`; emits `transitioned(ev)`): icon button next to the chip plus its own dialog (radios of the off-graph targets, an info alert instead when there are none, required reason, the record's timeline; the current status shows only as the «Estatus actual» chip). Blocked — `aria-disabled` with the reason in the tooltip, not hidden — unless `flowStore.getAdminRootBlock(root)` is empty, i.e. the root has role `reviewer`; an IES-side root shows `not_sent_message`, a terminal root «El envío ya está cerrado».
- `useFlowAdminOverride(record, app, model, { root, onTransitioned })` is a sibling of `useFlowActions`, not part of it (no entry rules, children rule or blocked dialog, so the normal kernel carries no admin logic). It posts through `useFlow().adminTransition` and mutates the record in place like `runTransition`.
- `flowStore.getAdminTargets(current, app, model)` reads `admin_targets` from the current status in the catalog (falls back to deriving the set from the graph for a catalog older than the field), filters by group and `applicable_models`, drops the current status and its `next_statuses`, and sorts by `priority`.
- `flowStore.isAdminEvent(ev)` is the client side of the timeline derivation above; the drawing lives in `FlowTimeline` ([comments.md](comments.md)).
