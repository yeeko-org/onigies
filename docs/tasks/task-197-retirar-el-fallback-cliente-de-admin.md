---
type: task
id: task-197
title: Retirar el fallback cliente de admin_targets cuando API y Netlify estén desplegados
state: open
date: 2026-10-02
owner: ai
source: ["[[2026-10-02-comentarios-editables-y-valvula-de-admin]]"]
related: ["[[task-190]]", "[[adr-0023]]"]
---

# Retirar el fallback cliente de admin_targets cuando API y Netlify estén desplegados

`getAdminTargets` en `store/flow.js` lee `admin_targets` de la fila de status del catálogo y, si falta (catálogo de una API anterior al campo), recalcula el conjunto del grafo. Existe solo porque la API (Yeeko) y el frontend (Netlify) se despliegan por separado; es la regla escrita dos veces (`admin_target_names` en el backend y el fallback en JS) y puede divergir. Con el orden de push de [[task-190]] (API primero, Netlify después) el fallback nunca se ejercita: el front nuevo siempre encuentra el campo. Una vez que ambos deploys estén en producción, borrar el fallback y el test de Vitest que lo cubre, y dejar `references/admin-override.md` de la skill `flow` con una sola fuente.

## Criterios de aceptación

- [ ] Fallback eliminado del store y de los tests
- [ ] La referencia de la skill dice que el backend es la única fuente
