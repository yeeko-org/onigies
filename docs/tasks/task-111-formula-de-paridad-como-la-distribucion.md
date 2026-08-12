---
type: task
id: task-111
title: "Fórmula de paridad: cómo la distribución por sexo y género produce el valor del 1.7"
state: open
date: 2026-08-11
owner: ricardo
parent: "[[task-5]]"
source: ["[[2026-08-11-reunion-con-ruben-sobre-la-informacion-base]]"]
related: ["[[task-110]]", "[[task-28]]", "[[adr-0004]]"]
---

# Fórmula de paridad: cómo la distribución por sexo y género produce el valor del 1.7

Rubén reconoció en la reunión del 11 de agosto, `[22:23]`, que falta construir una fórmula para medir, en términos de paridad, qué tan cerca está la distribución por sexo y género de un reparto equitativo. Ricardo matizó que la existencia del indicador no cambia la realidad del registro, solo la mide.

Importa ahora porque la composición se captura en generales por [[adr-0004]] y puntúa el observable 1.7 a través de su ponderación de población: el dato entra, pero no hay regla escrita que lo convierta en valor.

Con una tercera columna ([[task-110]]) el problema deja de ser trivial: el reparto mitad y mitad deja de ser el óptimo evidente y hay que decidir contra qué se mide la distancia.

Es hermana de [[task-27]], [[task-28]] y [[task-29]] — la misma familia de definiciones metodológicas que espera una sesión dedicada con Rubén.

## Criterios de aceptación

- [ ] Rubén y Ricardo definieron la fórmula de paridad del observable 1.7
- [ ] La fórmula dice qué hacer con la población no binaria y con los sectores sin dato
- [ ] La definición quedó escrita antes de implementarse
