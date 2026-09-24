---
type: task
id: task-87
title: Edición masiva de estatus de buenas prácticas y de envíos
state: open
date: 2026-08-06
owner: ai
parent: "[[task-6]]"
source: ["[[2026-08-06-temas-reunion-fer]]"]
related: ["[[2026-09-23-reunion-ruben]]"]
---

# Edición masiva de estatus de buenas prácticas y de envíos

Encargo de Ricardo (2026-08-06), a raíz de la revisión con Fernanda: permitir editar **en masa** los estatus de «buenas prácticas» y de «envíos de buenas prácticas» desde el dashboard.

El detonante es el volumen de casos que aparecieron en la llamada: envíos parados en borrador tras el cierre (§13), envíos que hay que reencauzar uno por uno. Hacerlo de a uno no escala para la revisora.

El mecanismo genérico ya existe: `nuxt/app/components/dashboard/common/MassiveEdit.vue`. Lo que falta es habilitarlo para estas dos colecciones y decidir cómo se comporta frente al motor de flujo — un cambio de estatus no es un `PATCH` cualquiera: pasa por `validate_flow_transition` y por las `entry_rules` (ver skill `flow`). Hay que resolver qué ocurre cuando parte del lote no puede transicionar.

## Criterios de aceptación

- [ ] Se pueden seleccionar varias buenas prácticas y cambiarles el estatus en una operación
- [ ] Lo mismo para los envíos de buenas prácticas
- [ ] El lote respeta las reglas del motor de flujo y reporta con claridad lo que no pudo transicionar

## Reunión con Rubén, 2026-09-23

Fuente: [[2026-09-23-reunion-ruben]]. Las revisoras no están usando el estatus «recibida para dictamen» y lo van a marcar a todas las prácticas juntas. Ricardo, `[1:21:32]`: «después de completadas les ponen "recibidas para dictamen"; más bien, les falta todavía "revisado" a muchas»; `[1:21:55]`: «¿Por qué no usan esto?»; `[1:22:32]`–`[1:22:44]`: «ninguna está en este estatus, que es "recibida para dictamen". Güey, no están usando ese estatus». Rubén, `[1:21:49]`: «como no vamos revisando por universidad sino por práctica…»; `[1:22:04]`: «las tenemos que mandar de 5 en 5»; `[1:22:16]`: «¿Te acuerdas que se mandan juntas todas? Claro, es que tú estás en el filtro de… en el filtro por práctica. Así sí lo podemos hacer»; `[1:22:41]`: «"completado" es del envío, no de la revisión»; `[1:22:59]`: «las vamos a marcar todas juntas cuando se las enviemos, cuando terminemos todo, porque cada revisora no tiene la misma institución siempre»; `[1:23:22]`–`[1:23:25]`: «ya llevamos más de 100 revisadas»; `[1:23:35]`: «al final se les va a tener que marcar, porque si no, no se les pueden enviar juntas todas las prácticas que hayan postulado». Ricardo, `[1:23:29]`: «sí creo que deberían usar ese estatus» (el principio del párrafo es ininteligible, duda T14 de la limpia).

Marcarlas todas juntas es la operación que esta task habilita: es lectura de esta sesión, no algo dicho en la reunión.
