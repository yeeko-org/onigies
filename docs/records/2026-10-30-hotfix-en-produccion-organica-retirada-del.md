---
type: record
id: 2026-10-30-hotfix-en-produccion-organica-retirada-del
title: "Hotfix en producción: orgánica retirada del 1.12"
date: 2026-10-30
---

# Hotfix en producción: orgánica retirada del 1.12

## Qué pasaba

El observable 1.12 (Planes y programas de estudio con perspectiva de género) tenía fila de aplicabilidad `ObservableQuestionType` para `b_questions` («Transversalidad orgánica») sin ninguna `BQuestion` (desajuste conocido desde [[task-135]]; Rubén iba a agregar la pregunta desde el dashboard y nunca ocurrió; el 2026-09-23 dijo que «no aplica transversalidad orgánica ahí», [[task-173]]). La sección se pintaba porque existía el `GroupResponse`, que nace en `cp_pre_start` y solo pasa a `cp_filling` con el primer guardado; sin preguntas no hay nada que guardar, así que el grupo nunca salía de `cp_pre_start` y la regla de hijos del flow (`valid_child_statuses` de `cp_completed`, `cp_postponed`, `cp_partial`) impedía completar el observable y, por tanto, enviar el eje 1. La validación de contenido no bloqueaba: con cero preguntas devuelve sin errores.

## Estado previo (sondeo 2026-10-30)

- 67 grupos de orgánica del 1.12, todos en `cp_pre_start`; 6 IES ya habían contestado «Sí» (observable en `cp_filling`) y estaban atoradas.
- 0 `BResponse`. Instrumento abierto (`content_open=True`).
- La UABCS había subido el 2026-10-29 un PDF (adjunto 1472) y el comentario «No da opción para responder» (evento 2217) en ese grupo vacío.

## Qué se hizo

Decisión de Ricardo (alternativa descartada: poner los grupos en `cp_approved` como `population`, que dejaba la sección vacía visible con chip «Aprobado»).

1. Dump `pg_dump -Fc` desde el servidor (RDS 15, pg_dump 16): `~/databases/onigies-20261030-1922-pre-fix-1-12.dump` (copia en la carpeta `_backups` del API en el servidor).
2. En una transacción vía `manage.py shell`: adjunto 1472 y evento 2217 reasignados (`object_id`) al grupo de planes de la misma `ObservableResponse` (grupo 9218, UABCS); borrados los 67 `GroupResponse` de orgánica del 1.12 y la fila puente `(1.12, b_questions)`.
3. Sondeo post: puente del 1.12 = `a_questions`, `plans`; 0 grupos B; 67 grupos A y 67 de planes; adjunto y comentario vivos en el grupo 9218.

Nada recrea las filas: el aprovisionamiento (`provision_cp_responses`) lee la fila puente y el seed está retirado ([[adr-0015]]). Sin reload del API. `QuestionType.b_questions.required=True` se queda: solo lo leen el editor (mostrará orgánica como casilla de solo lectura, desmarcada, en 1.12) y el seed.

## Lo que deja abierto

- [[task-173]] (b): el rediseño donde «Planes de estudio» pasa a ser transversalidad curricular, para que todo observable tenga al menos una sección de transversalidad. Pendiente de sesión con calma.
- [[task-184]]: este caso es el precedente de puente borrado con grupos huérfanos; aquí se borraron ambos a mano.
- Si Rubén crea una `BQuestion` en 1.12 desde el dashboard mientras el instrumento esté abierto, la fila puente vuelve (`ObservableQuestionSerializer.create`), pero los grupos no se reaprovisionan solos.
