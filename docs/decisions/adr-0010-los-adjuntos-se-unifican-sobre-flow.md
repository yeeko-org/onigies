---
type: decision
id: adr-0010
title: Los adjuntos se unifican sobre flow.Attachment y BP migra al mismo stack
state: accepted
date: 2026-08-06
origin: ricardo
deliberation: dialogued
rationale: recorded
source: ["[[2026-08-06-sesion-duo-adjuntos-sobre-flow-y]]"]
affects: ["api/flow/attachment_views.py", "api/flow/registry.py", "api/flow/permissions.py", "nuxt/app/components/dashboard/flow/FlowAttachments.vue"]
related: ["[[task-68]]", "[[task-7]]"]
---

# Los adjuntos se unifican sobre flow.Attachment y BP migra al mismo stack

## Contexto y planteamiento del problema

[[task-68]] pedía evidencia probatoria en las preguntas base «idéntica a los archivos de Buenas Prácticas, sobre flow». Al investigar se descubrió que la premisa estaba invertida: BP corría sobre el modelo viejo `example.Evidence` (la única subida de archivos viva del sistema) y `flow.Attachment` era un modelo sin API ni frontend. A la vez, [[task-7]] planeaba borrar los tres modelos viejos de adjuntos con una razón escrita pero nunca argumentada (una línea del diseño del motor, [[2026-06-05-diseno-del-motor-de-flujo]]: consolidación de tres modelos con FK dedicada en uno genérico).

## Criterios de decisión

- Un solo mecanismo de adjuntos para todo el sistema, coherente con la consolidación que ya hizo `FlowEvent` con los comentarios.
- No dejar funcionalidad viva (BP) colgando de modelos destinados al borrado.
- Permisos correctos desde el estreno: el viejo `EvidenceViewSet` permitía a cualquier autenticado borrar evidencias ajenas.

## Opciones consideradas

- **(a)** Estrenar flow.Attachment solo en gen/cp y dejar BP sobre `Evidence` hasta una migración futura, acotando el borrado de [[task-7]].
- **(b)** Migrar también BP al stack nuevo en la misma obra, dejando [[task-7]] íntegra.

## Resultado

Ricardo eligió **(b)**. Decisiones de diseño que la acompañan, todas suyas: los adjuntos se anclan **al objeto** (GenericFK `target`; `event` queda null, nunca cuelgan del timeline); los niveles son `GroupResponse` (cp) y `GeneralGroupResponse` (gen) — `Observable` jamás lleva adjuntos directos —; en BP siguen siendo `GoodPractice` y `FeatureGoodPractice`; el backend es genérico para todos los targets y la UI de cp espera a su superficie de captura ([[task-92]]).

### Consecuencias

- **Bueno:** un solo stack (endpoint genérico + `FlowAttachments.vue`); el borrado de [[task-7]] queda destrabado, incluidos `Evidence`, `ActionFileMixin`/`add_file`, `EvidenceViewSet` y `mainStore.saveFile`; el hueco de permisos quedó cerrado (escritura solo de la IES dueña en turno editable, revisión solo lectura, DELETE acotado al target).
- **Malo:** `evidences` sigue viajando como payload muerto en los serializers de BP hasta [[task-7]]; en producción hay que re-correr `migrate_flow_data` en el deploy (siguió entrando evidencia al modelo viejo hasta este cambio) y contar las `Evidence` huérfanas, que la migración no copia.

### Cómo se comprueba

`grep -rn "add_file\|/evidence/\|Evidences" nuxt/app` solo devuelve el action muerto `saveFile`; `verify_flow_data` reporta la sección de adjuntos `[ok]`; los tests de regresión propuestos viven en [[task-94]]. (La evidencia fue válida en su momento: el re-run comprometido aquí se ejecutó el 2026-08-12 y cerró 661 = 661, pero ese mismo re-run causó el incidente de estatus de [[2026-08-12-incidente-migrate-flow-data]], tras el cual `migrate_flow_data` y `verify_flow_data` se retiraron del repo.)

## Más información

Bitácora: [[2026-08-06-sesion-duo-adjuntos-sobre-flow-y]]. La reconstrucción de la historia del borrado quedó también en [[task-7]].
