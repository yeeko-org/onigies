---
type: task
id: task-77
title: El filtro de estatus de envíos de buenas prácticas no funciona bien
state: open
date: 2026-08-06
owner: ai
parent: "[[task-6]]"
source: ["[[2026-08-06-temas-reunion-fer]]"]
related: ["[[task-9]]"]
---

# El filtro de estatus de envíos de buenas prácticas no funciona bien

§12 de la reunión con Fernanda, `[29:43]`–`[34:37]`, dictado por Ricardo en el bloque de pendientes: el filtro de estatus de envío de buenas prácticas en el listado del dashboard no funciona bien.

Sospecha de origen, a verificar: [[task-9]] documenta que `status_filters` sigue hardcodeado en el frontend (`composables/filters.js`, `fetch.js`) y que `HeaderCommon` bifurca entre el motor nuevo de `flow` y los `status_groups` viejos. Si el filtro del listado se arma con el mapa viejo, no puede coincidir con los estatus que devuelve el motor. Conviene mirar ambas cosas a la vez.

## Criterios de aceptación

- [ ] Filtrar por estatus en el listado de envíos devuelve exactamente los envíos de ese estatus
- [ ] Las opciones del filtro corresponden a los estatus reales del motor de flujo
