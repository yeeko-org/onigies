---
name: gen-general-info
description: The «Información de base» / Generales section of the ONIGIES
  survey (flow group `gen`) — the GeneralGroup catalog and its fields
  schema, where each answer is actually stored (Survey columns,
  Survey.sectors, PopulationQuantity), the Sector flags (is_main,
  is_authority, is_standard_extra, is_ies_head), the capture surface
  (GeneralGroupList and friends) and the period lock, and how observable
  1.7's sex-gender composition is captured here but scored on the
  observable. Use when building the Generales capture UI, touching
  GeneralGroup, GeneralGroupResponse, GeneralPackage,
  PopulationQuantity or Survey base fields, or population/authority
  checklists.
---

# gen-general-info

The Generales section (`gen` flow group) captures institutional facts
per Survey (= institution + period), before the per-observable
questionnaire. Sibling skill: `cp-questionnaire`; flow statuses:
`flow` skill (gen is terminal-absolute and a prerequisite for cp).

## The 5 GeneralGroups and where each answer lives

Catalog: `question/seed_data/catalogs.py` (`GENERAL_GROUPS`), seeded by
`load_questionnaire`. `GeneralGroup.order` (the model's `Meta.ordering`)
fixes the instrument's order — `autoridades`, seeded last, would
otherwise land at the end. `GeneralGroup.fields` is a **UI schema**
(`{name, label, type}` with `type ∈ {integer, boolean}`) — the values
themselves are NOT stored on the group response:

| Group | fields | Values stored in |
|---|---|---|
| `estructuras` | `academic_instances`, `admin_instances` (integer) | Same-named `Survey` columns |
| `poblaciones` | `[]` — checklist from Sector catalog (POB-ESTÁNDAR: 10 `is_main` + «Población externa», «Público en general») | Selection → `Survey.sectors` M2M; men/women counts → `PopulationQuantity` |
| `autoridades` | `[]` — checklist from Sectors with `is_authority=True` | `PopulationQuantity` |
| `planes_estudio` | `media_plans`, `superior_plans`, `postgraduate_plans` (integer) | Same-named `Survey` columns |
| `forma_gobierno` | `decentralized`, `centralized` (boolean) | **Gotcha:** `Survey` has a single `is_centralized` boolean — the two UI options map to one field; the frontend must translate |

`GeneralGroupResponse` (`survey/models.py`) is the flow wrapper per
(survey, group): status, `flow_events`, `flow_attachments`. It carries
no answer data. Its parent `GeneralPackage` (1:1 with Survey, root of
the gen flow, mirror of `GoodPracticePackage`) holds the package status
and a `sent_at` stamped by its own `save()`, and vetoes the IES's
transitions once the period closed (`validate_flow_transition`).

## Sector catalog flags (`load_sectors`)

Four booleans (`indicator/models.py`) are enough to build the whole
section; a sector with none of them is not captured here:

- `is_main=True` — the 10 core populations.
- `is_standard_extra=True` — «Población externa», «Público en general»,
  the 2 that complete POB-ESTÁNDAR (`is_main=False`), appended to every
  standard ReachQuestion. Kept as explicit extras on purpose (decision
  closed 2026-07-04): the 10 `is_main` sectors are exactly the
  composition list of 1.7.
- `is_authority=True` — the 4 authorities: «Titular de la IES»,
  «Máximo cuerpo colegiado de toda la IES», «Titulares de instancias
  académicas», «Titulares de instancias administrativas». Note:
  «Autoridades y alto funcionariado» is NOT an authority — it is a
  population item of 1.13's custom list.
- `is_ies_head=True` — «Titular de la IES» only: the single-person
  authority, captured as «¿Mujer?» instead of a head count, so the UI
  singles it out from the other three.
- `needs_name` — sector requires a free-text name when selected.

## PopulationQuantity: composition capture with a dual role

`survey.PopulationQuantity` — per (survey, sector): `number_men`,
`number_women`, `no_apply`, `name` (`name` optional since migration
`survey 0008`; `no_apply` is not captured today, pending `docs/tasks/task-56`).

1. **Population visualizations** — direct men/women data per sector.
2. **Scores observable 1.7** (integración paritaria) via
   `Observable.pop_weight`. Decision 2026-07-04: 1.7's sex-gender
   composition block was moved OUT of the observable and is asked here
   (autoridades + poblaciones groups); the observable keeps only its
   part A.

Details: 1.7's composition uses **only the 10 `is_main` sectors** (not
the 2 extras). «Titular de la IES» is captured as total 1 with
`number_women` 0/1 (the «Mujer: sí/no» answer); percentages for the
other authorities derive from men/women.

## Where the content is written (adr-0008)

Everything goes in one **PATCH `/survey/{id}/`** — scalars, `sectors`
and nested `population_quantities` (`api/api/views/survey/serializers.py`);
the flow wrappers accept no content and flow travels through the generic
`/flow/` endpoints. Saving from any group persists the whole section.

`population_quantities` has **total-sync** semantics: if the key travels,
the list IS the final state (upsert by `(survey, sector)`, deletion by
omission) — hence PATCH, never PUT. The frontend sends only rows with
some count (`buildPayload`): existence lives in `sectors`, and the
extras (`is_standard_extra`) carry no counts at all. Reading composition
means crossing `sectors` (existence) with `population_quantities`
(counts); «Titular de la IES» never enters `sectors`.

## Capture surface (one dual-audience component)

| File (`nuxt/app/`) | Role |
|---|---|
| `components/dashboard/survey/GeneralGroupList.vue` | the section: the Survey with its nested `general_package`, `persist()` (the PATCH), the package send and the period lock |
| `.../survey/GeneralGroupPanel.vue` | one expansion panel per group: its body + split-button "Guardar" / group transitions |
| `.../survey/General{Populations,Authorities,NumberFields,NumberInput,Government}.vue` | the per-group bodies |
| `.../survey/survey/Survey{Header,Sheet,EditSimple}.vue` | the reviewer's collection «Cuestionarios de las IES» |
| `composables/useGeneralSurvey.js` | sector lists by flag, `PopulationQuantity` rows, `buildPayload()` |

`GeneralGroupList` is **dual-audience**: it resolves role, editability
(`flowStore.canEditContent(group, general_package)`) and the available
transitions by itself, so the reviewer's `SurveyEditSimple` just mounts
it — read-only, since the reviewer transitions and comments but does not
edit content. Entry points: IES `/respuestas/[period]`, tab «Información
base»; reviewer, the Survey collection (plus a menu-less «Envíos de
preguntas generales» over `GeneralPackage`).

**Period lock.** `Period.gen_submission_deadline` +
`Period.is_gen_submission_closed` (the deadline day still counts as
open; unlike bp there is no manual publication flag). Authoritative on
the server — the frontend reads the flag, it never recomputes it with
the client clock.

## `--sync-institutions` gotcha

After adding a GeneralGroup (e.g. `autoridades`), existing Surveys lack
its `GeneralGroupResponse`. `load_questionnaire --sync-institutions`
re-saves every Institution to backfill them. Without it, existing
surveys silently miss the new group.
