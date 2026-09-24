---
name: cp-questionnaire
description: Domain model of the ONIGIES questionnaire per observable (flow
  group `cp`) — the Axis→Component→Observable hierarchy, the five question
  types (A, B, Reach, Plan, Special) and their response models, the
  `QuestionType` catalog and the `ObservableQuestionType` bridge (which
  types apply to an observable, and its weight), the seed pipeline
  (`load_questionnaire`), special-case observables, and weights.
  Use when building or debugging questionnaire capture or display (backend
  or frontend), touching `api/question/`, `api/indicator/`, `api/answer/`,
  `question/seed_data/`, or asking how a question type is answered/scored.
---

# cp-questionnaire

The 2026 questionnaire (`cp` flow group). 41 observables in 4 axes.
Decision history lives in `docs/records/2026-07-04-seed-del-cuestionario.md`; this
skill documents the *current* model. Sibling skill: `gen-general-info`
(the Generales section); flow statuses: `flow` skill.

## Hierarchy and seeding ownership

`Axis → Component → Observable` (`indicator/models.py`;
`Component.observables` is the only explicit related_name — question
models use default `*_set`).

- **`Observable.number` is a `CharField`, not a number.** "1.1" and
  "1.10" are distinct observables (as Decimal they were equal — that is
  why it was migrated). Never compare or sort it numerically; it is a
  label. Uniqueness is `(component, number)`.
- **`Observable.order`** is the global 1..41 traversal order, assigned
  by `load_questionnaire` (`Meta.ordering = ['order']`). Use it for
  display order, never `number`.

| Command | Owns |
|---|---|
| `load_questionnaire [--sync-institutions] [--overwrite-texts]` | Hierarchy structure + order, AQuestion/AOption, BQuestion, ReachQuestion, PlanQuestion, SpecialQuestion, GeneralGroup, and the `ObservableQuestionType` rows (which types apply; never their `weight`) |
| `load_main_axis` | Only `icon`/`color`/`short_name` of Axis (visual metadata) |
| `load_sectors` | Sector catalog (incl. `is_main`, `is_authority`) |
| `migrate_initial_data` | QuestionType: `order`, `required`, model names always; `public_name`, `default_weight`, `icon`, `color` and `description` only on create |

Run order after `migrate`: `load_sectors` → `migrate_initial_data` →
`load_questionnaire` (retired since 2026-09-10; see `deploy-api`). The seed is idempotent
(`update_or_create` on natural keys) and **the dashboard rules over the
instrument's texts** (`adr-0014`): observable `name`, `description`,
`init_question`, `a_main_question`, `a_main_subtitle` and every question
`text` are written only at creation (`create_defaults`); structure
(`order`, flags, sectors, bridge rows) is re-asserted every run.
`--overwrite-texts` restores the old behaviour for observables and
questions — never for `Axis`/`Component`, which have been edited by
users. Re-running still prunes stale AQuestion/PlanQuestion rows with
CASCADE to answers (`task-133`).

**The seed is retired** (`adr-0015`). `load_questionnaire` already ran for the last time on production (2026-09-10): `QuestionnaireSettings.seeded_at` is set, every invocation aborts unless `--force`, and the dashboard is the only source of the instrument's structure. `--force` is a data-loss decision, not a flag: it re-asserts seed structure over whatever the client built. Details and the backfills that replace `--sync-institutions`: `deploy-api` and `gen-general-info`.

### The questionnaire gate

`QuestionnaireSettings` (`question/models.py`, single row, catalog
`questionnaire_settings`, admin) holds `content_open`. **Open**: the
dashboard creates and deletes questions in the five families and
`ObservableQuestionType` rows, and edits the structural flags of B
(`includes_academic`/`includes_admin`) and Reach (`has_main_sectors`,
`others_sectors`, `has_general_planning`); creating a question assigns
the next `order` and `get_or_create`s its bridge row (type resolved from
`QuestionType.model_question`). **Closed**: only `text` and `weight`
remain writable; POST/DELETE answer 403. The gate is `ContentGateMixin` +
`ContentGatedSerializer` (`api/api/views/content_gate.py`,
`api/api/views/question/serializers.py`), evaluated per request because the
switch flips at runtime. **Closing is one-way from the API**: reopening is
a manual act in the Django admin (Ricardo), so a closed instrument cannot
be reopened by accident from the screen where it is edited. `Sector` is
not under the gate. New questions are created with the text «Nueva
pregunta» because `text` rejects blank (`task-141`).

## Question types ↔ response models

Response chain per survey: `ObservableResponse` (survey + observable,
`value` bool answers `init_question`) → `GroupResponse` (one per
QuestionType that applies, reverse accessor `statuses`; its `value` is
reserved for the score) → typed responses below. The first two are
**eager**: `Institution.save` provisions them for every axis
(`provision_cp_responses`, 41 observables and ~120 groups per survey;
`resave_institutions` is the backfill), guarded by unique constraints
`(survey, observable)` and `(observable_response, question_type)`. Typed
responses are **lazy**, created by the first save of their group. FKs are
CASCADE: deleting a question row deletes its answers (the seed warns
when it prunes stale AQuestion/PlanQuestion rows).

`ObservableResponse.value` governs the flow, not only the content: `False`
(«Sin la medida») moves the observable and its groups to
`cp_not_present` — worth 0 in the average, terminal, never reviewed —; leaving
`False` returns them to `cp_filling` (groups without capture, to
`cp_approved`). Typed answers already captured survive a
«No» in case the IES changes its mind. Status semantics: skill `flow`.

**Scoring does not exist yet**: no code fills `GroupResponse.value`,
`AxisValue.value` or `ComponentValue.value`, and the formulas are pending the
client (tasks 15, 28, 29, 111). Do not derive one from the weights below.

| Question (`question/models.py`) | Response (`answer/models.py`) | Captures |
|---|---|---|
| `AQuestion` — one row per checklist option, key `(observable, order)`; stem in `Observable.a_main_question`, instruction line («Mencione/Marque todas las características…») in `Observable.a_main_subtitle` (40 of 41; 2.1 has none) | `AResponse` → global `AOption` scale (Sí=1 / No=0) | «Armonización e institucionalización»: which options apply |
| `BQuestion` — one per observable (order=1); `text` is the only home of that question (seed key `reach_instances_question`, no longer a model field); flags `includes_academic` / `includes_admin` | `BResponse` — `academic_instances_complying`, `admin_instances_complying`, `percentage` | «Transversalidad orgánica»: in how many instances it holds |
| `ReachQuestion` — `has_main_sectors`, `others_sectors` M2M, `has_general_planning` | `ReachResponse` — `not_focalized` + M2M `sectors` | «Transversalidad sectorial»: population reach |
| `PlanQuestion` — key `(observable, order)` | `PlanResponse` — `media_plans`, `superior_plans`, `postgraduate_plans`, `percentage` | Counts per study-plan level |
| `SpecialQuestion` — one per observable | `SpecialResponse` — `total`, `complying`, `compliance_percentage` | Ad-hoc proportions |

## Capture (API)

Three endpoints (`api/api/views/answer/`); transitions, comments and
attachments go through `/flow/`:

- `GET /axis_value/` — collection «Ejes del cuestionario», read-only; the axis
  is the root and the unit of send. The list row carries
  `observables_by_status`; the detail carries the whole questionnaire of the
  axis with its answers (`observable_responses[].observable_full` and
  `.group_responses[]`), the global A scale, the gen denominators the B and plan
  counts are checked against, and `cp_capture` (the gate state). One read serves
  the capture: the frontend never fetches observables one by one.
- `PATCH /observable_response/{id}/` `{value}` — the initial answer; its flow
  effect lives in `answer/services.py` (`set_init_value`).
- `PATCH /group_response/{id}/` — one group's typed answers, only the list of
  the group's own type (`a_responses`, `b_responses`, …), rows keyed by
  `question`. It **upserts per question and never deletes by omission** (the IES
  captures across sessions), and the first save promotes the group to
  `cp_filling`.

Both PATCH return the ancestors' status after propagation (`observable_status`,
`axis_status`) so the client does not reread them. Each group carries
`completion` `{errors, warnings}`: `answer/group_validation.py` holds the rules
per type and is also the motor hook that refuses `cp_completed`/`cp_adjusted`
with errors. Where a rule depends on a gen value the IES has not declared, it
warns instead of blocking. `population` (1.7) has no capturable content here:
its groups are born in `cp_approved` and get neither PATCH nor review
(criterion: `QuestionType.model_response is None`, not the type name).

**The answer gate** (`survey/cp_gate.py`): the IES captures only when the period
opened answers (`Period.cp_open_at` reached, set in the admin) and its gen
section is closed (`GeneralPackage` in `gen_finished`). Until then it sees the
questionnaire but writes nothing — answers, initial boolean, transitions,
attachments — through the `AxisValue.content_lock_errors` and
`validate_flow_transition` hooks; direct writes get 403 with `code`
`cp_not_open` / `gen_not_approved`. Test institutions skip the date, not the
validated gen. The
reviewer never captures (403 `reviewer_read_only`) and the gate does not stop
its transitions.

Frontend surfaces and the review mode: skill `flow`, «cp: the live surfaces».

## Reach: POB-ESTÁNDAR and variants

- Standard reach (33 of 35 ReachQuestions): `has_main_sectors=True` +
  `others_sectors` = `STANDARD_EXTRA_SECTORS` («Población externa»,
  «Público en general») → 12 populations = 10 `is_main` sectors + 2.
- Custom lists: `has_main_sectors=False` + full list in
  `others_sectors` — 1.6 (Titular / Máximo cuerpo colegiado), 1.13
  (6 populations), 1.16 (3 student levels).
- `has_general_planning` (only 1.4 and 1.9) is an **escape option**
  («covered by general planning»), not a population; the answer lands
  in `ReachResponse.not_focalized`.

## Special observables

| Observable | Shape |
|---|---|
| 1.1, 4.1, 1.15, 4.7 | No ReachQuestion; measured only via their BQuestion (instance counts) |
| 1.6 | ReachQuestion with the 2 authority roles as custom list |
| 1.12 | No Reach/BQuestion; 4 PlanQuestions (one per sub-question) |
| 1.14 | SpecialQuestion (research projects led by women) + academic-only BQuestion |
| 1.7 | Only part A here. Its sex-gender composition block is asked in Generales and stored in `PopulationQuantity`; scored via its `population` bridge row (seed key `"population": True`). See `gen-general-info` |

Academic-only BQuestions (`includes_admin=False`): 1.14, 1.15, 1.16,
2.1, 2.2 — set via `b_includes` in `seed_data/axis_N.py` (default is
academic + admin).

## QuestionType and the bridge (weights, applicability, names)

`QuestionType` (pk `name`: `a_questions`, `reach`, `b_questions`, `plans`, `special`, `population`) is the **source of truth** for the public name of each block (`public_name` — the frontend reads it from `cats.question_type`, never hardcodes it), the block order in editors (`order`: A=1, sectorial=2, orgánica=3, planes=4, especial=5, población=6), whether the type applies to every observable (`required`: A and B) the default weight (`default_weight`: A 5, reach 2.5, B 2.5, null for plans/special/population — the tentative weighting agreed with Rubén on 2026-09-07) the block's `icon`/`color` (editable; the frontend reads them from the catalog so a type without a collection, like `population`, needs no hardcoded map) and its `description`, one sentence on what the block measures (editable; the seeded texts are drafts pending Rubén's review). `population` has no question model: it is captured in Generales.

`ObservableQuestionType` (`question/models.py`; `observable.type_weights`, `question_type.observable_weights`) has one row per (observable, type) that applies, with a nullable `weight`. Effective weight = `row.final_weight` = own weight, or the type's default **only when the observable has exactly the standard trio {A, reach, B}** (`Observable.uses_default_weights`, `adr-0015`): the defaults were calibrated for that combination, so any other set must carry every weight by hand and the observable reports `weights_pending` (detail and list) until it does — a warning, never a save blocker. `Observable.weight_for('plans')` returns `None` when no row exists. The seed creates missing rows (A and B always; reach/plans/special when the question exists; population for 1.7) and never touches `weight`. Today: 120 rows (41/41/35/1/1/1), every `weight` null — real weights are pending the client (`task-15`); do not invent them. Validation of "all weights non-null when a non-required type applies" is a warning, never a block. Known mismatch: 1.12 has a `b_questions` row (required) but no `BQuestion`; the client adds it from the dashboard while the questionnaire is open (`task-135`). Dashboard: catalog `question_type` (editable `public_name`, `default_weight`, `icon`, `color`, `description`; no create/delete; `order` is never edited from a form) and catalog `observable_question_type` (`weight` always writable; create/delete only while the questionnaire is open, see the gate above). The observable editor captures weights in its type list, showing the inherited default as placeholder.

## Pending with the client (do not "fix" silently)

- 4.4: reach texts seeded verbatim with a known copy-paste error.
- 2.1/2.2: «instancias académicas» without «administrativas» (their
  `includes_admin=False` may change).

When resolved: correct `docs/reference/cuestionario-2026-reducido.md`; the
text itself is fixed from the dashboard (the seed no longer re-runs after
its last deploy, see the gate above), and `seed_data/axis_N.py` only if a
fresh install must match.
