---
type: task
id: task-160
title: Unificar las tres redacciones de la salida «planeación general» de las preguntas de alcance
state: open
date: 2026-09-22
owner: ricardo
parent: "[[task-2]]"
---

# Unificar las tres redacciones de la salida «planeación general» de las preguntas de alcance

La opción `has_general_planning` de `ReachQuestion` tiene tres redacciones en el repo: en el maquetado y en la exportación a Word, «Planeación general sin focalizar un sector específico» (la que las IES vieron; hoy constante en `api/question/export/texts.py`); en el editor del dashboard, `ReachSectorFields.vue`, «Ofrece la salida «cubierto por la planeación general»»; y en `answer.ReachResponse.not_focalized`, el `verbose_name` «No focalizado en sectores específicos». La redacción es de Rubén; una vez decidida, propuesta: guardarla en un solo lugar (por ejemplo en `QuestionType` o en la propia `ReachQuestion`) y que el Word, el editor y la captura la lean de ahí. Surgió el 2026-09-22 en [[task-150]]; está en la lista de lo que Rubén revisa.

## Criterios de aceptación

- [ ] Rubén fijó la redacción
- [ ] Una sola fuente para las tres superficies
