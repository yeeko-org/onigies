---
type: task
id: task-111
title: "Fórmula de paridad: cómo la distribución por sexo-género produce el valor del 1.7"
state: open
date: 2026-08-11
owner: ricardo
parent: "[[task-5]]"
source: ["[[2026-08-11-reunion-con-ruben-sobre-la-informacion-base]]"]
related: ["[[task-110]]", "[[task-28]]", "[[adr-0004]]", "[[2026-09-23-reunion-ruben]]"]
---

# Fórmula de paridad: cómo la distribución por sexo-género produce el valor del 1.7

Rubén reconoció en la reunión del 11 de agosto, `[22:23]`, que falta construir una fórmula para medir, en términos de paridad, qué tan cerca está la distribución por sexo-género de un reparto equitativo. Ricardo matizó que la existencia del indicador no cambia la realidad del registro, solo la mide.

Importa ahora porque la composición se captura en generales por [[adr-0004]] y puntúa el observable 1.7 a través de su ponderación de población: el dato entra, pero no hay regla escrita que lo convierta en valor.

Con una tercera columna ([[task-110]]) el problema deja de ser trivial: el reparto mitad y mitad deja de ser el óptimo evidente y hay que decidir contra qué se mide la distancia.

Es hermana de [[task-27]], [[task-28]] y [[task-29]] — la misma familia de definiciones metodológicas que espera una sesión dedicada con Rubén.

## Criterios de aceptación

- [ ] Rubén y Ricardo definieron la fórmula de paridad del observable 1.7
- [ ] La fórmula dice qué hacer con la población no binaria y con los sectores sin dato
- [ ] La definición quedó escrita antes de implementarse

## Reunión con Rubén, 2026-09-23

Fuente: [[2026-09-23-reunion-ruben]]; también en [[task-173]] punto (d). Ricardo lo llamó «el más complicado»: `[48:56]`–`[49:01]`, «¿cuánto vale la ponderación de la distribución de la población? ¿Cómo medir eso?»; `[49:26]`, «es la de integración paritaria. Muy difícil»; `[50:03]`–`[50:05]`, «cómo entra distribución de la población, cómo entra el ponderador. Esa es la gran pregunta». Rubén, `[49:23]`, había preguntado si era la de formación docente.

- Rubén, `[50:12]`: «lo ideal sería tener una regla en la que, si la distribución de la población se encuentra entre 45 y 55, se considere paritaria, y si no… pues no sé si se puede hacer».
- Ricardo, `[50:36]`–`[50:43]`: «¿45 %, o sea, hasta 45 %? Sí se puede. ¿Pero calificarías igual 44 % que 22 % o que 12 %?».
- Rubén, `[50:51]`: «Sí, porque si no tendría que generar un índice de proporcionalidad. Hay unos instrumentos que hizo el Instituto de las Mujeres hace muchos años que se llamaban índices de feminidad; podría ser un índice de paridad. El tema es que tienes que decidir si lo construyes con base en las mujeres o en los hombres».
- Ricardo, `[51:30]`: «si tienes paridad, ¿tienes 0.9, tienes cuánto? Si valiera un punto, si valiera dos puntos, cómo haces cada cosa. Y además, tal vez haya poblaciones que sean más importantes que otras». Rubén, `[51:55]`: «Tienes razón».

Sin decidir: Ricardo, `[49:41]`–`[49:42]`, «no tenemos que definirla ahora».
