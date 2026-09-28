---
type: task
id: task-184
title: Quitar un tipo de pregunta a un observable desde el dashboard deja huérfano el GroupResponse de cada IES
state: open
date: 2026-09-28
owner: ai
related: ["[[task-178]]"]
---

# Quitar un tipo de pregunta a un observable desde el dashboard deja huérfano el GroupResponse de cada IES

Hallazgo colateral de [[task-178]] (2026-09-28), al poner en `PROTECT` las FKs de respuestas hacia el instrumento. Es preexistente: el cambio de hoy no lo introduce ni lo corrige.

**Qué pasa.** `removeType` (`nuxt/app/components/dashboard/indicator/observable/ObservableEditSimple.vue`, l. 441) borra la fila puente `ObservableQuestionType` (`api/question/models.py`, l. 81). Pero `GroupResponse.question_type` (`api/answer/models.py`, l. 65) apunta a `QuestionType`, no a la fila puente: el `GroupResponse` de cada IES para ese tipo, con sus respuestas tipadas, sigue existiendo sin que ningún tipo activo del observable lo referencie. Ni la cascada lo arrastra (la puente no es su padre) ni `PROTECT` lo bloquea (el `QuestionType` no se borra). El borrado de la puente solo es posible con el cuestionario abierto (`QuestionnaireSettings.content_open`).

**Qué hay que decidir.** Si la fila puente debe quedar protegida cuando existe algún `GroupResponse` con captura para ese (observable, tipo), o si el huérfano se conserva a propósito —por si el tipo vuelve— y se oculta del cálculo y de las pantallas. Antes de decidir, contar los huérfanos que ya existan en producción.

## Criterios de aceptación

- [ ] Contados en producción los GroupResponse cuyo (observable, question_type) no tiene fila ObservableQuestionType, distinguiendo los que tienen respuestas tipadas
- [ ] Decidido si la fila puente se protege cuando hay captura o si el huérfano se conserva y se oculta
- [ ] Aplicado lo decidido, y los huérfanos existentes resueltos en consecuencia
