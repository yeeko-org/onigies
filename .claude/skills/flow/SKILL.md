---
name: flow
description: ONIGIES validation-flow engine: status roles, transitions, propagation, who may edit or comment, the comment timeline, the admin override and the frontend flow components. Use for status changes, the review workflow, or the flow app.
metadata:
  rules: 2026-09-05
  type: domain
  reader: both
---

# flow — ONIGIES validation-flow engine

`api/flow/` is a generic, data-driven state machine shared by three groups: **bp** (Buenas Prácticas), **cp** (Cuestionario principal), **gen** (Generales). The catalog — the `Status` rows, their `next_statuses` graph and the parent-child rules — is seeded from `api/flow/seed.py` (`seed_flow` command), the source of truth for every field: re-seeding overwrites admin edits. Design rationale: `docs/records/2026-06-05-diseno-del-motor-de-flujo.md`.

Hierarchies (every edge a real FK, declared on the child as `flow_parent`):

```
bp:   GoodPracticePackage → GoodPractice
cp:   AxisValue → ObservableResponse → GroupResponse
gen:  GeneralPackage → GeneralGroupResponse
```

References, read when the work touches them:

- [statuses-and-graph.md](references/statuses-and-graph.md) — `Status` fields, the registry mixin, how objects are born, the bp catalog as worked example, gen specifics.
- [permissions.md](references/permissions.md) — content-edit vs transition, the root rule, the model hooks, attachments.
- [comments.md](references/comments.md) — timeline model, who edits a comment and until when, the criterion note, `FlowComments`/`FlowTimeline`.
- [admin-override.md](references/admin-override.md) — the admin valve, backend and frontend.
- [frontend.md](references/frontend.md) — composables, components, split-buttons, the rules registry, the bp package actions.
- [cp.md](references/cp.md) — cp statuses, child rules, the initial «No», the capture/review surfaces.

## The one rule: `role` = whose turn it is

Each `Status` has a nullable `role`: who may execute its outgoing transitions. `ies` → the institution acts; `reviewer` → the reviewer acts; `None` → terminal, nobody moves it. `obj.status` travels as the **name string** (`"bp_draft"`); the frontend resolves it through the catalog (`flowStore.getStatus(name)`) and decides everything from `status.role` — **never from a status name**. The motor owns the rules; UI logic that hardcodes `bp_sent` breaks the day the seed changes.

Two user flags, mirrored backend (`User` properties) and frontend (`authStore`), and only these two in components:

- `is_reviewer` = `is_superuser || is_staff || reviewer` → `auth.flow_role` is `'reviewer'`, else `'ies'`. Dual-audience UI reads `auth.is_reviewer` in each component, never `is_staff` (real reviewers carry `reviewer` without `is_staff`) and never through a prop.
- `is_admin` = `is_superuser || is_staff` → the admin override only.

## Two permissions, and the root governs

`role` answers «whose turn to *transition*». Editing *content* is stricter: the object's own status must be `content_editable` **and** the **root** of its hierarchy (package or axis) must be in the user's turn. Once the IES sends the root, no descendant is editable even if its own status is still an IES one. Server: `user_can_edit_flow_content` (`api/flow/permissions.py`); client: `flowStore.canEditContent(obj, root)`.

The root governs the reviewer too: a child reaches a reviewer-role status (`bp_completed`, `gen_completed`, `cp_completed`) before the IES sends the root, and the motor only checks the object's own role. `root_turn_errors`, called from every child's `validate_flow_transition` hook, rejects reviewer transitions while the root is on the IES side; `flowStore.getRootNotInTurn(root)` pre-blocks the menu. Comments — posting, editing, deleting — follow the same root turn (`user_holds_root_turn`), and editing or deleting only reaches the current round ([comments.md](references/comments.md)). Attachments do not follow the turn alone: they follow content edit and are IES-only. Hooks and details: [permissions.md](references/permissions.md).

## The motor (`api/flow/services.py`)

`validate_transition` checks, in order: `target ∈ current.next_statuses` → target applies to the model (`applicable_models`) → user role = `current.role` → children rule (all children in `target.valid_child_statuses`) → required comment → the model's own `validate_flow_transition(user, target)` hook (duck typing: the motor stays generic, each participant vetoes with its own domain). `execute_transition` re-reads the row under `select_for_update`, writes a `FlowEvent`, saves and propagates (`propagates_up` / `propagates_down`: automatic, no role or comment check, only onto objects where the status applies and that don't already hold it), then emits `transition_executed` — `flow/notifications.py` turns it into an email to the IES when a **root** returns to the IES's turn or closes; manual transitions only, never the propagated ones.

Every status write is a **full `obj.save()`** on purpose (`_save_status`): with `update_fields=['status']` whatever the model's `save()` derives from the status was silently dropped — that is how `sent_at` never persisted. Hooks in `save()` just work, nothing to register in `flow`.

Three doors write a status; the menu only reaches the first:

- `execute_transition` — every manual change; the children rule always runs before propagation.
- `execute_admin_transition` — the admin override: same effects, its own validation ([admin-override.md](references/admin-override.md)). Never add its targets to the seed graph: the normal endpoint keeps rejecting off-graph targets for everyone.
- `assign_status_tree` — the domain door: forces a status on an object and all its descendants, skipping role, graph and children rule; only `answer.services` uses it (the initial «No» of an observable). Its sibling `assign_auto_status` promotes from the group default to the `auto_on_first_save` status on the first save.

`entry_rules` is the exception: a UX gate evaluated client-side only (`flowRules.js`); the motor never checks it. The children rule is the reverse: a client pre-check (`getChildrenNotReady`) feeds the blocked dialog, the POST enforces it.

Available transitions are computed **client-side** from the catalog (role + `next_statuses` ∩ `applicable_models`); there is no `GET transitions/`.

## Catalog once, status as a string, timeline embedded

- `GET /flow/statuses/` returns the whole `Status` row per status plus the computed `admin_targets`; `middleware/dashboard.js` loads it once into `useFlowStore` (`app/store/flow.js`). Never re-denormalize display fields onto each record.
- Model serializers expose `status` — and `FlowEvent.from_status`/`to_status` — as the name string, not a nested object.
- Each participant has `flow_events` and `flow_attachments` (`GenericRelation`s), nested by the detail serializers; the frontend reads them from the record and appends what each POST returns — it never fetches the history separately.

## Frontend contract

`useFlow(app, model, pk)` is the write plumbing; `useFlowActions(record, app, model, options)` the headless kernel (available transitions with their `blocked` reasons, the blocked and confirm/comment dialogs, `runTransition`); `FlowStatusActions` the thin chip + menu + dialogs assembly over it. **Record-as-model**: the flow components take the whole record through `defineModel` and mutate it in place (`record.status = ev.to_status`, `record.flow_events.push(ev)`); the shared reference carries the update, no `@transitioned` handlers. Descendants pass `options.root` to the kernel and `:root` to `FlowComments`. Components, props, split-buttons and the rules registry: [frontend.md](references/frontend.md).

## IES vs reviewer: two surfaces

- **IES** → `/respuestas/[period]`: answers content and runs its own transitions. IES-only fields (`has_good_practices`) live only here.
- **Reviewer** → `/dashboard` collections: scores, validates, runs reviewer transitions; never edits the IES's gen or cp content; **never sees IES-only fields**.

gen and cp share one dual-audience component tree per section (skill `gen-general-info`; cp: [cp.md](references/cp.md)); bp keeps separate detail components (skill `bp-validation-ux`). Content is written outside `flow` — bp and gen through their own viewsets, cp through `/axis_value/`, `/observable_response/` and `/group_response/` (skill `cp-questionnaire`) — while transitions, comments and attachments of any object go through `/flow/{app}/{model}/{pk}/…` (`api/flow/urls.py`).
