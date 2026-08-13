---
type: task
id: task-124
title: "Mapa completo del proceso de comentarios: quién ve qué y cuándo"
state: open
date: 2026-08-12
owner: ai
parent: "[[task-99]]"
source: ["[[2026-08-12-deploy-gen-a-produccion-migraciones-seeds]]"]
related: ["[[task-69]]", "[[task-70]]", "[[task-71]]", "[[task-44]]", "[[task-97]]", "[[task-30]]"]
---

# Mapa completo del proceso de comentarios: quién ve qué y cuándo

Encargo textual de Ricardo (2026-08-12): «identificar con calma todo el proceso de los comentarios, quién puede ver qué, en qué momento se propagan y ya sin la parte de FlowEvent [espejado], qué pasa si alguien quiere editar un comentario y aún no se envía el agrupador, entre otros temas que esta conversación ahora está abriendo».

Lo detonó el incidente del 2026-08-12: el re-run de `migrate_flow_data` en producción, además de aplastar estatus de flujo (ya restaurados quirúrgicamente), espejó al timeline de `FlowEvent` los comentarios privados de revisora del `TextField` `comments` — que la IES puede leer, porque `FlowEventView.get` solo comprueba propiedad del objeto y no filtra por rol. Los comandos `migrate_flow_data`/`verify_flow_data` ya se retiraron del repo y los 11 eventos espejados en producción se borran con aprobación de Ricardo. El record del incidente queda por escribirse ese mismo día; el deploy que lo originó está en [[2026-08-12-deploy-gen-a-produccion-migraciones-seeds]].

Esta task **no es de arreglo**: es el mapa previo. Es diagnóstico y diálogo con Ricardo; de ella deberían salir las decisiones (ADR) y, si hace falta, tasks de implementación. Es hermana de [[task-69]] (unificación visual), [[task-70]] (editar/borrar los propios) y [[task-71]] (editar y mover desde el admin), y las precede: no se puede unificar ni abrir la edición sin saber antes quién ve qué.

## Qué hay que levantar

**1. Los dos mecanismos de comentario, que hoy coexisten y no son lo mismo.**

- **Timeline de flujo** (`FlowEvent`): comentarios puros (`POST events/`) y comentarios asociados a una transición. Son **compartidos**: los ve cualquiera con acceso al objeto, IES incluida. Viven en tres niveles — envío/paquete, buena práctica y criterio ([[task-69]]).
- **`TextField` `comments`, privado de revisora**, en `FeatureGoodPractice`, `GoodPractice` y `GoodPracticePackage`. Es parte de la calificación y **sigue vivo en la UI de calificación**: se oculta por `v-if="isStaff"` y se recorta en el payload con `hide_review_fields` (skill `bp-validation-ux`). Nunca fue pensado para llegar al timeline; el comando que lo espejaba ya no existe.

Hay que dejar escrito, con precisión, qué se captura en cuál, desde qué pantalla y con qué destinatario.

**2. Quién ve qué, por rol.** Matriz explícita IES / revisora / staff-admin, por mecanismo y por nivel. Incluye el hueco detectado: `FlowEventView.get` no filtra nada por rol — si algún día vuelve a entrar contenido privado al timeline, la IES lo lee. ¿Basta con no volver a espejar, o el timeline debería tener un concepto propio de visibilidad (evento interno vs. compartido)?

**3. Cuándo se puede comentar, y cómo se propaga.** El guard vigente en `FlowEventView.post` es «solo comenta quien tiene el turno»: el rol del usuario debe coincidir con el `role` del status actual. Frente a eso, [[task-44]] documenta que en el frontend el bloqueo no baja a hijos y nietos, y que el alcance se amplió a los tres flujos (`cp`, `gen`, `bp`). Hay que contrastar el guard del backend contra lo que la UI permite y contra la propagación de estatus hacia abajo (skill `flow`): un comentario a nivel de criterio no cambia de dueño cuando el paquete cambia de turno, pero su editabilidad sí debería.

**4. Edición y borrado antes de enviar el agrupador.** Pregunta abierta de Ricardo: qué pasa con un comentario cuyo agrupador (paquete/envío) aún no se envía. La regla que él enunció en [[task-70]] —se edita y se borra mientras el envío siga de tu lado— cubre el caso, pero falta resolver la mecánica: si el comentario ya está en el timeline y es visible para la contraparte antes del envío, la regla del turno no alcanza; si solo se vuelve visible al enviar, entonces el timeline necesita un estado «borrador». Decidirlo aquí, no en [[task-70]], que implementa.

**5. La pregunta que abre el fin del espejado.** Sin el comando, el `TextField` privado **ya nunca llegará al timeline**. ¿Está bien así? Es decir: ¿el comentario de calificación debe quedarse privado para siempre, o hay un momento del flujo —típicamente al devolver el envío a la IES con «requiere ajustes»— en el que la revisora debería poder publicarlo deliberadamente? Hoy no hay ningún puente, ni manual ni automático. Ligado a [[task-30]] (¿comentario obligatorio al marcar «atendido»?).

**6. Qué queda del histórico.** [[task-97]] (resurrección de comentarios legacy en el re-run) probablemente queda sin objeto al retirarse `migrate_flow_data`, pero **no se cierra desde aquí**: se relaciona y se decide en su lugar. Sí hay que verificar qué comentarios legacy (`ObservableComment`, `GroupComment`, `GeneralGroupComment`) quedaron como eventos y si alguno era privado.

## Salidas esperadas

Una `reference` con el mapa (mecanismos, matriz de visibilidad, reglas de turno y edición), más las decisiones que se tomen como `decision`. Las tasks de implementación que surjan cuelgan de [[task-99]].

## Criterios de aceptación

- [ ] Está escrito en reference/ el mapa de los dos mecanismos de comentario, con qué se captura en cada uno y desde qué pantalla
- [ ] Existe una matriz explícita de quién ve qué (IES / revisora / staff) por mecanismo y por nivel, contrastada contra el código
- [ ] Está documentado el guard de turno de FlowEventView.post y su contraste con lo que permite la UI en cada nivel
- [ ] Ricardo decidió qué pasa con un comentario cuyo agrupador aún no se envía (editable, borrable, visible o no)
- [ ] Ricardo decidió si el TextField privado de calificación debe seguir sin ningún puente al timeline, o si necesita uno deliberado
- [ ] Está verificado si FlowEventView.get necesita filtro por rol, o si basta con no volver a inyectar contenido privado
- [ ] Quedó revisado el destino de [[task-97]] a la luz del retiro de migrate_flow_data (decidido en su lugar, no aquí)
