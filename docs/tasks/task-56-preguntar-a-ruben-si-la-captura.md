---
type: task
id: task-56
title: Preguntar a Rubén si la captura de poblaciones requiere el estado «sin dato» (no_apply)
state: open
date: 2026-08-04
owner: ricardo
parent: "[[task-41]]"
---

# Preguntar a Rubén si la captura de poblaciones requiere el estado «sin dato» (no_apply)

Surgió al diseñar la tabla única de poblaciones (existe / hombres / mujeres). El modelo PopulationQuantity tiene no_apply, pero Ricardo está casi seguro de que es redundante con la columna «existe». Importa porque para el observable 1.7 «cero», «sin dato» y «no existe» son tres cosas distintas en los denominadores. La captura de hoy se construye SIN considerar no_apply.

Segunda pregunta, agregada al afinar el grupo de autoridades: ¿existe alguna IES donde falte alguno de los 3 cuerpos de autoridad (máximo cuerpo colegiado, titulares de instancias académicas, titulares de instancias administrativas)? La tabla de autoridades se construyó con las 3 filas fijas y sin escape; si la excepción existe en la realidad, el mecanismo acordado es un checkbox discreto «No aplica» por fila persistido en el `no_apply` que el modelo ya trae (opt-out para excepción rara, a diferencia del opt-in «existe» de poblaciones) — entra después con costo mínimo, sin migración.

## Criterios de aceptación

- [ ] Rubén respondió si «existe pero sin dato» debe ser capturable en poblaciones, distinto de no marcar el sector
- [ ] Rubén respondió si algún cuerpo de autoridad puede no existir en alguna IES
- [ ] Con las respuestas: se agenda el uso de no_apply donde aplique, o se evalúa retirar el campo del modelo
