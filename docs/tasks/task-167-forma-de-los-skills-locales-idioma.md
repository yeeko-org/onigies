---
type: task
id: task-167
title: "Forma de los skills locales: idioma, prosa envuelta, descripciones, tamaño y duplicados con los CLAUDE.md"
state: open
date: 2026-09-22
owner: ricardo
source: ["[[2026-09-22-cierre-cuestionario-principal-captura-y-borrado]]"]
related: ["[[task-138]]"]
---

# Forma de los skills locales: idioma, prosa envuelta, descripciones, tamaño y duplicados con los CLAUDE.md

Hallazgos del auditor de congruencia del 22 de septiembre que Ricardo dejó para una sesión propia. Son de forma, no de verdad: lo falso ya se corrigió ese día.

- **Idioma:** la regla global `create-skill` dice «project skills in Spanish» y `rules/workflow.md` dice «the harness's own skills … written in English»; los doce skills de onigies están en inglés. Es una contradicción del harness global; se resuelve desde `~/.claude`.
- **Prosa envuelta a 80 columnas** (contra la regla global de nunca hard-wrap en .md) en `flow`, `gen-general-info`, `bp-validation-ux`, `snackbar`, `.claude/commands/invitations.md`, y partes de `cp-questionnaire`, `dashboard-collections` y `manage-collections`; `api/CLAUDE.md` líneas 41-44 y 48-56.
- **Descripciones** con rutas (`flow`, `cp-questionnaire`) y por encima de 250 caracteres (`gen-general-info` ~690, `bp-validation-ux` ~580, `dashboard-collections` ~535, `playwright-e2e` ~530, `cp-questionnaire` ~510). Falta la tabla «Modules and skills» en el `CLAUDE.md` raíz como router de rutas a skills; hoy solo hay los prefijos `[nuxt]`/`[api]`.
- **Cuerpos por encima de 12 mil caracteres:** `dashboard-collections` (~17,7k), `deploy-api` (~13,8k), `cp-questionnaire` (~13,3k). `flow` se partió el mismo día con `references/cp.md`.
- **Contenido que `create-skill` deja fuera:** ids de tasks y ADR dentro de `cp-questionnaire` y `gen-general-info`; la sección «Pending with the client» de `cp-questionnaire`; tablas «Key files» en `bp-validation-ux` y `dashboard-collections`; decisiones fechadas en `dashboard-collections`.
- `send-mail/SKILL.md` declara `name: send-email`; el comando lo da la carpeta.
- `.claude/commands/invitations.md`: guía de API para frontend guardada como comando, sin frontmatter y con CRLF; además dice que el administrador debe crear dos plantillas que la migración `email_send.0002` ya crea. Destino probable: `docs/reference/`.
- **Duplicados:** `nuxt/CLAUDE.md` repite a `dashboard-collections` (colección vs categoría, contrato `{data}|{errors}`) y a `nuxt/TESTING.md` (comandos de tests; y le falta `test:unit`); `playwright-e2e` trae una tabla de cobertura vieja copiada de `nuxt/TESTING.md` (sin `respuestas-tabs` ni los `gen-*`) y una línea «Add pytest-django» que ya es el nivel api; la frase sobre STIG del `CLAUDE.md` raíz repite la de `~/dev/CLAUDE.md`; `api/CLAUDE.md` 52-54 repite en parte `coding-preferences-backend.md`.
- Ningún skill editado el 22 de septiembre lleva sello `metadata.rules` salvo `deploy-api`.
- `nuxt/TESTING.md` dice que Vitest cubre «la IES real no ve cp»; sigue siendo cierto hasta que cp se publique.

## Criterios de aceptación

- [ ] Decidido el idioma de los skills locales (y corregida la contradicción global)
- [ ] Descripciones sin rutas y bajo 250 caracteres, con la tabla «Modules and skills» en el CLAUDE.md raíz
- [ ] Prosa des-envuelta en los skills y CLAUDE.md listados
- [ ] invitations.md movido o borrado; send-mail con name alineado
- [ ] Duplicados resueltos con una sola casa por tema
