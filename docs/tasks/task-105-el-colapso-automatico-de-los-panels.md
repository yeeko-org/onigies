---
type: task
id: task-105
title: El colapso automático de los panels al completar un grupo no funciona
state: open
date: 2026-08-11
owner: ai
parent: "[[task-41]]"
source: ["[[2026-08-11-reunion-con-ruben-sobre-la-informacion-base]]"]
---

# El colapso automático de los panels al completar un grupo no funciona

En la demo de la reunión del 11 de agosto, `[13:24]`, el colapso automático **falló en vivo**: al completar un grupo el panel no se cerró. Es la razón por la que Rubén no validó el comportamiento de los panels — no llegó a verlo funcionando.

Es un bug, no una función faltante: el comportamiento está implementado. `GeneralGroupPanel.vue` emite `collapse` cuando la transición ocurrió y el grupo dejó de ser editable, y `GeneralGroupList.vue` lo saca de la lista de panels abiertos. Hay que reproducir el caso exacto de la demo y ver dónde se rompe la cadena — el candidato natural es que la editabilidad no se recalcule a tiempo tras la transición.

Importa antes del viernes: es lo primero que Rubén va a volver a mirar.

## Criterios de aceptación

- [ ] Al completar un grupo, su panel se colapsa solo
- [ ] Reproducido y corregido el caso exacto que falló en la demo
