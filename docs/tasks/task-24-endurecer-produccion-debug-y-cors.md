---
type: task
id: task-24
title: "Endurecer producción: DEBUG y CORS"
state: closed
date: 2026-08-03
owner: ai
parent: "[[task-4]]"
source: ["[[2026-07-29-commits-tematicos-y-deploy-flow]]"]
---

# Endurecer producción: DEBUG y CORS

Durante el smoke del deploy de julio se asomó una traza de Django en un 404: producción corre con `DEBUG=True`, y `CORS_ORIGIN_ALLOW_ALL=True` deja el API abierto a cualquier origen. Ambos viven en `api/core/settings/__init__.py`; el segundo debe pasar a una allowlist con los dominios reales.

## Criterios de aceptación

- [x] `DEBUG` es False en producción
- [x] El CORS acepta solo los orígenes de ONIGIES
