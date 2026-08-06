---
type: task
id: task-68
title: Evidencia probatoria en las preguntas base e iniciales
state: open
date: 2026-08-06
owner: ai
source: ["[[2026-08-06-temas-reunion-fer]]"]
related: ["[[task-41]]", "[[task-7]]"]
---

# Evidencia probatoria en las preguntas base e iniciales

§9 de la reunión con Fernanda, `[14:14]`–`[15:49]`. Ricardo notó que no aparecen los adjuntos en la vista revisada. Fernanda no recordaba que se pidieran archivos probatorios; **Ricardo confirmó que sí se necesitan y que fue un acuerdo con Rubí**, de la nueva actualización del instrumento.

**Alcance definido por Ricardo (2026-08-06):** la obligatoriedad de adjuntar evidencia debería ser **por cada `GeneralGroup` y también por cada `Observable`**. Anotación suya: *corroborar en su momento si es a ese nivel que se sube la evidencia* — el nivel de granularidad es la parte que falta confirmar, no la existencia del requisito.

Esto resuelve la duda que Fernanda planteó en la llamada sobre si la obligatoriedad dependía del año o de la versión del instrumento: se ancla al grupo y al observable, no a la versión.

Dos piezas: hacer visible el adjunto en la interfaz de revisión (hoy no aparece) y agregar la función de adjuntar en la captura de las preguntas base e iniciales. Modelos involucrados: `GeneralGroup` en `api/survey/` (ver skill `gen-general-info`) y `Observable` en `api/question/models.py` (ver skill `cp-questionnaire`).

**Ojo con [[task-7]]:** esa task planifica borrar `GroupAttachment`, `GeneralGroupAttachment` y `Evidence`. Hay que revisar si esta funcionalidad se construye sobre el mecanismo nuevo de `flow` (como ya ocurre con los archivos de las buenas prácticas) o si el borrado planeado deja un hueco. La duda quedó anotada también en [[task-7]].

## Criterios de aceptación

- [ ] La IES puede adjuntar evidencia en las preguntas base e iniciales
- [ ] Está confirmado si el adjunto se sube por `GeneralGroup` y por `Observable`, o a otro nivel
- [ ] La revisora ve los adjuntos en la vista de revisión
- [ ] La relación con el borrado planeado en [[task-7]] quedó resuelta
