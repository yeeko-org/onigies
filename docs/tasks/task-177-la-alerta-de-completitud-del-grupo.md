---
type: task
id: task-177
title: La alerta de completitud del grupo cp no debe leerse como rechazo tras un guardado normal
state: open
date: 2026-09-25
owner: ai
parent: "[[task-2]]"
related: ["[[task-174]]", "[[task-169]]"]
---

# La alerta de completitud del grupo cp no debe leerse como rechazo tras un guardado normal

Viene de la §Alerta de [[task-174]], que se cerró el 2026-09-25 con el bug de la transición redundante corregido y esta parte sin tocar.

El `v-alert type="error"` de `completion.errors` en `CpGroupCard.vue` se llena tras cada guardado y dice «Para marcar este bloque como completado falta: …». Tras el primer guardado de un grupo «Por iniciar» sigue apareciendo en rojo aunque la IES no pidió «Marcar como completado», y esa lista roja es parte de lo que Ricardo leyó en la reunión del 23 como «no me deja guardarlo». Es UX, no bug: las respuestas se guardan.

Propuesta: tono informativo o `warning` por defecto (lo que falta para completar, como guía), y rojo solo tras un intento rechazado de «Marcar como completado» (el 400 del POST `cp_completed`). Relacionado con la descubribilidad de «Marcar como completado» dentro de «Guardar ▾» ([[task-169]], hallazgos de los ejecutores).

## Criterios de aceptación

- [ ] Tras un guardado sin transición la lista de faltantes se muestra en tono informativo
- [ ] Tras un «Marcar como completado» rechazado la lista se muestra en rojo
- [ ] Propuesta de e2e presentada a Ricardo si la suite cp de task-166 ya existe
