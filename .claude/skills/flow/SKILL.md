---
name: flow
description: validation-flow engine (`flow` app) — Status roles,
  transitions, propagation, the IES-vs-reviewer model, and the frontend flow
  components + useFlow composable. Use for status changes, the review workflow,
  comments/timeline, or anything under `api/flow/` or `nuxt/.../dashboard/flow/`.
---

# flow — ONIGIES validation-flow engine

The `flow` app is a generic, data-driven state machine shared by three groups:
**bp** (Buenas Prácticas), **cp** (Cuestionario principal), **gen** (Generales).
It replaces the old `ies.StatusControl` / `status_sending` / `status_register`
(coexisting until the data-verification cleanup, plan §8). Source of truth for
the design: `api/ies/flux_rules/PLAN_flujo_validacion.md`.

## The one rule that governs everything: `role` = whose turn it is

Each `Status` has a nullable `role`. It means **who may execute the outgoing
transitions of that status**:

- `role='ies'` → the institution acts (edits + moves forward).
- `role='reviewer'` → the reviewer (staff) acts.
- `role=None` → terminal; nobody moves it.

**The frontend decides everything from the status's `role`, never by hardcoding
a status name.** `obj.status` is the name string, so resolve the role via the
catalog: `editionAvailable` for an IES = `flowStore.getStatus(obj.status)?.role
=== 'ies'`; a reviewer acts when it `=== 'reviewer'`. Hardcoding names like
`bp_completed` in UI logic is the bug to avoid — the motor owns the rules.

## Status model (`api/flow/models.py`)

PK is `name` (CharField, e.g. `bp_draft`). Key fields:

| field | meaning |
|---|---|
| `role` | whose turn (see above); `None` = terminal |
| `group` | `bp` / `cp` / `gen` |
| `public_name`, `color`, `icon` | display (chip/button) |
| `is_default` | one per group (DB constraint); auto-assigned on create |
| `is_public` | record shows on the public site in this status |
| `requires_comment` | transition INTO it needs a comment |
| `propagates_up` | on assignment, recursively set the parent to it too |
| `propagates_down` | on assignment, recursively set all children (and grandchildren) to it too |
| `auto_on_first_save` | assigned automatically on the object's first save |
| `hint` | next-step guidance shown by `FlowStatusActions` below the chip (≠ `description`, which is the chip tooltip) |
| `entry_rules` | JSON list of rule names (frontend `flowRules` registry) that must pass to move an object INTO this status — a **UX gate**, enforced client-side; the motor does NOT check it |
| `next_statuses` (M2M self) | allowed outgoing transitions |
| `valid_child_statuses` (M2M self) | to move a PARENT here, ALL children must be in one of these |
| `applicable_models` (M2M ContentType) | which models this status applies to |

`next_statuses` and `valid_child_statuses` collapsed the old separate
`StatusTransition`/`ParentChildRule` models: verified that
`transition.role == from_status.role` in 100% of cases.

## Hierarchy (`api/flow/registry.py`, code — not DB)

```
cp:   AxisValue → ObservableResponse → GroupResponse
bp:   GoodPracticePackage → GoodPractice
gen:  GeneralGroupResponse (no hierarchy)
```

`GoodPractice.package` and `GroupResponse.observable_response` are real FKs.
**`AxisValue ↔ ObservableResponse` has NO FK**: the parent is the `AxisValue` of
the same `survey` with `axis = observable.component.axis` (callable in the
registry). `ComponentValue` does **not** participate in the flow. Use
`get_parent(obj)` / `get_children(obj)` / `node_for(model)` from the registry.

## The motor (`api/flow/services.py`)

`validate_transition(user, obj, target, comment)` checks, in order:
`target ∈ current.next_statuses` → `target` applies to the model →
`user` role matches `current.role` → children rule (`_check_children_rule`:
all children in `target.valid_child_statuses`) → `requires_comment`.

`execute_transition` validates, writes a `FlowEvent`, updates `obj.status`, then
propagates: `_propagate_up` when `target.propagates_up`, `_propagate_down` when
`target.propagates_down`. Propagation is automatic (no role/comment check) and
only touches objects where the status applies (`applicable_models`) and that
don't already have it. `_propagate_down` walks `get_children` recursively (the bp
hierarchy is 2 levels; no cp/gen status uses `down`). **There is no bypass that
skips validation** — every status change of a parent goes through
`execute_transition`, so `valid_child_statuses` is always enforced before
propagation runs. `get_available_transitions` filters by role + `next_statuses` +
`applicable_models` (NOT the children rule — that is POST-only). Those three
inputs are all in the catalog + auth, so **the frontend computes available
transitions client-side** (`useFlowStore`); there is no `GET transitions/`
endpoint.

## Status is normalized: a `name` string + a client catalog

Model serializers expose `status` as the **name string** (`"bp_draft"`), not a
nested object — `PrimaryKeyRelatedField(read_only=True)`. Same for
`FlowEvent.from_status`/`to_status`. There is **no `StatusBriefSerializer`**.

The **timeline travels embedded**: each participating model has a
`GenericRelation('flow.FlowEvent')` named `flow_events` (already on the bp
models in `api/example/models.py`), and the **Full/detail serializers** nest it
(`flow_events = FlowEventSerializer(many=True, read_only=True)`, prefetched in
the viewset to avoid N+1). So the frontend never fetches the history separately
— it reads `obj.flow_events` and appends the event each POST returns. The `GET
events/` endpoint still exists but the bp components no longer call it.

Display and static rules (`color, icon, public_name, hint, role, entry_rules,
next_statuses, applicable_models, requires_comment`) are resolved from a
client-side catalog,
loaded **once** by `middleware/dashboard.js` into the `useFlowStore`
(`app/store/flow.js`) from `GET /flow/statuses/`. Never re-denormalize the
status onto each row.

- `flowStore.getStatus(name)` → the catalog status object (or `null`).
- `flowStore.getAvailableTransitions(currentName, appLabel, modelName)` → mirrors
  the motor's role + `next_statuses` ∩ `applicable_models` filter.
- `auth.flow_role` → `'reviewer'` if `is_superuser || is_staff || reviewer`, else
  `'ies'` (mirrors backend `User.is_reviewer`; the payload's `is_reviewer` field
  is only the `reviewer` flag, so it is not used).

## Frontend components (`nuxt/app/components/dashboard/flow/`)

All write plumbing goes through one composable, **`useFlow(appLabel, modelName,
pk)`** (`app/composables/useFlow.js`): it builds the base URL
`/flow/{app}/{model}/{pk}/` and returns `sending`, `addComment(text)` and
`transition(name, comment)`, each wrapping `notifyApiError` and returning the
created `FlowEvent`. It does **not** fetch the history (that is embedded). The
three ids may be values, refs or getters (`toValue`). `GoodPracticeList.send`
uses it for the package send too.

**`FlowStatusActions` and `FlowComments` take the whole record via `defineModel`
(`v-model="full_main"` / `v-model="pkg"`), not a pile of derived props.** They
read `status`/`flow_events`/`id` off the record and, on transition/comment,
**mutate it in place** (`record.status = ev.to_status`,
`record.flow_events.push(ev)`). The parent has no `@transitioned`/`@commented`
handlers — the shared object reference carries the update back.

| component | use |
|---|---|
| `FlowStatusChip.vue` | display-only chip; prop `:status` is the **name string**, resolved via `flowStore.getStatus`. Props: `label` (optional prefix), `onlyIcon`/`xSmall` (compact), `disabled`; tooltip with `public_name` + `description`. Trailing `<slot/>` for appended content (the caret in `FlowStatusActions`). |
| `FlowStatusActions.vue` | **unified status control (renamed from `FlowStatusControl`)** — replaced the old `FlowStatusChip` + `FlowTransitions` pair. `v-model` is the record; props `appLabel/modelName`. Reuses `FlowStatusChip`: on the user's turn with transitions, the chip is a `v-menu` activator; else a plain chip. Shows the status **`hint`** below. Before transitioning it runs the target's `entry_rules` (`flowRules`) against the record; if they fail it opens `FlowBlockedDialog` instead. `requires_comment` → dialog embeds `FlowTimeline` (from the record's `flow_events`). |
| `FlowTimeline.vue` | **presentational** read-only history (status changes + comments), chronological; prop `:events` (no fetch). Reused by `FlowComments` and the `FlowStatusActions` comment dialog. |
| `FlowComments.vue` | compact yellow "sticky note" card with the comment count; opens a dialog with `FlowTimeline` + an add-comment box. `v-model` is the record; props `appLabel/modelName`, `width`. Reads/pushes `record.flow_events` directly. |
| `FlowBlockedDialog.vue` | generic "transition blocked" dialog (replaced bp's `NotReadyDialog`). Presentational: `v-model` (open), `title`, `reasons: string[]`. The caller builds `reasons` from the failed `entry_rules`. |

Rule registry: **`app/composables/flowRules.js`** maps a rule name → a function
returning the missing items; `runEntryRules(entryRules, obj)` → `{ ok, missing }`.
`practice_complete` reuses `good_practice_validation.js`.

Endpoints (`api/flow/urls.py`, base `/flow/{app_label}/{model_name}/{pk}/`):

- `POST transitions/` → `{ target_status, comment }` executes one (validation +
  children rule enforced here).
- `GET events/` → timeline (`FlowEventSerializer`); still exists, but the bp
  components read `flow_events` embedded instead of calling it.
- `POST events/` → `{ comment }` adds a pure comment.
- `GET /flow/statuses/?group=bp` → read-only catalog (`StatusSerializer`).

After a transition the components mutate the record (`status` + `flow_events`)
directly; no extra fetch and no `loadEvents`.

## IES vs reviewer: keep them separate

Two audiences, two surfaces:

- **IES** → `/respuestas/[period]` pages. The IES answers content and runs its
  own transitions (e.g. mark a practice complete, send the package). Only here
  live IES-only questions like `has_good_practices`.
- **Reviewer** → `/dashboard` collections. The reviewer scores/validates and runs
  reviewer transitions. **Never** show IES-only questions to the reviewer.

`has_good_practices` is **orthogonal to the flow** — it is a boolean on the
package, not a status. The two `GoodPracticePackageViewSet` actions (in
`api/api/views/example/__init__.py`) combine the boolean with a validated motor
transition:

- `discard/` ("No"): runs `execute_transition(..., bp_discarded)` — validated, so
  `valid_child_statuses` must allow it — then sets `has_good_practices=False`.
  `bp_discarded.propagates_down` cascades the discard to the practices. (For this
  to work the seed must list `bp_discarded` in `next_statuses["bp_draft"]`.)
- `reopen/` ("Cambiar respuesta", from both Sí and No): if the package is in
  `bp_discarded`, runs `execute_transition(..., bp_draft)` (validated) which
  propagates `bp_draft` down to the practices; if it is already in `bp_draft`
  (answer was "Sí") there is no status to revert, so it only clears
  `has_good_practices=None`. Both paths require the package to be in the IES's
  turn (`status.role == 'ies'`) and the period still open.

Both actions return 400 with the motor's error list when the transition is
invalid. The frontend (`GoodPracticeList.vue`) shows "Respuesta registrada" + a
"Cambiar respuesta" button (→ `reopen`) whenever `has_good_practices != null`,
gated by `canEditResponse` (`!isStaff && periodOpen && packageStatus.role ===
'ies'`).

`sent_at` is set automatically by `GoodPracticePackage.save()` when the status
becomes `bp_sent`/`bp_resent` — don't set it from the client.

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

Child rules (`valid_child_statuses`): `bp_sent ← bp_completed`;
`bp_resent ← bp_adjusted, bp_completed`; `bp_finished ← bp_for_ruling, bp_rejected`.
So the IES sending the package (`bp_draft → bp_sent`) is blocked by the motor
until every practice is `bp_completed`. Content completeness is a separate UX
gate: `bp_completed.entry_rules = ['practice_complete']` makes
`FlowStatusActions` block marking a practice complete until
`good_practice_validation.js` passes — fixing the old bug where an incomplete
practice could reach `bp_completed`. The hard children rule stays server-side.

The full bp/cp/gen tables and transitions live in the plan §3
(`api/ies/flux_rules/PLAN_flujo_validacion.md`).

## Coexistence (until cleanup §8)

The old `status_sending`/`status_register` FK fields and `ies.StatusControl`
still exist alongside the new `status` FK. Seed: `flow/seed.py` /
`management/commands/seed_flow.py`. Data migration + verification:
`migrate_flow_data` / `verify_flow_data`. Do not delete the old fields until the
production checkpoint passes.

> The dashboard's `{Model}Edit/EditSimple/Sheet` auto-load convention (how a
> collection picks its detail component) is **out of scope here** — it gets its
> own skill in a later session.
