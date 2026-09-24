---
type: task
id: task-164
title: Análisis de la brecha entre la pregunta inicial de cada observable y sus preguntas A
state: open
date: 2026-09-22
owner: ai
parent: "[[task-2]]"
source: ["[[2026-09-22-cierre-cuestionario-principal-captura-y-borrado]]"]
related: ["[[task-157]]", "[[task-50]]", "[[2026-09-23-reunion-ruben]]", "[[task-175]]"]
---

# Análisis de la brecha entre la pregunta inicial de cada observable y sus preguntas A

Ricardo lo pidió el 22 de septiembre para una sesión Fable aparte, antes de compartir las preguntas con las IES: «no con la idea de cambiar todo, sino de observar qué puede mejorar y en qué sentido». El disparador fue la observación de que la pregunta inicial («¿La IES cuenta con…?») mide tenencia de una medida, mientras que las opciones A miden grados de armonización e institucionalización que a veces no se corresponden con lo que la inicial prometió (el análisis de «no aplica» del mismo día, sobre el texto real de la base, lo hizo visible en 1.10, 1.14, 1.15, 3.2 y 4.7, donde una IES puede responder «Sí» y marcar solo las opciones que dependen de ella).

**Urgencia que dio Ricardo:** antes de que se compartan las preguntas, hoy mismo (22-23 de septiembre).

Material: los 41 observables con `init_question`, `a_main_question`, `a_main_subtitle` y sus `AQuestion` (280), en la base local restaurada de producción; la skill `cp-questionnaire`. Entregable: un record con la tabla por observable (qué promete la inicial, qué miden las A, dónde se abren) y una lista corta de mejoras propuestas en el sentido que Rubén pueda aceptar, sin rehacer el instrumento. Sin alucinar casos: sobre el texto real.

**Ampliación del 23 de septiembre (Ricardo):** el mismo ejercicio de «no aplica» que se hizo con las preguntas iniciales se repite sobre las AQuestion: revisar si existen opciones donde una IES pueda necesitar «No aplica». Mientras tanto la captura cp asume que no hay «No aplica» en las A (radios Sí/No en `YesNoRadio`); si el análisis lo introduce, el control pasa de radio a select en ese momento.

**Entregado el 2026-09-23** en [[2026-09-23-brecha-entre-pregunta-inicial-y-preguntas-a]]: tabla de los 41, siete bloques de mejoras por impacto y constancia de que ninguna A requiere «No aplica» (`YesNoRadio` se queda). Cierre pendiente de la lectura de Ricardo y de qué se lleva a Rubén.

## Criterios de aceptación

- [x] Record con la tabla de los 41 observables y las brechas encontradas
- [x] Lista de mejoras propuestas, ordenadas por impacto, lista para llevar a Rubén
- [x] Lista de AQuestion candidatas a «No aplica», o constancia de que no hay
- [ ] Ricardo le mandó a Rubén la lista de candidatas a «no aplica» en preguntas iniciales (`[32:00]`)
- [ ] Ricardo le mandó a Rubén el análisis de «no aplica» de las 280 A y el documento de la brecha (el 24 de septiembre, `[59:35]`)

## Reunión con Rubén, 2026-09-23

Fuente: [[2026-09-23-reunion-ruben]].

**Lo que Ricardo le contó y prometió mandar.** `[30:51]`–`[31:18]`: pidió a la IA «un análisis de si podría haber alguna pregunta de este tipo, de las de armonización, institucionalización, en la que pueda aplicar el no aplica». `[32:00]`: «te mando la lista de las posibles. […] esta fue la única, la 1.14». `[33:28]`: otro análisis «que ahorita está corriendo», porque «a veces puede ser que […] respondas directamente a esta que no, pero alguna de estas sí aplique […] te lo paso tal cual […] Va a ser otro documento muy breve de observaciones». `[59:35]`–`[1:00:03]`: «te mando esto, que ya está hecho […] dice que en ninguna de las […] 280 preguntas tendría sentido poner el no aplica». `[1:02:34]`–`[1:02:48]`: «Si hay casos específicos donde un no aplica aplica para preguntas de institucionalización, pues igual sí se pueden poner, pero van a ser tres o cuatro máximo, tal vez una o dos». Rubén, `[1:01:14]`–`[1:01:19]`: «¿Eso me lo podrías mandar para checarlo? Y ya con eso, junto con el análisis que vemos ahorita…»; `[1:02:53]`–`[1:02:55]`: «Si quieres, mándamelo, lo checo».

**El 1.6 A5, en vivo, contra el record.** Ricardo, `[1:00:07]`: «Solo… cargos de elección, en la 1.6. Mira, de una vez lo checamos: 1.6, es la 5. Si no tiene cuerpos colegiados…»; Rubén, `[1:00:31]`: «Difícil»; Ricardo, `[1:00:33]`: «O cargos de elección: si es una pregunta que hacemos… cuerpo colegiado máximo sí tienen. Entonces, ¿qué pasa? Esta pregunta sí podría tener el no aplica». Rubén, `[1:01:00]`: «si quieres tú puedes hacer esa consulta»; Ricardo, `[1:01:05]`–`[1:01:10]`: «Ya la hice; por eso te puedo decir este ejemplo: me lo dio en el reporte ahorita la IA». El record [[2026-09-23-brecha-entre-pregunta-inicial-y-preguntas-a]] clasifica el 1.6 A5 como candidata débil que se resuelve como «No», porque la misma A cubre los cuerpos colegiados de máximo nivel, que sí existen. Llamado de Ricardo: P4 abajo.

**Envío:** Ricardo le manda el documento de la brecha a Rubén mañana, 24 de septiembre de 2026 (triage).

**La brecha, dicha por Rubén** ([[task-173]] punto e): Ricardo, `[53:22]`–`[53:36]`, «¿qué pasa si alguien pone que sí y en todas estas pone que no?»; Rubén, `[53:38]`, «sí puede pasar. Es que la realidad siempre va a superar al cuestionario».

## Decisiones pendientes de Ricardo

Del análisis de la brecha, textuales:

- **P1.** Qué bloques de mejora llevar a Rubén: recomendación del agente 1 a 5 como propuesta, 6 (erratas) se corrige sin él, 7 se menciona como agenda de la versión siguiente.
- **P2.** Bloque 3, la que sí bloquea compartir las preguntas: las tres A que piden texto (1.16 A1 y A2, 2.5 A9): editar el texto o abrir un campo de texto en AResponse.
- **P3.** Las diez erratas del bloque 6: corregirlas en el admin local para el próximo deploy o dejárselas a Rubén, que edita ahí.

De la reunión del 23 de septiembre:

- **P4.** El 1.6 A5: ¿«No aplica», como lo leyó Ricardo en vivo (`[1:00:33]`), o candidata débil que se resuelve como «No», como la clasificó el record? Si se habilita, el control de esa A deja de ser `YesNoRadio` (ampliación del 23, arriba).

La task sigue abierta; su cierre espera la lectura de Ricardo.
