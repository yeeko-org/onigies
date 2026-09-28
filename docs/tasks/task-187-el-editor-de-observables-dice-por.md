---
type: task
id: task-187
title: El editor de observables dice por qué no se pudo eliminar una pregunta
state: open
date: 2026-09-28
owner: ai
related: ["[[task-178]]"]
---

# El editor de observables dice por qué no se pudo eliminar una pregunta

Propuesta salida de [[task-178]] el 2026-09-28, sin respuesta de Ricardo. Cuando el dashboard intenta borrar una pregunta con respuestas, el API responde 400 con `report_data` (la lista de modelos dependientes, vía `CustomDeleteMixin.destroy`) y, si el borrado llegara a ejecutarse, 409 con `detail` (manejador global). El editor `nuxt/app/components/dashboard/indicator/observable/ObservableEditSimple.vue` muestra en ambos casos el genérico `DELETE_QUESTION_ERROR` («No se pudo eliminar la pregunta.») sin decir el motivo. Con IES capturando, quien edita el instrumento necesita saber que el bloqueo es por respuestas existentes y no por un fallo.

## Criterios de aceptación

- [ ] Propuesta a Ricardo del texto: qué dice el snackbar cuando el 400 trae respuestas en `report_data` y cuando llega un 409 con `detail`
- [ ] Implementado con su ok, sin cambiar el contrato del API
