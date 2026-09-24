# cp in the flow engine

Detail of the cp group (`AxisValue` → `ObservableResponse` → `GroupResponse`) behind the two cp sections of [SKILL.md](../SKILL.md): read it when touching cp statuses, child rules, the initial «No», or the capture/review components.

## cp catalog

A = `AxisValue` (the unit of send), O = `ObservableResponse` (the unit of work), G = `GroupResponse` (one per question type of the observable, the unit of save).

| status | applies | role | note |
|---|---|---|---|
| `cp_pre_start` | A, O, G | ies | default; the whole tree is born here, except the groups without capture |
| `cp_filling` | A, O, G | ies | auto on first save, propagates up |
| `cp_completed` | O, G | reviewer | IES marked it complete; reviewed once the axis is sent |
| `cp_sent` / `cp_resent` | A | reviewer | axis sent / resent |
| `cp_in_review` | A | reviewer | |
| `cp_need_changes` | A, O, G | ies | reviewer returns it; comment required |
| `cp_in_adjustment` | A, O, G | ies | auto, propagates up |
| `cp_adjusted` | O, G | reviewer | fixes applied |
| `cp_postponed` | O, G | ies | answer later |
| `cp_partial` / `cp_partial_approved` | O, G | reviewer / ies | partial delivery and its approval |
| `cp_voluntary_readjust` | A, O, G | reviewer | IES asks to reopen an approved answer |
| `cp_approved` | A, O, G | ies | public; IES may only ask a readjust; groups without capture are born here |
| `cp_not_present` | O, G | None | «Sin la medida» |

`cp_not_present` is **terminal by domain, not by the motor**: no `next_statuses` point to it or leave it. The IES's «No» to the observable's initial question sets it on the observable and all its groups through `assign_status_tree`, and changing the answer back leaves it the same way (to `cp_filling`; the groups without capture, to `cp_approved`). Both need the axis in the IES's turn and the answer gate open; the «No» is also refused once any group with capture has entered review (the IES asks a readjust instead) — the groups without capture sit in `cp_approved` from birth and do not count. It counts as 0 in the average (a decided rule; scoring is not built yet) and is never reviewed, so it is a valid child in every child rule that moves a parent forward. There is no «no aplica» at the observable level: partial applicability is declared in gen.

Groups without capture (type with `QuestionType.model_response` null, today `population`, whose data lives in gen) are born in `cp_approved` and stay there: their `validate_flow_transition` refuses every menu transition, since `cp_approved` has the ies role and would offer a readjust of something nobody captured. So `cp_approved` is also a valid group in the four observable child rules that move it forward (`cp_completed`, `cp_partial`, `cp_postponed`, `cp_partial_approved`).

Child rules worth knowing: `cp_postponed` requires every group resolved or postponed itself (`cp_completed`, `cp_postponed`, `cp_partial`, `cp_approved`, `cp_not_present`) — without it a postponed observable travelled in `cp_sent` with untouched groups; `cp_partial_approved` accepts `cp_not_present` groups.

The reviewer returns **per group**: the group, the observable and the axis are transitioned separately (`flow.permissions.root_turn_errors` keeps all of them waiting until the axis is sent). What the IES can type is guarded by `answer/group_validation.py` on `cp_completed`/`cp_adjusted` and by the answer gate on everything (skill `cp-questionnaire`).

## cp: the live surfaces

cp also runs end to end, with one tree of components under `components/dashboard/answer/capture/` serving both audiences through a `review` prop (read-only content; transitions, comments and attachments stay):

- **IES** → `/respuestas/[period]`, one `CpAxisCapture` per axis. Each observable is a `CpObservablePanel` (initial question saved on change, the observable's status, groups consultable before answering and editable only after «Sí»); each group a `CpGroupCard` with its own «Guardar» that appears only with changes — **save is per group**, no autosave — and one `CpQuestions{A,B,Reach,Plan,Special}` body per type. The axis payload's `cp_capture` (`{open, reason, open_at}`) drives the gate: closed, the IES sees the whole questionnaire but captures and transitions nothing.
- **Reviewer** → collection «Ejes del cuestionario» (`AxisValue`): `AxisValueHeader` (row with `CpStatusCounts`), `AxisValueEditSimple` (the same `CpAxisCapture` with `review`), `AxisValueSheet` empty on purpose. The survey detail (`SurveyEditSimple`) adds `CpSurveyAxes` below `GeneralGroupList`: the survey's axes, each opening the same review detail in a dialog.

cp is still unpublished for real IES: only `is_test` institutions see it until `PUBLISHED_SECTIONS` (`nuxt/app/utils/sections.js`) includes it.

Next steps are **offered, never taken**: after a group transition, `CpObservablePanel` offers the observable the same status when the child rule now passes; after an observable change, `CpAxisCapture` offers the axis step (or highlights the axis chip when there is more than one destination). The offer is a snackbar with an action (skill `snackbar`). The pure logic — draft per group, PATCH payload with only the changed rows (the backend upserts and never deletes by omission), status counts — lives in `utils/cp_capture.js`, free of Vue so it can be tested alone. O and G pass `options.root` (the axis) to `useFlowActions`.
