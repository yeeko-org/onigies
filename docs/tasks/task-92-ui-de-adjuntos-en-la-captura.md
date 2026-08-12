---
type: task
id: task-92
title: UI de adjuntos en la captura del cuestionario por observable (cp)
state: open
date: 2026-08-06
owner: ai
parent: "[[task-2]]"
related: ["[[task-68]]", "[[task-42]]"]
---

# UI de adjuntos en la captura del cuestionario por observable (cp)

La sesión del 2026-08-06 ([[task-68]]) construyó el stack genérico de adjuntos sobre `flow.Attachment` con UI en generales y Buenas Prácticas; el backend ya sirve también a la cadena cp. Falta montar la UI cuando exista la superficie de captura del cuestionario por observable ([[task-42]]). Decisiones ya tomadas por Ricardo: los adjuntos cp van por `GroupResponse` (nunca por `Observable`) y cuelgan del objeto, no del evento del timeline.

## Criterios de aceptación

- [ ] La IES puede adjuntar evidencia por GroupResponse en la captura cp
- [ ] La revisora ve esos adjuntos en su vista de revisión
