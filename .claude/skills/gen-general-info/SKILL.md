---
name: gen-general-info
description: The «Información de base» / Generales section of the ONIGIES
  survey (flow group `gen`) — the GeneralGroup catalog and its fields
  schema, where each answer is actually stored (Survey columns,
  Survey.sectors, PopulationQuantity), the Sector flags (is_main,
  is_authority), and how observable 1.7's sex-gender composition is
  captured here but scored on the observable. Use when building the
  Generales capture UI, touching GeneralGroup, GeneralGroupResponse,
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
`load_questionnaire`. `GeneralGroup.fields` is a **UI schema**
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
(survey, group): status, comments, attachments, grouped under
`GeneralPackage` (root of the gen flow). It carries no answer data.

## Sector catalog flags (`load_sectors`)

- `is_main=True` — the 10 core populations.
- `STANDARD_EXTRA_SECTORS` («Población externa», «Público en general»)
  — `is_main=False`, appended to every standard ReachQuestion. Kept as
  explicit extras on purpose (decision closed 2026-07-04): the 10
  `is_main` sectors are exactly the composition list of 1.7.
- `is_authority=True` — the 4 authorities: «Titular de la IES»,
  «Máximo cuerpo colegiado de toda la IES», «Titulares de instancias
  académicas», «Titulares de instancias administrativas». Note:
  «Autoridades y alto funcionariado» is NOT an authority — it is a
  population item of 1.13's custom list.
- `needs_name` — sector requires a free-text name when selected.

## PopulationQuantity: composition capture with a dual role

`survey.PopulationQuantity` — per (survey, sector): `number_men`,
`number_women`, `no_apply`, `name`.

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

## `--sync-institutions` gotcha

After adding a GeneralGroup (e.g. `autoridades`), existing Surveys lack
its `GeneralGroupResponse`. `load_questionnaire --sync-institutions`
re-saves every Institution to backfill them. Without it, existing
surveys silently miss the new group.
