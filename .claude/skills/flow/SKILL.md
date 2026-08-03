---
name: flow
description: validation-flow engine (`flow` app) — Status roles, transitions,
  propagation, content-edit permissions, the IES-vs-reviewer model, and the
  frontend flow components (`useFlow`/`useFlowActions`, FlowStatusActions). Use
  for status changes, the review workflow, comments/timeline, who-can-edit, or
  anything under `api/flow/` or `nuxt/.../dashboard/flow/`.
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
| `requires_comment` | transition INTO it needs a comment |
| `propagates_up` | on assignment, recursively set the parent to it too |
| `propagates_down` | on assignment, recursively set all descendants to it too |
| `auto_on_first_save` | assigned automatically on the object's first save |
| `hint` | next-step guidance shown by `FlowStatusActions` below the chip (≠ `description`, the chip tooltip) |
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

**Every parent-child edge is a real FK**: `GoodPractice.package`,
`ObservableResponse.axis_value`, `GroupResponse.observable_response`,
`GeneralGroupResponse.general_package`. The roots (`GoodPracticePackage`,
`AxisValue`, `GeneralPackage`) are created eager in `Institution.save`.

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
`target.valid_child_statuses`) → `requires_comment`.

`execute_transition` validates, writes a `FlowEvent`, updates `obj.status`, then
propagates: `_propagate_up` when `target.propagates_up`, `_propagate_down` when
`target.propagates_down`. Propagation is automatic (no role/comment check) and
only touches objects where the status applies (`applicable_models`) and that
don't already have it. **Every parent status change goes through
`execute_transition`** — there is no bypass — so `valid_child_statuses` is always
enforced before propagation.

`get_available_transitions` filters by role + `next_statuses` +
`applicable_models` (NOT the children rule — that is POST-only). All three inputs
are in the catalog + auth, so the **frontend computes available transitions
client-side**; there is no `GET transitions/` endpoint.

`assign_auto_status(user, obj)` assigns the group's `auto_on_first_save` status
when the object has none (called from the view on first save).

## Status normalization + client catalog

Model serializers expose `status` as the **name string**
(`PrimaryKeyRelatedField(read_only=True)`), not a nested object — same for
`FlowEvent.from_status`/`to_status`. There is no `StatusBriefSerializer`.

The **timeline travels embedded**: each participating model has a
`GenericRelation('flow.FlowEvent')` named `flow_events`; the Full/detail
serializers nest it (`FlowEventSerializer(many=True, read_only=True)`,
prefetched in the viewset). The frontend reads `obj.flow_events` and appends the
event each POST returns — it never fetches the history separately.

The catalog (`color, icon, public_name, action_name, hint, role, content_editable,
entry_rules, next_statuses, applicable_models, requires_comment`) loads **once**
via `middleware/dashboard.js` into `useFlowStore` (`app/store/flow.js`) from
`GET /flow/statuses/`. Never re-denormalize the status onto each row.

- `flowStore.getStatus(name)` → the catalog status object (or `null`).
- `flowStore.canEditContent(obj, root)` → the content-edit permission (above).
- `flowStore.getAvailableTransitions(currentName, appLabel, modelName)` → mirrors
  the motor's role + `next_statuses` ∩ `applicable_models` filter.
- `auth.flow_role` → `'reviewer'` if `is_superuser || is_staff || reviewer`, else
  `'ies'` (mirrors backend `User.is_reviewer`).

## Frontend (`nuxt/app/components/dashboard/flow/`)

**Write plumbing → `useFlow(appLabel, modelName, pk)`**
(`app/composables/useFlow.js`): builds `/flow/{app}/{model}/{pk}/` and returns
`sending`, `addComment(text)`, `transition(name, comment)` — each wraps
`notifyApiError` and returns the created `FlowEvent`. The three ids may be
values, refs or getters (`toValue`). It does not fetch history.

**Transition orchestration → `useFlowActions(record, appLabel, modelName)`**
(`app/composables/useFlowActions.js`): the headless kernel holding available
`transitions`, the `entry_rules` gate → `FlowBlockedDialog`, the
`requires_comment` → comment dialog, and `runTransition` with in-place mutation
+ snackbar. Consumers only provide the **activator**. Key bits: `onSelect(t)`
returns the `FlowEvent` on a real transition, `null` if it opened a dialog or
failed (the caller closes its own dialog only when an event came back);
`block(title, reasons)` opens the blocked dialog manually. It wraps `useFlow`.

**Record-as-model.** `FlowStatusActions` and `FlowComments` take the whole record
via `defineModel` (not derived props); on transition/comment they **mutate it in
place** (`record.status = ev.to_status`, `record.flow_events.push(ev)`). The
shared object reference carries the update back — no `@transitioned`/`@commented`
handlers.

| component | use |
|---|---|
| `FlowStatusChip.vue` | display-only chip; `:status` is the **name string**, resolved via `flowStore.getStatus`. Props `label`, `onlyIcon`/`xSmall`, `disabled`; tooltip = `public_name` + `description`. Trailing `<slot/>` for appended content. |
| `FlowStatusActions.vue` | **unified status control** — thin assembly over `useFlowActions`: chip activator (`v-menu`) + `FlowTransitionMenu` + `FlowTransitionDialogs`. `v-model` = record; props `appLabel/modelName`. On the user's turn with transitions the chip is a menu activator, else plain. Shows the status `hint` below. |
| `FlowTransitionMenu.vue` | **presentational** `v-list` of transitions; `:transitions`, emits `@select(t)`; `:title` uses `action_name || public_name`. Reused by chip-menu and split-button carets. |
| `FlowTransitionDialogs.vue` | **presentational** comment dialog (embeds `FlowTimeline`) + `FlowBlockedDialog`, bound via `:actions="useFlowActions(...)"`. |
| `FlowTimeline.vue` | **presentational** read-only history (status changes + comments), chronological; `:events` (no fetch). Reused by `FlowComments` and `FlowTransitionDialogs`. |
| `FlowComments.vue` | compact yellow "sticky note" with comment count; opens a dialog with `FlowTimeline` + add-comment box. `v-model` = record; props `appLabel/modelName`, `width`. |
| `FlowBlockedDialog.vue` | generic "transition blocked" dialog. Presentational: `v-model` (open), `title`, `reasons: string[]` (built from failed `entry_rules`). |

**Split-buttons (alternative activator).** Where a prominent action beats the
chip-menu, a `v-btn-group` (primary button + caret) drives the same transitions
and the chip degrades to display-only (`FlowStatusChip`); no caret when
`transitions.length === 0`:

- `GoodPracticeEditSimple` (IES): "Guardar" (`saveSimple`) + caret items that
  **save then transition** — `saveAndTransition(t)` = `await persist();
  onSelect(t)`, closing only if `onSelect` returned an event. `persist` is split
  from the close so the save doesn't dismiss the dialog before the transition.
- `GoodPracticeList` (IES): "Enviar a revisión" evaluates `bp_sent`'s
  `entry_rules` (`package_ready`) via `runEntryRules`; on failure opens
  `FlowBlockedDialog`, else the confirm dialog, then `packageTransition('bp_sent')`
  + `loadPractices()`. (Uses `runEntryRules` directly, not the full kernel, to
  keep its own snackbar and avoid a double mutation since it reloads.)

**Rule registry `app/composables/flowRules.js`** maps a rule name → a function
returning the missing items; `runEntryRules(entryRules, obj)` → `{ ok, missing }`.
`practice_complete` reuses `good_practice_validation.js`. `package_ready` (on
`bp_sent`) lists the practices still in the IES's turn (touches the store per
child).

## Endpoints (`api/flow/urls.py`, base `/flow/{app_label}/{model_name}/{pk}/`)

- `POST transitions/` → `{ target_status, comment }` executes one (validation +
  children rule enforced here).
- `GET events/` → timeline (`FlowEventSerializer`); the components read embedded
  `flow_events` instead.
- `POST events/` → `{ comment }` adds a pure comment.
- `GET /flow/statuses/?group=bp` → read-only catalog (`StatusSerializer`).

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
So sending the package (`bp_draft → bp_sent`) is blocked by the motor until every
practice is `bp_completed`. The UX mirrors this client-side:
`bp_completed.entry_rules = ['practice_complete']` blocks marking a practice
complete until `good_practice_validation.js` passes;
`bp_sent.entry_rules = ['package_ready']` gates the send. The hard children rules
stay server-side.

Full bp/cp/gen tables and transitions: plan §3
(`docs/records/2026-06-05-diseno-del-motor-de-flujo.md`).

## Coexistence

The old `status_sending`/`status_register` FK fields and `ies.StatusControl`
still exist alongside the new `status` FK during data verification (plan §8) —
do not delete them yet. Seed: `flow/seed.py` / `seed_flow` command.