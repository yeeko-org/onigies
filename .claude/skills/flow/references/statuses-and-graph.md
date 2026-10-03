# Statuses and the graph

Detail behind the «one rule» and «the motor» sections of [SKILL.md](../SKILL.md): read it when adding or changing a status, a transition, a child rule, or when an object is born with the wrong status.

## Status fields (`api/flow/models.py`)

PK is `name` (`bp_draft`). What each field is for, where the name does not say it:

| field | meaning |
|---|---|
| `role` | whose turn; `None` = terminal |
| `group` | `bp` / `cp` / `gen` |
| `public_name` | the **state** the chip shows («Enviado a revisión») |
| `action_name` | the **verb** of the menu item that transitions INTO it («Enviar a revisión»); `None` when never a manual target |
| `description` | base text of the chip tooltip |
| `content_editable` | the turn-holder may edit content here, vs. only transition. Separates «my turn to edit» (`bp_completed`, `bp_adjusted`: editable bookmarks before the send) from «my turn to only transition» (`bp_discarded`, review states) |
| `is_default` | one per group (DB constraint); assigned by a `post_save` signal to any participant created without status, with no `FlowEvent` |
| `is_public` | the record shows on the public site in this status |
| `comment_type` | `none` / `optional` / `required` — whether the transition INTO it asks for a comment; only `required` is enforced by the motor |
| `comment_prompt` | label of the comment box; empty → the frontend's generic text |
| `propagates_up` / `propagates_down` | on assignment, the parent / all descendants adopt it too |
| `auto_on_first_save` | assigned by `assign_auto_status` on the object's first save (`cp_filling`, `cp_in_adjustment`) |
| `hint` / `hint_wait` | next-step guidance for the role in turn / for the role waiting (empty falls back to `hint`); `FlowStatusActions` shows it below the chip or in its tooltip |
| `priority` | urgency, higher first; sorts status summaries (`SurveyHeader` group counts) and the admin targets list |
| `requires_confirmation` + `confirm_title` / `confirm_text` | the frontend asks before transitioning INTO it; empty title → derived from `action_name` |
| `entry_rules` | JSON list of `flowRules` names that must pass to move INTO it — client-side only |
| `next_statuses` (M2M self) | allowed outgoing transitions |
| `valid_child_statuses` (M2M self) | to move a PARENT here, ALL children must be in one of these; empty = no rule |
| `applicable_models` (M2M ContentType) | which models the status applies to; filters transitions and propagation |

`order` is the catalog order (`Meta.ordering`), distinct from `priority`.

## Hierarchy and registry (`api/flow/registry.py`)

Topology lives **on each model, not in a central dict**: a participant inherits the `FlowParticipant` mixin (a marker, no fields → no migration) and declares `flow_parent = '<fk field>'`; roots leave the default `None`. The children side is **not** declared — `get_children` derives the reverse accessor from the child's `flow_parent` FK (cached; each parent has one child type, the chains are linear), so each edge is written once. `ComponentValue` does not participate.

Satellites: a model without status that still hangs on the flow declares `flow_delegate = '<fk>'` (`FeatureGoodPractice → good_practice`); `resolve_flow_owner` returns the object whose permissions govern it. Today only attachments use it.

Helpers: `get_parent`, `get_children`, `is_flow_participant`, `resolve_flow_root` (in `permissions.py`).

## How objects are born

The roots (`GoodPracticePackage`, `AxisValue`, `GeneralPackage`) are created eagerly in `Institution.save`, and so is the whole cp tree below each axis — `ObservableResponse` and `GroupResponse` — by `answer.models.provision_cp_responses` (idempotent). That function sets `cp_pre_start` itself because `bulk_create` skips the `post_save` signal; the groups without capture (question type with `model_response` null, today `population`) are born in `cp_approved` and stay there. Only the typed answers are lazy.

## bp catalog (worked example)

P = `GoodPracticePackage`, G = `GoodPractice`.

| status | applies | role | note |
|---|---|---|---|
| `bp_draft` | P, G | ies | default; IES edits freely; propagates down (the reopen) |
| `bp_discarded` | P, G | ies | «No tengo buenas prácticas»; propagates down to the practices |
| `bp_completed` | G | reviewer | IES marked it complete; waits for the package send |
| `bp_sent` | P | reviewer | package in review |
| `bp_need_changes` | P, G | ies | reviewer asked for fixes; comment required |
| `bp_adjusted` | G | reviewer | fixes applied, awaiting re-review |
| `bp_resent` | P | reviewer | package resent |
| `bp_for_ruling` / `bp_rejected` | G | None | terminal per practice; `bp_rejected` requires a comment |
| `bp_finished` | P | None | terminal package |

Child rules (`VALID_CHILD_STATUSES` in the seed): `bp_sent ← bp_completed, bp_discarded`; `bp_discarded ← bp_discarded, bp_draft, bp_need_changes`; `bp_resent ← bp_adjusted, bp_completed, bp_for_ruling, bp_rejected` (mixed rounds: some practices already ruled, others adjusted); `bp_finished ← bp_for_ruling, bp_rejected`. So sending the package is blocked by the motor until every practice is `bp_completed` (or discarded).

Entry rules: `practice_complete` on `bp_completed` and `bp_adjusted` (the practice form passes `good_practice_validation.js`), `features_rated` on `bp_for_ruling` (every marked feature carries the reviewer's rating). The send itself has no entry rule: its gate is the children rule, mirrored client-side by `getChildrenNotReady`.

`has_good_practices` and the `discard/` / `reopen/` package actions that wrap `bp_discarded` / `bp_draft`: [frontend.md](frontend.md).

## gen specifics

Mirror of bp (`GeneralPackage` → the five `GeneralGroupResponse`), with two differences: `gen_approved` / `gen_finished` are terminal in every direction (nothing leaves them — the generals feed the start of cp), and `gen_need_changes` does **not** propagate up: the reviewer returns the group and the package separately. The package send is gated by `valid_child_statuses` (all five groups `gen_completed`) and by the period lock. A group's hook also refuses `gen_completed` with missing answers (`survey.general_validation`, mirror of the frontend gate). Content is written against `Survey`, not the flow wrappers: skill `gen-general-info`.

`sent_at` on `GoodPracticePackage` and `GeneralPackage` is set by the model's `save()` when the status becomes `*_sent` / `*_resent` — never from the client.
