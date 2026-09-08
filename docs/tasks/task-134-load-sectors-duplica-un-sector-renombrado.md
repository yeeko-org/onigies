---
type: task
id: task-134
title: load_sectors duplica un sector renombrado desde el dashboard
state: open
date: 2026-09-07
owner: ai
parent: "[[task-2]]"
source: ["[[2026-09-07-rediseno-edicion-observables-pesos-y-nomenclatura]]"]
---

# load_sectors duplica un sector renombrado desde el dashboard

`api/indicator/management/commands/load_sectors.py` hace `update_or_create` con llave `name`, y `Sector.name` es editable desde el dashboard (catálogo autogenerado, todo escribible) y no es único. Renombrar un sector desde el dashboard hace que el siguiente deploy inserte una fila nueva con el nombre viejo: `ReachQuestion.others_sectors` y la captura apuntan a la nueva, mientras `Survey.sectors`, `ReachResponse.sectors` y `PopulationQuantity.sector` siguen en la renombrada. Silencioso hasta que los totales de población no cuadran. Mismo patrón (llave natural editable) en `AOption.value` (riesgo bajo: una fila duplicada en la escala) y en `Axis.order` y `Component.name`, donde el riesgo es mayor: `load_questionnaire` no encuentra el componente renombrado, lo crea de nuevo y bajo él crea observables y preguntas nuevos, dejando los originales con sus respuestas huérfanos bajo el renombrado. Desde el 2026-09-08 `load_questionnaire` aborta antes de escribir si algún componente del seed no existe bajo su eje (`_validate_hierarchy_keys`). Test propuesto, no escrito: renombrar un `Component` y comprobar que el seed aborta con `CommandError` sin crear filas. `load_sectors` sigue sin ese pre-flight.

## Criterios de aceptación

- [ ] El seed de sectores usa una llave que el dashboard no puede editar, o `name` deja de ser escribible
- [ ] Test que muerde: renombrar y re-sembrar no crea una fila nueva
