---
type: task
id: task-15
title: Conseguir los pesos reales por observable
state: open
date: 2026-08-03
owner: ricardo
parent: "[[task-2]]"
source: ["[[2026-07-04-seed-del-cuestionario]]"]
---

# Conseguir los pesos reales por observable

Bloqueado: el cliente no ha entregado la fuente de ponderaciones. Mientras tanto los pesos quedan en `null` y aplica el fallback a `QuestionType.default_weight` (a=60, b=40), lo que significa que cualquier índice calculado hoy es provisional.

## Criterios de aceptación

- [ ] Los pesos están sembrados desde una fuente entregada por el cliente, o se documenta que el fallback es la decisión definitiva
