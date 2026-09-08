---
type: task
id: task-133
title: load_questionnaire borra opciones y planes sobrantes con cascada a respuestas capturadas
state: open
date: 2026-09-07
owner: ai
parent: "[[task-2]]"
source: ["[[2026-09-07-rediseno-edicion-observables-pesos-y-nomenclatura]]"]
---

# load_questionnaire borra opciones y planes sobrantes con cascada a respuestas capturadas

En `api/question/management/commands/load_questionnaire.py`, al re-correr el seed se borran las filas de `AQuestion` con `order` mayor que el largo de `a_options` y las de `PlanQuestion` sobrantes. `AResponse.question` y `PlanResponse.question` son CASCADE, así que acortar una lista en `seed_data` y correr el deploy borra respuestas capturadas de las IES. Solo imprime un aviso; no hay `--dry-run`, no cuenta respuestas afectadas ni aborta. Las de Generales están protegidas (PROTECT). Comparar con `seed_flow`, que protege el borrado con `FlowEvent`.

## Criterios de aceptación

- [ ] El comando cuenta las respuestas que perdería el borrado y aborta salvo con una bandera explícita
- [ ] Existe un modo de solo lectura que reporta lo que borraría
- [ ] Test de regresión que muerde: una opción sobrante con respuesta no se borra sin la bandera
