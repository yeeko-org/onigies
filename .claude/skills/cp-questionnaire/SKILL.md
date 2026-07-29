---
name: cp-questionnaire
description: Domain model of the ONIGIES questionnaire per observable (flow
  group `cp`) — the Axis→Component→Observable hierarchy, the five question
  types (A, B, Reach, Plan, Special) and their response models, the seed
  pipeline (`load_questionnaire`), special-case observables, and weights.
  Use when building or debugging questionnaire capture or display (backend
  or frontend), touching `api/question/`, `api/indicator/`, `api/answer/`,
  `question/seed_data/`, or asking how a question type is answered/scored.
---

# cp-questionnaire

The 2026 questionnaire (`cp` flow group). 41 observables in 4 axes.
Decision history lives in `docs/plans/PLAN_seed_cuestionario.md`; this
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
| `load_questionnaire [--sync-institutions]` | Hierarchy texts + order, AQuestion/AOption, BQuestion, ReachQuestion, PlanQuestion, SpecialQuestion, GeneralGroup |
| `load_main_axis` | Only `icon`/`color`/`short_name` of Axis (visual metadata) |
| `load_sectors` | Sector catalog (incl. `is_main`, `is_authority`) |
| `migrate_initial_data` | QuestionType (default_weight a=60, b=40) |

Run order after `migrate`: `load_sectors` → `migrate_initial_data` →
`load_questionnaire --sync-institutions`. The seed is idempotent
(`update_or_create` on natural keys); re-running after editing
`question/seed_data/axis_N.py` is the normal update path.

## Question types ↔ response models

Response chain per survey: `ObservableResponse` (survey + observable,
`value` bool answers `init_question`) → `GroupResponse` (one per
QuestionType, holds the score) → typed responses below. FKs are
CASCADE: deleting a question row deletes its answers (the seed warns
when it prunes stale AQuestion/PlanQuestion rows).

| Question (`question/models.py`) | Response (`answer/models.py`) | Captures |
|---|---|---|
| `AQuestion` — one row per checklist option, key `(observable, order)`; text of the block in `Observable.a_main_question` | `AResponse` → global `AOption` scale (Sí=1 / No=0) | Institucionalización: which options apply |
| `BQuestion` — one per observable (order=1), text copied from `Observable.reach_instances_question`; flags `includes_academic` / `includes_admin` | `BResponse` — `academic_instances_complying`, `admin_instances_complying`, `percentage` | Transversalización: in how many instances it holds |
| `ReachQuestion` — `has_main_sectors`, `others_sectors` M2M, `has_general_planning` | `ReachResponse` — `not_focalized` + M2M `sectors` | Population reach |
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
| 1.7 | Only part A here. Its sex-gender composition block is asked in Generales and stored in `PopulationQuantity`; scored via `Observable.pop_weight`. See `gen-general-info` |

Academic-only BQuestions (`includes_admin=False`): 1.14, 1.15, 1.16,
2.1, 2.2 — set via `b_includes` in `seed_data/axis_N.py` (default is
academic + admin).

## Weights

Per-type weights on `Observable` (`a_weight`, `b_weight`,
`reach_weight`, `plan_weight`, `special_weight`, `pop_weight`) are all
`null` today; `Observable.final_*_weight` falls back to
`QuestionType.default_weight`. Real weights are pending a source from
the client — do not invent them.

## Pending with the client (do not "fix" silently)

- 4.4: reach texts seeded verbatim with a known copy-paste error.
- 2.1/2.2: «instancias académicas» without «administrativas» (their
  `includes_admin=False` may change).

When resolved: correct `docs/questions/all_questions_reduced.md`, then
`seed_data/axis_N.py`, then re-run `load_questionnaire`.
