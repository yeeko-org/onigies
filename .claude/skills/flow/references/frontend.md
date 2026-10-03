# Frontend: composables, components and the live surfaces

Read when building or debugging a status control, a save-then-transition button, a blocked transition, or the bp package actions. The cp surfaces: [cp.md](cp.md); the gen surfaces: skill `gen-general-info`; comments: [comments.md](comments.md); the admin valve: [admin-override.md](admin-override.md). Everything lives under `nuxt/app/components/dashboard/flow/`, `composables/useFlow*.js`, `composables/flowRules.js` and `store/flow.js`.

## Composables

**`useFlow(appLabel, modelName, pk)`** — write plumbing: builds `/flow/{app}/{model}/{pk}/` and returns `sending` plus `addComment`, `transition`, `editComment`, `deleteComment`, `adminTransition`; each wraps `notifyApiError` and returns the created `FlowEvent` (`undefined` on error, already notified). The three ids may be values, refs or getters (`toValue`), so the URL follows a changing pk. It never fetches history.

**`useFlowActions(record, appLabel, modelName, options)`** — the headless kernel: `transitions` (from `flowStore.getAvailableTransitions`, each carrying `blocked` when the root gate, an `entry_rules` failure or the children rule would stop it, so the menu pre-disables it with the reasons as subtitle), `onSelect(t)`, `runTransition`, the confirm/comment dialog state and the blocked dialog state. Consumers only provide the **activator**.

- `onSelect(t)` re-checks the three gates (the record may have changed since the render), then either opens the blocked dialog, opens the confirm/comment dialog (one dialog for both, when `requires_confirmation || comment_type !== 'none'`), or runs the transition. It returns the `FlowEvent` on a real transition and `null` otherwise — the caller closes its own dialog only when an event came back. A second click while the POST flies is ignored (`sending`).
- `runTransition` mutates in place, shows the snackbar, then awaits `options.onTransitioned(ev)`: for when the mutation isn't enough and the consumer must refetch (`GoodPracticeList` reloads for `sent_at`; `GeneralGroupList` recomputes open panels).
- `options.root` (value, ref or getter): the flow root when `record` is a descendant; its reasons go first in `blocked`. It also returns `root()` and `afterTransition`, which the admin valve reads ([admin-override.md](admin-override.md)).
- `block(title, reasons)` opens the blocked dialog manually.

**`flowRules.js`** — registry name → function returning the missing items; `runEntryRules(entryRules, obj)` → `{ ok, missing }`; unknown names warn in dev and pass. Also home of `flowRoleOf(user)`, the client mirror of `User.is_reviewer`.

**`store/flow.js`** — `CHILD_REGISTRY` maps each parent model to the field where its Full serializer nests the children (`good_practices`, `observable_responses`, `group_responses`, `general_group_responses`) and the label for messages; a root with a children rule must nest them there. `getChildrenNotReady(record, target, modelName)` reads it and returns reasons in Spanish naming the allowed statuses, not the offending child.

## Components

| component | use |
|---|---|
| `FlowStatusChip` | display-only chip; `:status` is the **name string**. Props `label`, `size`, `variant`, `onlyIcon`/`xSmall`, `disabled`; tooltip = `public_name` + `description` + slot `tooltip`; trailing `<slot/>` for appended content. |
| `FlowStatusActions` | the **unified status control**: chip activator (`v-menu`) + `FlowTransitionMenu` + `FlowTransitionDialogs` + `FlowAdminOverride` when the kernel has a root. `v-model` = record; props `appLabel`/`modelName`, `actions` (a kernel built by the parent, to share transitions and dialogs with another trigger), `size`, `variant`, `hint: 'box' \| 'tooltip'` (default `box`). On the user's turn with transitions the chip is a menu activator, else plain. |
| `FlowTransitionMenu` | presentational `v-list` of transitions; `:transitions`, emits `select(t)`, title `action_name \|\| public_name`, slot `lead`. Reused by the chip-menu and the split-button carets. |
| `FlowTransitionDialogs` | presentational confirm/comment dialog (title `confirm_title` or derived, body `confirm_text`, label `comment_prompt` or a generic one, embeds `FlowTimeline`) + `FlowBlockedDialog`, bound via `:actions="kernel"`. Every activator that isn't `FlowStatusActions` must mount it. |
| `FlowBlockedDialog` | presentational «transition blocked»: `v-model`, `title`, `reasons: string[]`. |
| `FlowSaveMenu` | presentational split-button «Guardar ▾»: lead item «Guardar y mantener como {status}» then `FlowTransitionMenu`; plain «Guardar» without transitions. Props `transitions`, `currentStatus`, `loading`, `disabled`, `saveDisabled` (only the plain save), `saveLabel` (replaces the lead text when saving does not keep the status: cp's first save auto-promotes, so `CpGroupCard` drops that transition and labels the lead «Guardar y pasar a …»); emits `save`, `select(t)`. The parent saves-then-transitions and mounts `FlowTransitionDialogs`. Used by gen (`GeneralGroupPanel`), bp (`GoodPracticeEditSimple`) and cp (`CpGroupCard`). |
| `FlowAttachments` | list / upload / delete of the embedded `flow_attachments`; prop `editable` ([permissions.md](permissions.md)). |
| `FlowComments`, `FlowTimeline`, `FlowCommentIcon` | [comments.md](comments.md) |
| `FlowAdminOverride` | [admin-override.md](admin-override.md) |

**Hint placement.** `hint="box"` shows the status `hint` below the chip, turn-sensitive: warning box «Te toca» with `hint`, grey box with `hint_wait` for the role waiting, faint text on terminals. `hint="tooltip"` puts the same text in the chip tooltip plus a small `flag` icon when it is the user's turn — cp uses `tooltip` on observable and group (three levels would stack boxes) and `box` on the axis.

## Split-buttons (alternative activator)

Where a prominent action beats the chip-menu, a split-button drives the same kernel and the chip degrades to display-only (`FlowStatusChip`); no caret when `transitions.length === 0`:

- `GoodPracticeEditSimple`: `FlowSaveMenu` — «Guardar» (`persist`) + items that **save then transition**: `saveAndTransition(t)` = `await persist(); onSelect(t)`, closing only if `onSelect` returned an event. `persist` is split from the close so the save doesn't dismiss the dialog before the transition.
- `GoodPracticeList` (IES): «Enviar a revisión» runs the full kernel on the package with `onTransitioned` reloading the practices. The real gate is the children rule (every practice `bp_completed`), so before `onSelect` it syncs `record.good_practices` with the live list: the children gate reads the embedded array, which goes stale after adds and deletes.

## bp: `has_good_practices` and the two package actions

`has_good_practices` is **orthogonal to the flow** (a boolean on the package, not a status). Two `GoodPracticePackageViewSet` actions (`api/api/views/example/__init__.py`) combine it with a validated transition and return 400 with the motor's error list when invalid:

- `discard/` («No»): `execute_transition(..., bp_discarded)` — turn, graph and children rule checked — then `has_good_practices=False`; `bp_discarded.propagates_down` cascades to the practices. Requires `bp_discarded ∈ next_statuses['bp_draft']` in the seed.
- `reopen/` («Cambiar respuesta»): from `bp_discarded`, `execute_transition(..., bp_draft)` (propagates down); from `bp_draft` (the answer was «Sí») there is nothing to revert, so it only clears `has_good_practices=None`. Both paths require the package in the IES's turn and the period open.

`GoodPracticeList.vue` shows «Respuesta registrada» + «Cambiar respuesta» (→ `reopen`) whenever `has_good_practices != null`, gated by `canEditResponse` (`!isReviewer && periodOpen && packageStatus.role === 'ies'`); the discard dialog texts come from the `bp_discarded` catalog row.

## gen: the live surfaces

One dual-audience `GeneralGroupList` serves the IES and the reviewer; its description lives in skill `gen-general-info`.
