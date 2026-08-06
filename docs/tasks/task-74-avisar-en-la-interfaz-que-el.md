---
type: task
id: task-74
title: Avisar en la interfaz que el periodo cerró y ya no se puede editar
state: open
date: 2026-08-06
owner: ai
source: ["[[2026-08-06-temas-reunion-fer]]"]
related: ["[[task-10]]"]
---

# Avisar en la interfaz que el periodo cerró y ya no se puede editar

§15 de la reunión con Fernanda, `[55:45]`–`[58:41]`. Hoy, pasada la fecha límite, el sistema bloquea algunas acciones (enviar, cambiar de estatus) pero **no dice nada**: la IES descubre el cierre al chocar con un botón que no responde. Fernanda planteó en `[58:25]` que hiciera falta un aviso automático de que el periodo ya se cerró, y Ricardo cerró con «eso sí lo agrego» en `[58:41]`.

**Es este aviso lo que Ricardo se comprometió a agregar** — no el recordatorio previo al cierre, que quedó como propuesta a Rubí por no estar presupuestado (`[57:39]`).

El aviso es la cara visible del candado que [[task-10]] endurece en el backend: si el bloqueo va a ser total, la interfaz tiene que decirlo de forma clara y anticipada, no dejar que la usuaria lo descubra por ensayo y error.

## Criterios de aceptación

- [ ] Con el periodo cerrado, la IES ve un aviso explícito de que ya no puede editar
- [ ] El aviso se muestra al entrar a la sección, no solo al intentar una acción bloqueada
