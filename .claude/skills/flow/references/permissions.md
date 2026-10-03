# Permissions: who may transition, edit, comment, attach

Detail behind «Two permissions, and the root governs» in [SKILL.md](../SKILL.md). All helpers live in `api/flow/permissions.py`; the client mirrors in `app/store/flow.js`.

## Membership

`user_can_act_on_flow_object(user, obj)`: reviewers act on any object; an IES user only on objects of their own institution, resolved by walking to the root (`resolve_flow_root`) and reading `root.survey.institution`. Every `/flow/…` view runs it (403); the participants' viewsets restrict list reads in `get_queryset` and use `IsFlowInstitutionOwnerOrReviewer` for object access.

## Content edit

`user_can_edit_flow_content(user, obj)` = membership **and** own status `content_editable` **and** `user_holds_root_turn` **and** no `content_lock_errors`. The client helper `flowStore.canEditContent(obj, root = obj)` knows the first three; `root` defaults to `obj` for roots, descendants pass it explicitly (the caller already holds the nested tree).

`content_lock_errors(user, root)` is a hook on the root model (duck typing, like `validate_flow_transition`): `AxisValue.content_lock_errors` closes all cp content — typed answers, the initial boolean, attachments — while the answer gate is closed (`survey.cp_gate.capture_lock_errors`; reviewers never locked). The frontend gets that state as `cp_capture` (`{open, reason, open_at}`) in the axis and survey payloads instead of re-deriving it. The gate's own rule — the opening date, the `gen_finished` prerequisite, the 403 codes — is skill `cp-questionnaire`.

Content writes check it on the server per group: cp through `ContentWriteMixin` (`api/api/views/answer/`, the reviewer always read-only), bp through its sibling `PracticeContentWriteMixin` (`api/api/views/example/__init__.py`) — an IES create/update/delete of a practice or criterion needs `user_can_edit_flow_content` on the practice (criteria via `flow_delegate`; a new practice is checked against the package, since the default `bp_draft` is IES-role even under `bp_discarded`), `confirm-delete/` included; the reviewer is exempt from the lock but the serializers keep only its review fields (`PRACTICE_REVIEW_FIELDS`, `FEATURE_REVIEW_FIELDS`) and drop the rest silently, as they drop the review fields from the IES. The reviewer never deletes a practice or criterion (403 on `DELETE` and `confirm-delete/`), and `status` is read-only in the practice and package serializers, so it changes only through the `/flow/…/transitions/` endpoints. The admin (`User.is_admin`) is exempt from the three bp reviewer rules — it creates, deletes and writes content with no turn lock (`split_review_fields` keeps everything via `is_admin_request`) —, but the criterion note lock (`comments`, root turn) applies to it like to any reviewer.

## Root turn

`user_holds_root_turn(user, obj)`: the root's status role equals the user's flow role; a terminal root (`role=None`) belongs to nobody. It is the one check for every timeline write ([comments.md](comments.md)) and the criterion note.

`root_turn_errors(user, obj)`: reasons why the reviewer cannot transition a descendant today — non-empty only for a reviewer, on a descendant, with the root in `ies` role. The message is the root's `root_not_sent_message` (class attribute, duck typing; `ROOT_NOT_SENT_MESSAGE` as fallback), exposed to the frontend as `not_sent_message` in the root serializers; `flowStore.getRootNotInTurn(root)` is the client mirror, applied by `useFlowActions` when given `options.root`.

## The model hooks

`validate_flow_transition(user, target) → list[str]`, read by both `validate_transition` and `validate_admin_transition`. What each participant vetoes today:

- `GoodPracticePackage`, `GeneralPackage`: the send when the period is closed (`Period.is_bp_submission_closed` / `is_gen_submission_closed`); reviewers and test institutions are exempt.
- `GoodPractice`: `root_turn_errors`.
- `GeneralGroupResponse`: `root_turn_errors` + completeness of the group's answers for `gen_completed` (`survey.general_validation`).
- `AxisValue`: the answer gate for the IES (`capture_lock_errors`).
- `ObservableResponse`: gate + `root_turn_errors` + the initial question answered for the validated targets.
- `GroupResponse`: a group without capture refuses every menu transition (it sits in `cp_approved`, an IES-role status that would offer a readjust of nothing); then gate + `root_turn_errors` + `answer.group_validation.completion_errors`.

The bp package's `discard/` and `reopen/` actions check the period and the IES turn themselves before calling `execute_transition`.

## Attachments (`api/flow/attachment_views.py`)

Anchored to the **object** (`GenericFK target`), never to a timeline event (`event` stays null), so the history does not change when a file is uploaded or deleted. Reading = membership; writing (upload, delete) = **the IES only** — a reviewer always gets 403, even on an object it may act on — plus `user_can_edit_flow_content` on the owner (so a sent package is closed). Satellites go through `flow_delegate` (`FeatureGoodPractice` → its practice). Downloads go through `download/`, which re-checks the reader (an `is_public` attachment skips it) and redirects to `file.url` on each call: with `USE_S3_FILES` the bucket is private and that URL is freshly signed, otherwise it is the disk path. `AttachmentSerializer.url` is that endpoint, never `file.url`. No extension or content-type filtering on purpose (IES evidence arrives in any format); the only cap is 30 MB. The physical file is deleted by a `post_delete` signal so the GenericRelation cascade also reaches it.

Frontend: `FlowAttachments` (`v-model` = the embedded `flow_attachments`, prop `editable` decided by the parent with `canEditContent`), mutations in place like `FlowComments`.
