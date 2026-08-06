---
type: task
id: task-88
title: Cambiar «existen» por «se atiende» en la redacción de las preguntas
state: open
date: 2026-08-06
owner: ai
parent: "[[task-2]]"
source: ["[[2026-08-06-temas-reunion-fer]]"]
related: ["[[task-50]]"]
---

# Cambiar «existen» por «se atiende» en la redacción de las preguntas

§6 de la reunión con Fernanda, `[12:17]`–`[13:07]`. Ricardo señaló que en una de las preguntas la palabra **«existen»** no es la mejor redacción; entre ambos surgieron alternativas: «se atiende», «es parte de», «está presente».

**Decisión de Ricardo (2026-08-06): implementar ya «Se atiende».** Anotación suya en la misma respuesta: **igual hay que corroborarlo con Rubén**, porque en la llamada él mismo lo marcó como tema metodológico. O sea: se implementa sin esperar, pero la validación sigue debiendo — si Rubén prefiere otra redacción, se cambia.

El texto vive en el seed del cuestionario (`api/question/seed_data/`, ver skill `cp-questionnaire`) y llega a la base con `load_questionnaire`. La revisión completa pregunta por pregunta que hará Rubí con su equipo es [[task-50]]; este cambio no la espera, pero es un buen ejemplo del tipo de hallazgo que ella va a producir.

## Criterios de aceptación

- [ ] La pregunta usa «Se atiende» en lugar de «existen»
- [ ] El cambio quedó en el seed y en la base, no solo en un lado
- [ ] Rubén corroboró la redacción, o quedó anotado que sigue pendiente
