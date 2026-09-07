---
type: task
id: task-19
title: Integrar el cuestionario actualizado de Rubén
state: closed
date: 2026-08-03
owner: ai
parent: "[[task-2]]"
source: ["[[2026-06-26-seguimiento-pendientes-ruben]]"]
---

# Integrar el cuestionario actualizado de Rubén

Acuerdo §6 de la reunión de junio: Rubén entregaría una versión actualizada del cuestionario. Integrarla significa actualizar [[cuestionario-2026-reducido]], propagar a `question/seed_data/` y re-correr `load_questionnaire`.

## Cierre (2026-09-07): la integración resultó vacua

La versión final llegó maquetada el 2026-09-07 y el cotejo ([[2026-09-07-cotejo-del-instrumento-maquetado]]) demostró que es textualmente equivalente al original de julio: misma estructura de 61 secciones, ninguna pregunta ni opción nueva y solo dos diferencias de forma. No hay nada que integrar —el reducido, el seed y la base ya dicen lo que dice la versión final—, así que la task se cierra sin trabajo: `load_questionnaire` no tiene nada que propagar.

## Criterios de aceptación

- [x] La versión de Rubén está integrada al instrumento reducido y al seed — por equivalencia textual, no por integración de cambios ([[2026-09-07-cotejo-del-instrumento-maquetado]])
