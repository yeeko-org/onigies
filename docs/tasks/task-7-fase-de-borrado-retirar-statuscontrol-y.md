---
type: task
id: task-7
title: "Fase de borrado: retirar StatusControl y los modelos viejos"
state: open
date: 2026-08-03
owner: ai
parent: "[[task-1]]"
source: ["[[2026-06-05-diseno-del-motor-de-flujo]]"]
---

# Fase de borrado: retirar StatusControl y los modelos viejos

El §8 del diseño del motor, que quedó fuera de los dos deploys. Quitar `status_register`/`status_sending` de los seis modelos; borrar `ObservableComment`, `GroupComment`, `GroupAttachment`, `GeneralGroupComment`, `GeneralGroupAttachment`, `Evidence`, el `Comment` abstracto y los helpers de upload viejos; quitar `comments` (TextField) de los tres modelos de `example`; borrar `ies.StatusControl`, su admin, `InitStatus` y sus choices; simplificar `Institution.save()`; y cambiar el filtro `status_sending__is_final=False` por `status__role__isnull=False` en `api/api/views/example/__init__.py`.

Precondición: haber verificado los datos migrados en producción con `verify_flow_data`. Las migraciones las corre Ricardo.

## Duda resuelta sobre los modelos de adjuntos (2026-08-06, sesión duo)

La duda que dejó la revisión con Fernanda ([[2026-08-06-temas-reunion-fer]], §9) quedó desenredada en [[2026-08-06-sesion-duo-adjuntos-sobre-flow-y]] y decidida en [[adr-0010]]. La historia: la razón del borrado sí estaba escrita —una línea del §2.3 del diseño del motor: `flow.Attachment` reemplaza a los tres modelos viejos, consolidación arquitectónica análoga a la de `FlowEvent`— pero nunca se argumentó como decisión de producto. La sorpresa fue que **BP no corría sobre flow**: `Evidence` era la única subida viva. La sesión estrenó el stack sobre `flow.Attachment` y migró BP al mismo mecanismo, así que **el borrado completo procede**, ampliado: también se retiran `ActionFileMixin`/`add_file`, `EvidenceViewSet` (`/evidence/`), el campo muerto `evidences` de los serializers de BP y `mainStore.saveFile` en el frontend.

Precondiciones nuevas antes de las migraciones de borrado: re-correr `migrate_flow_data` en producción justo antes (entró evidencia al modelo viejo hasta el deploy de este cambio) y contar las `Evidence` huérfanas (sin FK), que la migración no copia — si hay, decidir su destino.

## Re-run en producción (2026-08-12)

El deploy de [[2026-08-12-deploy-gen-a-produccion-migraciones-seeds]] corrió `migrate_flow_data` completo: 609 evidencias espejadas, `verify_flow_data` cerró **661 = 661 [ok] sin huérfanas**. La precondición está cumplida al día de hoy; si el borrado tarda en llegar, el re-run «justo antes» sigue aplicando porque puede seguir entrando evidencia al modelo viejo mientras coexistan.

## Criterios de aceptación

- [ ] `grep -r status_sending\|status_register api/` no devuelve nada
- [ ] `ies.StatusControl` y los modelos de comentarios/adjuntos viejos ya no existen
- [ ] `ActionFileMixin`, `EvidenceViewSet`, el campo `evidences` de los serializers de BP y `mainStore.saveFile` tampoco
- [ ] Las migraciones de borrado corrieron en producción sin incidentes (con `migrate_flow_data` re-corrido y huérfanas contadas justo antes)
- [x] La razón para borrar `GroupAttachment` y `Evidence` quedó reconstruida o decidida de nuevo, y es compatible con [[task-68]] ([[adr-0010]])
