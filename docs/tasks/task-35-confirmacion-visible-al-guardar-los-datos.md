---
type: task
id: task-35
title: Confirmación visible al guardar los datos iniciales
state: open
date: 2026-08-03
owner: ai
parent: "[[task-6]]"
source: ["[[2026-04-16-prueba-con-usuarias-reales]]"]
---

# Confirmación visible al guardar los datos iniciales

Hallazgo de la prueba con usuarias: al dar clic en «guardar datos iniciales» no aparece ningún indicativo de que la información se guardó, ni una opción visible para editarla después. El proyecto ya tiene el snackbar global (skill `snackbar`).

## Criterios de aceptación

- [ ] Guardar datos iniciales muestra confirmación
- [ ] Queda visible cómo editarlos

Ojo antes de empezar: la rama `claude/gallant-jemison` (commit `111e7c1`, sin mergear) ya toca `SurveyInitData.vue` con lo que parece ser justamente esta corrección. Revisar esa rama antes de reimplementar.
