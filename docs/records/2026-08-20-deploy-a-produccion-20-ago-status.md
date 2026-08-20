---
type: record
id: 2026-08-20-deploy-a-produccion-20-ago-status
title: "Deploy a producción 20-ago: status_groups desde el backend"
date: 2026-08-20
---

# Deploy a producción 20-ago: status_groups desde el backend

Deploy del rango `fa15b1d..8bfdbf6` (7 commits) siguiendo [[adr-0001|el fast-forward de ADR-0001]]: push de `main` y `production` al mismo ref.

- Sin migraciones, requirements ni seeds en el rango; el cambio en `api/ies/models.py` es solo código (`status_groups_data()`), verificado sin drift de esquema.
- pytest 94 ✓, Vitest 9 ✓. Servidor: pull limpio, `migrate` no-op, «No changes detected», reload con SIGHUP.
- Smoke: `/api/catalogs/all/` y `/api/` 200; `status_groups` ya en el payload (3 grupos); error.log limpio.
- Netlify publicó el build nuevo; verificado por contenido: los literales del mapa viejo de `filters.js` («de Validación», `pre_start`) ya no aparecen en ninguno de los 81 chunks servidos.
- Vistazo manual de Ricardo en dashboard y /respuestas: en orden.
