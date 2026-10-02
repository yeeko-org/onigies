---
type: task
id: task-70
title: Editar y borrar los comentarios propios mientras el envío siga de tu lado
state: open
date: 2026-08-06
owner: ai
parent: "[[task-99]]"
source: ["[[2026-08-06-temas-reunion-fer]]", "[[2026-10-02-comentarios-editables-y-valvula-de-admin]]"]
related: ["[[adr-0019]]", "[[task-44]]", "[[task-124]]", "[[task-190]]"]
---

# Editar y borrar los comentarios propios mientras el envío siga de tu lado

§10 de la reunión con Fernanda, `[17:20]`–`[24:33]`. Fernanda pidió un botón para editar comentarios; Ricardo detectó además que hoy no se puede borrar un comentario general ya guardado (lo probó con el COLEF), y propuso que si el envío está en tu turno y son tus últimos comentarios, debería permitirse.

**La regla que enunció Ricardo en la llamada:** se puede editar o borrar un comentario **mientras el envío siga de tu lado**; una vez que la contraparte ya lo vio o empezó a atenderlo, ya no debería poder modificarse. Es la misma noción de turno que gobierna la edición de contenido en el motor (`canEditContent`, skill `flow`).

Aplica a los tres niveles de comentario. El caso que lo motivó: Fernanda metió un comentario general muy largo en la buena práctica equivocada («agenda estadística») cuando debía ir a nivel de envío, y no pudo moverlo ni borrarlo; Ricardo le pidió eliminar el duplicado para que la IES no viera dos y no fue posible desde la interfaz.

## Decisiones del 2026-10-02

Ricardo cerró la regla en diálogo ([[2026-10-02-comentarios-editables-y-valvula-de-admin]]); esto extiende lo de arriba, no lo contradice:

- **El turno lo define la raíz, no el status propio** (como [[adr-0019]] y `canEditContent`). Un comentario de revisión sobre una buena práctica, un grupo gen o un observable es editable mientras el envío, el paquete o el eje (`AxisValue`) siga en rol `reviewer`; se congela cuando la raíz regresa a la IES o termina. Simétrico para la IES mientras la raíz esté en rol `ies`.
- **Ya no son solo los propios:** cada lado edita y borra los comentarios de su lado sin importar quién los escribió («sin importar quién sea la revisora»).
- **Borrar significa borrar solo el comentario:** en un comentario puro (sin cambio de status) se borra la fila del `FlowEvent`; en un comentario de transición se vacía `comment` y el evento de cambio de status se queda.
- **Sin `edited_at` ni migración.** Mientras la raíz siga de tu lado la contraparte aún no ha actuado sobre el comentario; corregirlo es corregir un borrador. El comentario de la transición raíz que disparó el correo a la IES queda congelado por la regla general, porque ese correo sale justo cuando la raíz deja el lado revisor; no hace falta excepción.
- **El POST de comentarios se alinea a la raíz.** Hoy `FlowEventView.post` compara con el status propio del objeto, lo que deja comentar un hijo en `cp_completed` con el eje aún en `cp_filling`; pasa a usar la raíz, como el resto del motor. Resuelve la divergencia que anotó [[task-124]] §3.
- **El campo privado `comments` de los criterios de bp** (TextField en `FeatureItem`, no es `FlowEvent`) sigue la misma regla: editable mientras el envío esté en revisión, congelado después. Cierra esa parte de [[task-44]].

Lo que hay que construir: `PATCH` y `DELETE` sobre un evento (`/flow/<app>/<model>/<pk>/events/<event_id>/`), con el guard de raíz y de lado; el mismo guard en el POST; controles de editar y borrar en `FlowComments` / `FlowTimeline` espejando la regla con `getRootNotInTurn` del store; el candado del campo de criterios.

## Criterios de aceptación

- [ ] Una revisora edita y borra cualquier comentario de revisión sobre un hijo mientras la raíz esté en rol `reviewer`; con la raíz en rol `ies` o terminal, los controles no aparecen y el endpoint responde 403
- [ ] La IES edita y borra los comentarios de su lado bajo la regla simétrica
- [ ] Borrar un comentario puro elimina el evento; borrar el de una transición deja el evento sin texto
- [ ] El POST de comentarios rechaza comentar un hijo cuando la raíz no está del lado de quien comenta
- [ ] El campo `comments` de los criterios de bp se bloquea cuando el envío no está en revisión
- [ ] La regla aplica a los tres niveles y a los tres flujos: `bp`, `gen` y `cp`
