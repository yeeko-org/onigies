---
type: task
id: task-183
title: Dónde se guarda la regla «lo operativo entre Rubén y las IES no se registra en el grafo»
state: closed
date: 2026-09-28
owner: ricardo
related: ["[[task-165]]", "[[task-175]]", "[[2026-09-28-panorama-onigies]]"]
---

# Dónde se guarda la regla «lo operativo entre Rubén y las IES no se registra en el grafo»

Instrucción de Ricardo (2026-09-28), a propósito del ritmo de aprobación de generales ([[task-165]] punto 5): «eso no se registra acá, eso es operativo (lo operativo del ritmo no lo registramos nosotros)». Preguntó dónde guardar esa instrucción para que no se vuelva a abrir. Es la misma línea que ya dio el 23 de septiembre sobre las fechas límite por sección («eso no nos corresponde, no guardar nada», [[task-175]]).

En un proyecto con cliente no hay feedback local (documenter §5): la regla vive en el harness del proyecto y aterriza con el ok de Ricardo. Propuesta de línea para el `CLAUDE.md` del monorepo, sección «Domain and language conventions»:

> **Operational matters between Rubén and the IES** (review pace, per-section deadlines, reminders) are his, happen outside the platform and are not recorded in the graph; the graph records only what the platform stores or decides.

## Criterios de aceptación

- [x] Ricardo aprobó la línea (o su redacción) y el coordinador la escribió en el CLAUDE.md del monorepo — 2026-09-28: aprobó una versión más breve, escrita en «Domain and language conventions»: «Operational matters between Rubén and the IES (review pace, per-section deadlines) stay outside the platform and are not recorded in the graph.»
