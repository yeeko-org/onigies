# ONIGIES monorepo

National observatory on gender equality in Mexican higher-education institutions (IES). This monorepo is the active rewrite of a system first built in 2017–2018.

| Directory | Stack | Port |
|-----------|-------|------|
| `api/` | Django REST Framework | 8018 |
| `nuxt/` | Nuxt 4 + Vuetify 3 | 3018 |

Each subproject has its own `CLAUDE.md` with stack-specific conventions.

## Context

The original ONIGIES (Python 2 + Vue 2) still serves the public site and is **not** in this repo. This monorepo is the new system — the `api/` backend plus the `nuxt/` authenticated app (dashboard + IES survey flows). The legacy public site stays live until it is rebuilt.

The new dashboard owns six routes (`/dashboard`, `/respuestas`, `/login`, `/register`, `/forgot-password`, `/recover-password`); everything else under `onigies.unam.mx` is still the legacy public site. Deployment topology and the migration roadmap — currently a temporary nginx bridge to Netlify — live in the `deployment` skill.

## Skill and command prefixes

Skills in `.claude/skills/` and commands in `.claude/commands/` are tagged by scope:

- `[nuxt]` — frontend only, applies in `nuxt/`
- `[api]` — backend only, applies in `api/`
- No prefix — applies to the full monorepo