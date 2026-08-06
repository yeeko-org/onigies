---
type: task
id: task-87
title: Edición masiva de estatus de buenas prácticas y de envíos
state: open
date: 2026-08-06
owner: ai
source: ["[[2026-08-06-temas-reunion-fer]]"]
---

# Edición masiva de estatus de buenas prácticas y de envíos

Encargo de Ricardo (2026-08-06), a raíz de la revisión con Fernanda: permitir editar **en masa** los estatus de «buenas prácticas» y de «envíos de buenas prácticas» desde el dashboard.

El detonante es el volumen de casos que aparecieron en la llamada: envíos parados en borrador tras el cierre (§13), envíos que hay que reencauzar uno por uno. Hacerlo de a uno no escala para la revisora.

El mecanismo genérico ya existe: `nuxt/app/components/dashboard/common/MassiveEdit.vue`. Lo que falta es habilitarlo para estas dos colecciones y decidir cómo se comporta frente al motor de flujo — un cambio de estatus no es un `PATCH` cualquiera: pasa por `validate_flow_transition` y por las `entry_rules` (ver skill `flow`). Hay que resolver qué ocurre cuando parte del lote no puede transicionar.

## Criterios de aceptación

- [ ] Se pueden seleccionar varias buenas prácticas y cambiarles el estatus en una operación
- [ ] Lo mismo para los envíos de buenas prácticas
- [ ] El lote respeta las reglas del motor de flujo y reporta con claridad lo que no pudo transicionar
