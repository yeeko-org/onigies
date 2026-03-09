# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working
with code in this monorepo.

## Structure

| Directory | Stack | Port |
|-----------|-------|------|
| `api/` | Django REST Framework (Python) | 8018 |
| `nuxt/` | Nuxt 4 + Vuetify 3 (TypeScript) | 3018 |

Each subproject has its own `CLAUDE.md` with stack-specific conventions.

## Skill and command prefixes

Skills in `.claude/skills/` and commands in `.claude/commands/` are tagged
by scope:

- `[nuxt]` — frontend only, applies when working in `nuxt/`
- `[api]` — backend only, applies when working in `api/`
- No prefix — applies to the full monorepo