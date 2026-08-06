---
type: task
id: task-66
title: "Ajustar el input de la tabla de poblaciones: tamaño y alineación"
state: closed
date: 2026-08-06
owner: ai
parent: "[[task-41]]"
source: ["[[2026-08-06-temas-reunion-fer]]"]
---

# Ajustar el input de la tabla de poblaciones: tamaño y alineación

§5 de la reunión con Fernanda, `[11:21]`–`[12:15]`. En la tabla de hombres y mujeres de los datos básicos, el input es demasiado grande y no queda centrado respecto al título de la columna de arriba.

Superficie: `nuxt/app/components/dashboard/survey/GeneralNumberInput.vue` y `GeneralNumberFields.vue` / `GeneralPopulations.vue`, en el mismo directorio. El modelo de datos de esta sección está descrito en el skill `gen-general-info`.

**Resuelto (2026-08-06, sesión duo):** prop opcional `maxWidth` en `GeneralNumberInput` (con `margin-inline-start: auto`, que pega el input al borde derecho de la celda, donde está el encabezado) y `110px` en las celdas Hombres/Mujeres — el mismo ancho que ya reservaba la columna «Total». El valor es ajuste de una línea en `GeneralPopulations.vue` si en la validación visual se prefiere otro.

## Criterios de aceptación

- [x] El input de cada celda queda alineado con el encabezado de su columna
- [x] El ancho del input es proporcionado al dato que recibe
