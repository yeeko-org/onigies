# onigies monorepo

| Directory | Stack | Port |
|-----------|-------|------|
| `api/` | Django REST Framework | 8018 |
| `nuxt/` | Nuxt 4 + Vuetify 3 | 3018 |

Each subproject has its own `CLAUDE.md` with stack-specific conventions.

## Skill and command prefixes

Skills in `.claude/skills/` and commands in `.claude/commands/` are tagged
by scope:

- `[nuxt]` — frontend only, applies in `nuxt/`
- `[api]` — backend only, applies in `api/`
- No prefix — applies to the full monorepo