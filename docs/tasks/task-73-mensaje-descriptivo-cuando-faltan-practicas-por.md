---
type: task
id: task-73
title: Mensaje descriptivo cuando faltan prácticas por alcanzar un estatus enviable
state: open
date: 2026-08-06
owner: ai
parent: "[[task-98]]"
source: ["[[2026-08-06-temas-reunion-fer]]"]
---

# Mensaje descriptivo cuando faltan prácticas por alcanzar un estatus enviable

§15 de la reunión con Fernanda, `[49:43]`–`[58:41]`, detectado en la prueba en vivo con la cuenta «Fer»/«FP». Al intentar completar el envío aparece: «Antes de completar, faltaban buenas prácticas por alcanzar un estatus válido, completado o descartado». Ricardo reconoció en el momento que **debe ser más descriptivo**: tendría que explicar que para poder enviar, todas las buenas prácticas del paquete deben estar en un estatus enviable (completado o descartado), y **cuáles** están en borrador y hay que mover antes.

El texto se arma en el cliente a partir de las `entry_rules` del status destino: `nuxt/app/composables/flowRules.js` evalúa las reglas y devuelve los faltantes, `nuxt/app/composables/good_practice_validation.js` las traduce al caso de buenas prácticas y `nuxt/app/components/dashboard/flow/FlowBlockedDialog.vue` las muestra. El catálogo de reglas vive en `api/flow/seed.py` (`entry_rules`). Ver el skill `flow`.

## Criterios de aceptación

- [ ] El mensaje explica qué condición falta, no solo que falta
- [ ] El mensaje nombra las buenas prácticas concretas que impiden enviar
- [ ] El mensaje dice qué acción resuelve el bloqueo
