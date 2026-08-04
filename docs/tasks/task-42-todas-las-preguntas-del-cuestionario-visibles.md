---
type: task
id: task-42
title: Todas las preguntas del cuestionario visibles y editables en el dashboard
state: open
date: 2026-08-03
owner: ai
parent: "[[task-2]]"
source: ["[[2026-07-28-reunion-flujo-bp-e-informacion-base]]"]
depends-on: ["[[task-14]]"]
---

# Todas las preguntas del cuestionario visibles y editables en el dashboard

Acuerdo explícito de la reunión, con fecha comprometida el **2026-08-03**. `[33:11]` «Eso también puede ser como un acuerdo de hoy, que para el lunes tengamos en el dashboard visible no solo los observables, sino todas las preguntas en producción. En producción, quiero decir, como en la página, en la base de datos, para que me ayudes a validar».

No basta con que estén sembradas: al preguntarle si se trataba solo de la integración, la respuesta fue `[37:32]` «No sólo la integración, sino la visualización para que se puedan editar».

Es la hermana de superficie de [[task-14]]: aquella corre `load_questionnaire` en producción, esta construye la vista del dashboard que lista y permite editar cada pregunta. Sin el seed desplegado no hay nada que mostrar, de ahí la dependencia.

Es además el habilitador de [[task-50]]: Rubí y su equipo hacen la revisión pregunta por pregunta sobre esta misma superficie, corrigiendo ellas los textos.

## Criterios de aceptación

- [ ] El dashboard lista todas las preguntas, no solo los ejes, componentes y observables
- [ ] Cada pregunta se puede editar desde el dashboard
- [ ] Está desplegado en producción, no solo en local
