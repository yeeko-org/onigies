---
type: task
id: task-66
title: "Ajustar el input de la tabla de poblaciones: tamaño y alineación"
state: open
date: 2026-08-06
owner: ai
parent: "[[task-41]]"
source: ["[[2026-08-06-temas-reunion-fer]]"]
---

# Ajustar el input de la tabla de poblaciones: tamaño y alineación

§5 de la reunión con Fernanda, `[11:21]`–`[12:15]`. En la tabla de hombres y mujeres de los datos básicos, el input es demasiado grande y no queda centrado respecto al título de la columna de arriba.

Superficie: `nuxt/app/components/dashboard/survey/GeneralNumberInput.vue` y `GeneralNumberFields.vue` / `GeneralPopulations.vue`, en el mismo directorio. El modelo de datos de esta sección está descrito en el skill `gen-general-info`.

## Criterios de aceptación

- [ ] El input de cada celda queda alineado con el encabezado de su columna
- [ ] El ancho del input es proporcionado al dato que recibe
