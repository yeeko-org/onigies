---
type: task
id: task-176
title: Repensar si las respuestas por pregunta del cuestionario principal deben existir de antemano (hoy nacen al primer guardado)
state: open
date: 2026-09-25
owner: ricardo
parent: "[[task-2]]"
related: ["[[adr-0018]]", "[[adr-0020]]", "[[task-163]]", "[[2026-09-25-deploy-del-cuestionario-principal-y-documento-para-ruben]]"]
---

# Repensar si las respuestas por pregunta del cuestionario principal deben existir de antemano (hoy nacen al primer guardado)

Ricardo, la noche del deploy (2026-09-25, 00:30): «no se crean también las respuestas en null? Por qué hasta GroupResponse?» y, tras la explicación: «Después, no hoy, debemos profundizar y repensar eso de las respuestas en null, abre una task, hoy estoy muy cansado».

**Cómo es hoy.** El árbol eager que `provision_cp_responses` crea de antemano (`Institution.save` y el backfill del deploy) termina en `GroupResponse`: por encuesta, 41 `ObservableResponse` y unos 120 `GroupResponse`, todos en «Por iniciar» salvo los grupos sin captura (población), que nacen en «Aprobado» ([[adr-0020]]). Las filas por pregunta (`AResponse`, `BResponse`, alcance, planes, especial) no existen hasta el primer guardado: el PATCH del grupo hace un upsert por (grupo, pregunta) en `GroupResponseSerializer._sync_rows` (`api/api/views/answer/serializers.py`) y nunca borra por omisión, porque la IES captura en varias sesiones.

**Argumentos que se dieron esa noche a favor de dejarlo así.** El grupo es la unidad que carga estatus de flujo y la unidad que la revisora aprueba; por eso existe de antemano. «Sin fila» ya significa «sin responder», y la compuerta de completitud (`completion.errors`, «Falta responder: …») se calcula contra el catálogo de preguntas, no contra filas vacías. Crear 66 × 280 filas A nulas obligaría a distinguir «respondida como null» de «no respondida» y dejaría huecos cada vez que Rubén agregue una pregunta desde el dashboard, que hoy tampoco reprovisiona ([[task-163]] riesgo 2).

**Lo que empuja a repensarlo (la duda de Ricardo, aún sin desarrollar).** Con filas de antemano, cada pregunta tendría identidad y fila desde el inicio: exportes y consultas por pregunta sin joins condicionales, un lugar donde colgar comentarios o evidencia por pregunta, y un conteo de «sin responder» que no dependa de reconstruir el catálogo por observable. También habría que decidir qué pasa con esas filas cuando cambia el instrumento (alta o baja de preguntas con el instrumento abierto).

Es una conversación de diseño con Ricardo, no una implementación; cualquier cambio toca el esquema y el backfill, y por eso es suyo.

## Criterios de aceptación

- [ ] Ricardo y el modelo analizaron juntos ambos caminos con casos concretos (exporte, completitud, cambios del instrumento)
- [ ] Queda escrita la decisión, como ADR si cambia el esquema o como nota en esta task si se deja como está
