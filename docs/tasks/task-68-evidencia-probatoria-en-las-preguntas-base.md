---
type: task
id: task-68
title: Evidencia probatoria en las preguntas base e iniciales
state: closed
date: 2026-08-06
owner: ai
parent: "[[task-41]]"
source: ["[[2026-08-06-temas-reunion-fer]]"]
related: ["[[task-7]]", "[[adr-0010]]", "[[adr-0011]]"]
---

# Evidencia probatoria en las preguntas base e iniciales

§9 de la reunión con Fernanda, `[14:14]`–`[15:49]`. Ricardo notó que no aparecen los adjuntos en la vista revisada. Fernanda no recordaba que se pidieran archivos probatorios; **Ricardo confirmó que sí se necesitan y que fue un acuerdo con Rubí**, de la nueva actualización del instrumento.

**Alcance definido por Ricardo (2026-08-06):** la obligatoriedad de adjuntar evidencia debería ser **por cada `GeneralGroup` y también por cada `Observable`**. Anotación suya: *corroborar en su momento si es a ese nivel que se sube la evidencia* — el nivel de granularidad es la parte que falta confirmar, no la existencia del requisito.

**Corrección de Ricardo (2026-08-06, sesión duo):** había confundido los nombres. Los niveles correctos son `GroupResponse` (cp, lo que guardaba `GroupAttachment`) y `GeneralGroupResponse` (gen, lo que guardaba `GeneralGroupAttachment`); **`Observable` nunca lleva adjuntos directos**. Coincide exactamente con los modelos viejos y con las ramas de `resolve_upload_path`.

Esto resuelve la duda que Fernanda planteó en la llamada sobre si la obligatoriedad dependía del año o de la versión del instrumento: se ancla al grupo, no a la versión.

## Construido (2026-08-06)

La sesión duo ([[2026-08-06-sesion-duo-adjuntos-sobre-flow-y]], [[adr-0010]]) estrenó el stack sobre `flow.Attachment`: endpoints genéricos en `api/flow/attachment_views.py`, `FlowAttachments.vue` montado en `GeneralGroupPanel` (captura IES y vista revisora a la vez) y en las superficies de BP, que migraron del modelo viejo `Evidence` al mismo mecanismo. El backend ya sirve también a cp; su UI espera a la superficie de captura ([[task-92]]).

**Fuera de este alcance, deliberado:** la *obligatoriedad* (bloquear el envío si falta evidencia) es un requisito distinto de la *capacidad* de adjuntar y no está pedida en ninguna task; si se confirma con Rubí, abrir task propia. La confirmación de granularidad se sumó a [[task-57]].

## Cierre (2026-08-11)

La reunión con Rubén del 11 de agosto ([[2026-08-11-reunion-con-ruben-sobre-la-informacion-base]]) resolvió las dos piezas que faltaban, y en direcciones distintas.

**El nivel quedó confirmado tal como estaba construido:** «la evidencia probatoria aplicará a todo el bloque, no por ítem». Es exactamente el anclaje al `GeneralGroupResponse` que [[adr-0010]] ya había fijado, así que no hay nada que cambiar. Esto responde también el cuarto criterio de [[task-57]].

**La obligatoriedad no va a existir.** Rubén pidió quitar la opcionalidad y Ricardo retiró el rótulo «(opcional)» en el momento, pero decidió el mismo día que no habrá candado técnico: si a la revisión le falta evidencia, el camino es retachar el envío en el proceso de revisión, no impedir a la IES entregar lo que sí tiene. Razonado en [[adr-0011]]. **No se abre la task propia que este cuerpo anticipaba** — el requisito se resolvió en contra.

Con eso la task queda cerrada: lo construido es todo lo que había que construir.

## Criterios de aceptación

- [x] La IES puede adjuntar evidencia en las preguntas base e iniciales
- [x] Está confirmado con Rubí el nivel del adjunto: por grupo de preguntas (`GeneralGroupResponse` en generales, `GroupResponse` en el cuestionario por observable), ratificado en la reunión del 11 de agosto
- [x] La revisora ve los adjuntos en la vista de revisión
- [x] La relación con el borrado planeado en [[task-7]] quedó resuelta ([[adr-0010]]: BP migró, el borrado completo procede)
- [x] Resuelto el carácter obligatorio del adjunto: no lo es ([[adr-0011]])
