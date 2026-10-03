---
type: task
id: task-70
title: Editar y borrar los comentarios propios mientras el envío siga de tu lado
state: closed
date: 2026-08-06
owner: ai
parent: "[[task-99]]"
source: ["[[2026-08-06-temas-reunion-fer]]", "[[2026-10-02-comentarios-editables-y-valvula-de-admin]]"]
related: ["[[adr-0019]]", "[[task-44]]", "[[task-124]]", "[[task-190]]", "[[task-69]]"]
---

# Editar y borrar los comentarios propios mientras el envío siga de tu lado

§10 de la reunión con Fernanda, `[17:20]`–`[24:33]`. Fernanda pidió un botón para editar comentarios; Ricardo detectó además que hoy no se puede borrar un comentario general ya guardado (lo probó con el COLEF), y propuso que si el envío está en tu turno y son tus últimos comentarios, debería permitirse.

**La regla que enunció Ricardo en la llamada:** se puede editar o borrar un comentario **mientras el envío siga de tu lado**; una vez que la contraparte ya lo vio o empezó a atenderlo, ya no debería poder modificarse. Es la misma noción de turno que gobierna la edición de contenido en el motor (`canEditContent`, skill `flow`).

Aplica a los tres niveles de comentario. El caso que lo motivó: Fernanda metió un comentario general muy largo en la buena práctica equivocada («agenda estadística») cuando debía ir a nivel de envío, y no pudo moverlo ni borrarlo; Ricardo le pidió eliminar el duplicado para que la IES no viera dos y no fue posible desde la interfaz.

## Decisiones del 2026-10-02

Ricardo cerró la regla en diálogo ([[2026-10-02-comentarios-editables-y-valvula-de-admin]]); esto extiende lo de arriba, no lo contradice:

- **El turno lo define la raíz, no el status propio** (como [[adr-0019]] y `canEditContent`). Un comentario de revisión sobre una buena práctica, un grupo gen o un observable es editable mientras el envío, el paquete o el eje (`AxisValue`) siga en rol `reviewer`. Simétrico para la IES mientras la raíz esté en rol `ies`. Una raíz terminal (rol de nadie) congela los comentarios de ambos lados.
- **Ya no son solo los propios:** cada lado edita y borra los comentarios de su lado sin importar quién los escribió («sin importar quién sea la revisora»). El lado de un comentario es el rol de flujo de su autor al momento de la petición.
- **Solo la ronda actual.** Es la regla original de Ricardo («una vez que la contraparte ya lo vio o empezó a atenderlo, ya no debería poder modificarse») llevada al código tras el hallazgo del auditor de congruencia: con solo «raíz en tu lado», los comentarios de una ronda anterior volvían a ser editables cuando el turno regresaba. Editable es lo escrito después de la última vez que la raíz **entró** a tu lado (el último `FlowEvent` de la raíz cuyo destino tiene tu rol y cuyo origen no lo tenía); un movimiento dentro del mismo lado (`cp_sent` → `cp_in_review`, las propagaciones de `cp_filling`) no abre ronda. Si la raíz nunca cambió de lado, todo lo de tu lado cuenta. Helper `round_started_at(root, role)` en `api/flow/permissions.py`, espejo `roundStartedAt` en el store.
- **Borrar significa borrar solo el comentario:** en un comentario puro (sin cambio de status) se borra la fila del `FlowEvent`; en un comentario de transición se vacía `comment` y el evento de cambio de status se queda.
- **El motivo de un cambio administrativo** ([[task-190]]) no se borra nunca (403 también para admin) y solo lo corrige `is_admin`: quien no pudo hacer el cambio no cambia su explicación.
- **Sin `edited_at` ni migración.** Dentro de la ronda la contraparte no ha actuado sobre ese comentario; una marca «editado» no cambia ninguna decisión. El comentario de la devolución que disparó el correo a la IES queda fuera de alcance en cuanto la IES reenvía, por la regla de ronda.
- **El POST de comentarios se alinea a la raíz.** `FlowEventView.post` comparaba con el status propio del objeto, lo que dejaba comentar un hijo en `cp_completed` con el eje aún en `cp_filling`; ahora usa `user_holds_root_turn`, como el resto del motor. Resuelve la divergencia que anotó [[task-124]] §3.
- **El campo privado `comments` de los criterios de bp** (`FeatureGoodPractice.comments`, no es `FlowEvent`; se edita desde `FeatureItem`) sigue la regla de turno por raíz, sin rondas porque es un solo campo: editable por cualquier revisora mientras el envío esté en rol `reviewer`, congelado después (`FeatureGoodPracticeSerializer.validate`). Un no revisor que lo mande se descarta en silencio, porque el formulario de la IES reenvía el campo oculto vacío en cada guardado; eso era, hasta hoy, una vía de borrado de la nota. Cierra esa parte de [[task-44]].

## Lo construido (2026-10-02)

`PATCH` y `DELETE` sobre `/flow/<app>/<model>/<pk>/events/<event_pk>/` (`FlowEventDetailView`), con guards en orden: pertenencia, comentario no vacío, lado, raíz en turno, ronda. Edición y borrado inline en `FlowTimeline` (lápiz, bote con confirmación en línea), API en `FlowComments`, regla espejo `canEditComment` en el store; `:root` llega a `FlowComments` desde `GeneralGroupPanel`, `CpGroupCard`, `GoodPracticeEditSimple` y el diálogo de la IES. Tests `CommentEditTests`, `CommentRootTurnTests`, `CommentRoundTests` y `CriterionCommentsLockTests`; Vitest de `canEditComment`/`eventSide`. Pasada en navegador del 2026-10-02 (capturas en `.claude/scratch/browser-pass/`). Reglas en la skill `flow` (references/comments.md).

## Criterios de aceptación

- [x] Una revisora edita y borra cualquier comentario de revisión sobre un hijo mientras la raíz esté en rol `reviewer`; con la raíz en rol `ies` o terminal, los controles no aparecen y el endpoint responde 403
- [x] La IES edita y borra los comentarios de su lado bajo la regla simétrica
- [x] Solo los comentarios de la ronda actual; los de una ronda anterior responden 403 (`CommentRoundTests`)
- [x] Borrar un comentario puro elimina el evento; borrar el de una transición deja el evento sin texto
- [x] El POST de comentarios rechaza comentar un hijo cuando la raíz no está del lado de quien comenta
- [x] El campo `comments` de los criterios de bp se bloquea cuando el envío no está en revisión
- [x] La regla aplica a los tres niveles y a los tres flujos: `bp`, `gen` y `cp`
