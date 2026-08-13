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

Precondición (cumplida y cerrada el 2026-08-12): los datos migrados quedaron verificados en producción con `verify_flow_data` (661 = 661, sin huérfanas). Las migraciones las corre Ricardo.

## Duda resuelta sobre los modelos de adjuntos (2026-08-06, sesión duo)

La duda que dejó la revisión con Fernanda ([[2026-08-06-temas-reunion-fer]], §9) quedó desenredada en [[2026-08-06-sesion-duo-adjuntos-sobre-flow-y]] y decidida en [[adr-0010]]. La historia: la razón del borrado sí estaba escrita —una línea del §2.3 del diseño del motor: `flow.Attachment` reemplaza a los tres modelos viejos, consolidación arquitectónica análoga a la de `FlowEvent`— pero nunca se argumentó como decisión de producto. La sorpresa fue que **BP no corría sobre flow**: `Evidence` era la única subida viva. La sesión estrenó el stack sobre `flow.Attachment` y migró BP al mismo mecanismo, así que **el borrado completo procede**, ampliado: también se retiran `ActionFileMixin`/`add_file`, `EvidenceViewSet` (`/evidence/`), el campo muerto `evidences` de los serializers de BP y `mainStore.saveFile` en el frontend.

Precondiciones nuevas antes de las migraciones de borrado: re-correr `migrate_flow_data` en producción justo antes (entró evidencia al modelo viejo hasta el deploy de este cambio) y contar las `Evidence` huérfanas (sin FK), que la migración no copia — si hay, decidir su destino.

## Re-run en producción y retiro del comando (2026-08-12)

El deploy de [[2026-08-12-deploy-gen-a-produccion-migraciones-seeds]] corrió `migrate_flow_data` completo: 609 evidencias espejadas, `verify_flow_data` cerró **661 = 661 [ok] sin huérfanas** — pero ese mismo re-run aplastó 179 estatus avanzados de flow ([[2026-08-12-incidente-migrate-flow-data]]; restaurados quirúrgicamente la misma noche). Tras el incidente, los comandos `migrate_flow_data`/`verify_flow_data` se retiraron del repo. **La precondición «re-correr justo antes del borrado» queda eliminada**: es insatisfacible (el comando ya no existe) e innecesaria — la migración de datos está completa y congelada desde ese día, porque ya no queda ninguna vía de escritura viva hacia los modelos legacy (el stack de Evidence se borró en la sesión de S3 y los comentarios viejos no tienen endpoint); lo único que escribe las columnas legacy son los defaults de creación, que el borrado retira de todos modos.

## Nivel 2 ejecutado en la sesión de S3 (2026-08-12)

La sesión de [[adr-0013]] ([[2026-08-12-migracion-de-archivos-a-s3]], [[task-122]]) adelantó una parte: se borraron los dos modelos huérfanos de adjuntos (`GroupAttachment` y `GeneralGroupAttachment`, migraciones `answer/0004` y `survey/0010`, desplegadas esa noche) y todo el stack API de `Evidence` — `EvidenceSerializer`, el campo `evidences`, `ActionFileMixin`/`add_file`, `EvidenceViewSet`, el módulo `action_file.py` completo y `mainStore.saveFile`. Los comandos `migrate_flow_data`/`verify_flow_data` quedaron reducidos a `Evidence`. La compuerta estaba cumplida ese mismo día (verify 661 = 661). **Queda el alcance restante**: el modelo `example.Evidence`, `ies.StatusControl` + `InitStatus`, los modelos de comentarios viejos, `status_register`/`status_sending`, el `comments` TextField, `Institution.save()` y el filtro de `example/__init__.py`.

## Criterios de aceptación

- [ ] `grep -r status_sending\|status_register api/` no devuelve nada
- [ ] `ies.StatusControl` y los modelos de comentarios viejos ya no existen (los de adjuntos ya se borraron el 2026-08-12)
- [x] `ActionFileMixin`, `EvidenceViewSet`, el campo `evidences` de los serializers de BP y `mainStore.saveFile` tampoco (sesión S3, 2026-08-12)
- [ ] Las migraciones de borrado corrieron en producción sin incidentes (la precondición del re-run quedó eliminada el 2026-08-12 con el retiro del comando; las `Evidence` huérfanas siguen pendientes de contar antes del borrado)
- [x] La razón para borrar `GroupAttachment` y `Evidence` quedó reconstruida o decidida de nuevo, y es compatible con [[task-68]] ([[adr-0010]])
