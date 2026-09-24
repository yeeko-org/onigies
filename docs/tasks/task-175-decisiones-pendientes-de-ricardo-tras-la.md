---
type: task
id: task-175
title: Decisiones pendientes de Ricardo tras la reunión del 23 de septiembre
state: open
date: 2026-09-23
owner: ricardo
parent: "[[task-2]]"
related: ["[[2026-09-23-reunion-ruben]]", "[[2026-09-23-sesion-meeting-reunion-con-ruben]]", "[[task-163]]", "[[task-164]]", "[[task-153]]", "[[task-157]]", "[[task-174]]", "[[task-169]]", "[[task-173]]"]
---

# Decisiones pendientes de Ricardo tras la reunión del 23 de septiembre

Ricardo se fue antes del cierre de la sesión meeting de la reunión con Rubén del 23 de septiembre ([[2026-09-23-reunion-ruben]], record de sesión [[2026-09-23-sesion-meeting-reunion-con-ruben]]) y pidió: «si hay otras decisiones que debo tomar, guárdalas en alguna tarea y después retomamos la conversación». Esta es esa tarea. Cada entrada trae contexto, opciones numeradas y la recomendación del coordinador; ninguna está aplicada.

## (a) Liberar hoy con el bug de [[task-174]] o arreglarlo antes

Cada grupo cp nace en «Por iniciar». Elegir «En llenado» en el menú «Guardar ▾» con cambios guarda las respuestas y el guardado ya promueve el grupo a «En llenado»; luego el POST de transición `cp_filling → cp_filling` da 400. Resultado: el primer guardado con «En llenado» de cualquier IES mostrará snackbar rojo y alerta roja, aunque las respuestas sí se guardan. Rubén espera el deploy hoy (`[1:25:04]`) para su reunión del viernes 25 ([[task-163]]).

1. Liberar hoy con el bug y arreglarlo después.
2. Aplicar antes la opción 2 de [[task-174]]: omitir el POST de transición cuando el guardado ya dejó el estatus en el destino. Cambio pequeño, solo de frontend (`saveAndTransition` en `CpGroupCard.vue`).

Recomendación del coordinador: opción 2 antes de abrir.

## (b) Campo de «cierre de cp»

Sobre las fechas límite por sección de la reunión (`[35:41]`–`[37:59]`), Ricardo respondió: «Eso no nos corresponde, no guardar nada, con los campos existentes tenemos, si acaso uno para "cierre de cp"». `Period` tiene hoy `submission_deadline`, `gen_submission_deadline` y `cp_open_at` (`api/ies/models.py`); no hay fecha de cierre de cp. Agregarla es cambio de esquema y requiere su ok ([[task-153]]).

1. No abrirlo: los campos existentes bastan.
2. Abrir una task para `cp_submission_deadline` en `Period`.

Recomendación del coordinador: ninguna fuerte; si Rubén no ha pedido cerrar cp en una fecha, la 1 hasta que lo pida.

## (c) Destino de [[task-162]]

[[task-162]] (decidir si la descarga pública del Word se cachea, owner ricardo) quedó colgando de [[task-2]] al cerrar [[task-150]]. Ricardo dijo: «No importa, el exportador de word ya está cerrado, no se harán más cambios». [[task-158]] y [[task-161]] (plan de pruebas acordado el 22 de septiembre) se recolgaron igual de [[task-2]] y se mantienen.

1. Abandonar [[task-162]]: sin cambios al exportador, el cacheo no entra.
2. Mantenerla abierta.

Recomendación del coordinador: abandonarla, por la literalidad de «no se harán más cambios».

## (d) Qué documento revisó Rubén «uno por uno… como en tres horas»

Rubén, `[34:31]`: «Me ayudó mucho el que me mandaste; la verdad, me fui uno por uno y acabé como en tres horas». Hipótesis, no confirmada: es el documento de correcciones de redacción del 4 de septiembre ([[2026-09-04-correcciones-de-redaccion-del-instrumento]]). No es el de la brecha, que Ricardo le manda el 24 de septiembre. Falta decidir a qué task va la línea «Rubén lo revisó y aplicó».

1. Confirmar la hipótesis y anotar la línea en [[task-157]].
2. Es otro documento: Ricardo dice cuál y a qué task va.

Recomendación del coordinador: la 1 si Ricardo lo reconoce; es la lectura más probable.

## (e) Las tres A que piden texto que la plataforma no guarda

1.16 A1 y A2 y 2.5 A9 piden a la IES un texto que la captura no guarda (las A son Sí/No). Es P2 de [[task-164]] y lo único de la brecha que bloquea compartir las preguntas tal cual.

1. Editar el texto de esas tres A para que se respondan con Sí/No.
2. Abrir un campo de texto en `AResponse` (cambio de esquema).

Recomendación del coordinador: la 1, como propone el análisis de la brecha ([[2026-09-23-brecha-entre-pregunta-inicial-y-preguntas-a]], bloque 3: «Un campo de texto en `AResponse` para dos o tres preguntas es más maquinaria que valor; propongo editar el texto»).

## (f) Dónde están las demás

- Brecha: [[task-164]] §Decisiones pendientes de Ricardo, P1–P4.
- Diseño de la captura cp: [[task-169]].
- Metodológicas: [[task-173]].
- [[task-98]]: botón «Enviar a revisión» deshabilitado con la razón a la vista, o activo con un clic que explique por qué no.
- [[task-172]] punto 6: si se toca el tamaño del eje Cuidados.

## Criterios de aceptación

- [ ] (a) Liberar con el bug de [[task-174]] o aplicar antes su opción 2
- [ ] (b) Campo de «cierre de cp»: no abrirlo o abrir task para `cp_submission_deadline`
- [ ] (c) [[task-162]]: abandonarla o mantenerla
- [ ] (d) Documento de las tres horas identificado y su línea anotada en la task que corresponda
- [ ] (e) Las tres A de texto: editar el texto o abrir campo en `AResponse`
