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

**Corrección de Ricardo (2026-08-06, sesión duo):** había confundido los nombres. Los niveles correctos son `GroupResponse` (cp, lo que guardaba `GroupAttachment`) y `GeneralGroupResponse` (gen, lo que guardaba `GeneralGroupAttachment`); **`Observable` nunca lleva adjuntos directos**. Coincide exactamente con los modelos viejos y con las ramas de `resolve_upload_path`.

Esto resuelve la duda que Fernanda planteó en la llamada sobre si la obligatoriedad dependía del año o de la versión del instrumento: se ancla al grupo, no a la versión.

## Construido (2026-08-06)

La sesión duo ([[2026-08-06-sesion-duo-adjuntos-sobre-flow-y]], [[adr-0010]]) estrenó el stack sobre `flow.Attachment`: endpoints genéricos en `api/flow/attachment_views.py`, `FlowAttachments.vue` montado en `GeneralGroupPanel` (captura IES y vista revisora a la vez) y en las superficies de BP, que migraron del modelo viejo `Evidence` al mismo mecanismo. El backend ya sirve también a cp; su UI espera a la superficie de captura ([[task-92]]).

**Fuera de este alcance, deliberado:** la *obligatoriedad* (bloquear el envío si falta evidencia) es un requisito distinto de la *capacidad* de adjuntar y no está pedida en ninguna task; si se confirma con Rubí, abrir task propia. La confirmación de granularidad se sumó a [[task-57]].

## Criterios de aceptación

- [x] La IES puede adjuntar evidencia en las preguntas base e iniciales
- [ ] Está confirmado con Rubí el nivel del adjunto (por grupo de preguntas; hoy `GeneralGroupResponse`/`GroupResponse`) — pregunta sumada a [[task-57]]
- [x] La revisora ve los adjuntos en la vista de revisión
- [x] La relación con el borrado planeado en [[task-7]] quedó resuelta ([[adr-0010]]: BP migró, el borrado completo procede)
