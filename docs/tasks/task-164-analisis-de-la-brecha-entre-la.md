---
type: task
id: task-164
title: Análisis de la brecha entre la pregunta inicial de cada observable y sus preguntas A
state: open
date: 2026-09-22
owner: ai
parent: "[[task-2]]"
source: ["[[2026-09-22-cierre-cuestionario-principal-captura-y-borrado]]"]
related: ["[[task-157]]", "[[task-50]]"]
---

# Análisis de la brecha entre la pregunta inicial de cada observable y sus preguntas A

Ricardo lo pidió el 22 de septiembre para una sesión Fable aparte, antes de compartir las preguntas con las IES: «no con la idea de cambiar todo, sino de observar qué puede mejorar y en qué sentido». El disparador fue la observación de que la pregunta inicial («¿La IES cuenta con…?») mide tenencia de una medida, mientras que las opciones A miden grados de armonización e institucionalización que a veces no se corresponden con lo que la inicial prometió (el análisis de «no aplica» del mismo día, sobre el texto real de la base, lo hizo visible en 1.10, 1.14, 1.15, 3.2 y 4.7, donde una IES puede responder «Sí» y marcar solo las opciones que dependen de ella).

Material: los 41 observables con `init_question`, `a_main_question`, `a_main_subtitle` y sus `AQuestion` (280), en la base local restaurada de producción; la skill `cp-questionnaire`. Entregable: un record con la tabla por observable (qué promete la inicial, qué miden las A, dónde se abren) y una lista corta de mejoras propuestas en el sentido que Rubén pueda aceptar, sin rehacer el instrumento. Sin alucinar casos: sobre el texto real.

## Criterios de aceptación

- [ ] Record con la tabla de los 41 observables y las brechas encontradas
- [ ] Lista de mejoras propuestas, ordenadas por impacto, lista para llevar a Rubén
