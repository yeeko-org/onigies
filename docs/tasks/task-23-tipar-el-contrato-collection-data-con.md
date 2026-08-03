---
type: task
id: task-23
title: Tipar el contrato collection_data con JSDoc
state: open
date: 2026-08-03
owner: ai
parent: "[[task-3]]"
source: ["[[2026-06-19-recomendaciones-del-dashboard]]"]
---

# Tipar el contrato collection_data con JSDoc

Recomendación 11. `collection_data` es el corazón del dashboard schema-driven y hoy es un `Object` suelto: un error de nombre de propiedad se descubre en runtime. Un `typedef` JSDoc de `collection_data` y de `field` da autocompletado y avisos en el IDE sin migrar a TypeScript.

## Criterios de aceptación

- [ ] `collection_data` y `field` tienen typedef y el IDE avisa de propiedades inexistentes
