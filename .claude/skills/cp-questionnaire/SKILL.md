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
| `migrate_initial_data` | QuestionType: `order`, `required`, model names always; `public_name` and `default_weight` only on create |

Run order after `migrate`: `load_sectors` → `migrate_initial_data` →
`load_questionnaire --sync-institutions`. The seed is idempotent
(`update_or_create` on natural keys) and **the dashboard rules over the
instrument's texts** (`adr-0014`): observable `name`, `description`,
`init_question`, `a_main_question`, `a_main_subtitle` and every question
`text` are written only at creation (`create_defaults`); structure
(`order`, flags, sectors, bridge rows) is re-asserted every run.
`--overwrite-texts` restores the old behaviour for observables and
questions — never for `Axis`/`Component`, which have been edited by
users. One planned use: the first deploy after 2026-09-07, while nobody
has edited texts yet. Re-running still prunes stale AQuestion/PlanQuestion
rows with CASCADE to answers (`task-133`).

## Question types ↔ response models

Response chain per survey: `ObservableResponse` (survey + observable,
`value` bool answers `init_question`) → `GroupResponse` (one per
QuestionType, holds the score) → typed responses below. FKs are
CASCADE: deleting a question row deletes its answers (the seed warns
when it prunes stale AQuestion/PlanQuestion rows).

| Question (`question/models.py`) | Response (`answer/models.py`) | Captures |
|---|---|---|
| `AQuestion` — one row per checklist option, key `(observable, order)`; stem in `Observable.a_main_question`, instruction line («Mencione/Marque todas las características…») in `Observable.a_main_subtitle` (40 of 41; 2.1 has none) | `AResponse` → global `AOption` scale (Sí=1 / No=0) | «Armonización e institucionalización»: which options apply |
| `BQuestion` — one per observable (order=1); `text` is the only home of that question (seed key `reach_instances_question`, no longer a model field); flags `includes_academic` / `includes_admin` | `BResponse` — `academic_instances_complying`, `admin_instances_complying`, `percentage` | «Transversalidad orgánica»: in how many instances it holds |
| `ReachQuestion` — `has_main_sectors`, `others_sectors` M2M, `has_general_planning` | `ReachResponse` — `not_focalized` + M2M `sectors` | «Transversalidad sectorial»: population reach |
| `PlanQuestion` — key `(observable, order)` | `PlanResponse` — `media_plans`, `superior_plans`, `postgraduate_plans`, `percentage` | Counts per study-plan level |
| `SpecialQuestion` — one per observable | `SpecialResponse` — `total`, `complying`, `compliance_percentage` | Ad-hoc proportions |

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

`QuestionType` (pk `name`: `a_questions`, `reach`, `b_questions`, `plans`, `special`, `population`) is the **source of truth** for the public name of each block (`public_name` — the frontend reads it from `cats.question_type`, never hardcodes it), the block order in editors (`order`: A=1, sectorial=2, orgánica=3, planes=4, especial=5, población=6), whether the type applies to every observable (`required`: A and B) and the default weight (`default_weight`: a=60, b=40, others 0). `population` has no question model: it is captured in Generales.

`ObservableQuestionType` (`question/models.py`; `observable.type_weights`, `question_type.observable_weights`) has one row per (observable, type) that applies, with a nullable `weight`. Effective weight = `row.final_weight` = own weight or the type's default; `Observable.weight_for('plans')` returns `None` when no row exists. The seed creates missing rows (A and B always; reach/plans/special when the question exists; population for 1.7) and never touches `weight`. Today: 120 rows (41/41/35/1/1/1), every `weight` null — real weights are pending the client (`task-15`); do not invent them. Validation of "all weights non-null when a non-required type applies" is a warning, never a block. Known mismatch: 1.12 has a `b_questions` row (required) but no `BQuestion` (`task-135`). Dashboard: catalog `question_type` (editable `public_name`, `default_weight`, `order`; no create/delete) and catalog `observable_question_type` (only `weight` writable, filters `observable` and `question_type`).

## Pending with the client (do not "fix" silently)

- 4.4: reach texts seeded verbatim with a known copy-paste error.
- 2.1/2.2: «instancias académicas» without «administrativas» (their
  `includes_admin=False` may change).

When resolved: correct `docs/reference/cuestionario-2026-reducido.md`, then
`seed_data/axis_N.py`, then re-run `load_questionnaire`.
