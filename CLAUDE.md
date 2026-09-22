# ONIGIES monorepo

National observatory on gender equality in Mexican higher-education institutions (IES). This monorepo is the active rewrite of a system first built in 2017–2018.

| Directory | Stack | Port |
|-----------|-------|------|
| `api/` | Django REST Framework | 8018 |
| `nuxt/` | Nuxt 4 + Vuetify 3 | 3018 |
| `docs/` | process documentation (`documenter` skill) | — |
| `design-system/` | brand handoff bundle: palette, type, UI kits | — |

Each subproject has its own `CLAUDE.md` with stack-specific conventions.

`docs/` follows the `documenter` scheme — `tasks/`, `decisions/`, `reference/`, `records/`, `notes/`, linked by `[[id]]`. A pre-commit hook (`.githooks/`) validates it; new clones need `git config core.hooksPath .githooks`.

## Context

The original ONIGIES (Python 2 + Vue 2) still serves the public site and is **not** in this repo. This monorepo is the new system — the `api/` backend plus the `nuxt/` authenticated app (dashboard + IES survey flows). The legacy public site stays live until it is rebuilt.

STIG (`~/dev/unam/stig`) is a sister project for the same client (CIGU) but a fully independent system: separate repo, servers, tickets with Cómputo UNAM and roadmap. Nothing said about one applies to the other.

The new dashboard owns six routes (`/dashboard`, `/respuestas`, `/login`, `/register`, `/forgot-password`, `/recover-password`); everything else under `onigies.unam.mx` is still the legacy public site. Deployment topology and the migration roadmap — currently a temporary nginx bridge to Netlify — live in the `deployment` skill.

## Domain and language conventions

- **Client**: CIGU — Coordinación para la Igualdad de Género de la UNAM. Rubén (also «Rubí» in older docs) belongs to its structure and leads ONIGIES there.
- **Who decides**: the methodology formally belongs to ANUIES; CIGU took the project on, so in practice Rubén alone makes many methodological and operational decisions. Attribute decisions to Rubén, not to «the CIGU».
- **«sexo-género»** (hyphenated, standardized by Rubén on 2026-09-04), never «sexo y género» nor just «sexo», in base/general questions and legends.
- **Column order: Mujeres before Hombres**, everywhere (tables, forms, exports).
- **UI wording: «De prueba»**, never «test», for test institutions and related labels.

## Skill and command prefixes

Skills in `.claude/skills/` and commands in `.claude/commands/` are tagged by scope:

- `[nuxt]` — frontend only, applies in `nuxt/`
- `[api]` — backend only, applies in `api/`
- No prefix — applies to the full monorepo