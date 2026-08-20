---
type: task
id: task-7
title: "Fase de borrado: retirar StatusControl y los modelos viejos"
state: open
date: 2026-08-03
owner: ai
parent: "[[task-1]]"
source: ["[[2026-06-05-diseno-del-motor-de-flujo]]", "[[2026-08-20-inventario-de-usos-vivos-de-statuscontrol]]"]
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

## Inventario de ejecución y retiro adelantado de la superficie visible (2026-08-20)

El insumo para ejecutar esta task sin volver a derivar nada es [[2026-08-20-inventario-de-usos-vivos-de-statuscontrol]]: inventario completo de cada uso vivo de `StatusControl` con paths y líneas, clasificado en andamiaje de coexistencia, código muerto y «UI viva sin efecto» (etiqueta acuñada ahí: código que se ejecuta y se pinta, pero cuyo resultado el sistema descarta). Trae además tres cosas que ahorran trabajo a la sesión que ejecute el borrado: el dato duro de que **solo `good_practice` y `good_practice_package` exponen `status_groups`** —los cuatro modelos con `status_register` no están registrados como colecciones—, la lista de restos borrables hoy sin migraciones (`utils/mix_models.py`, `IsEditorOrCreateOrRead`, `AdvancedConditionalFieldsViewMixin`, la clave `"validation"` de `STATUS_GROUP_PARAMS`, `StatusToggle.vue`), y el camino mínimo en cinco pasos con el orden forzado por las columnas `NOT NULL` y por el cambio de forma del payload.

Con ese inventario a la vista, Ricardo decidió el 2026-08-20 **separar las dos mitades**: esta task se ejecuta completa en una sesión aparte, y ese mismo día se retiró por adelantado solo la superficie visible de «Status de Envío» en el dashboard —el `v-select` que escribía `status_sending` por PATCH sin que eso gobernara ningún flujo, engañoso para la revisora que sí dictamina con `FlowStatusActions` en el mismo header—. Consecuencia para el alcance restante: **parte del paso 5 (frontend) ya está hecha** y quedan componentes huérfanos por borrar, que el borrado debe recoger junto con el resto de la cadena (`status_dict`, `status_filters`, `calculate_status`, `statusGroupLabel`, `StatusChip.vue`, la rama `status_groups` de `_derive_field_meta` y los typedefs de `nuxt/app/types/collection.js`).

## El punto 5 del §8 quedó sin objeto (2026-08-20)

El alcance descrito arriba y el §8.5 del diseño mandan cambiar el filtro `status_sending__is_final=False` por `status__role__isnull=False` en `api/api/views/example/__init__.py`. **Ese filtro ya no existe en el código**: `grep -rn is_final api/`, excluyendo migraciones, devuelve solo `api/ies/initial_data.py:7,61,75` y `api/ies/models.py:368` (el seed y la definición del campo), y en `api/api/views/example/__init__.py` no hay rastro — desapareció en un refactor previo que nadie anotó. El punto queda como desactualizado, no como pendiente: no hay nada que cambiar ahí.

## Criterios de aceptación

- [ ] `grep -r status_sending\|status_register api/` no devuelve nada
- [ ] `ies.StatusControl` y los modelos de comentarios viejos ya no existen (los de adjuntos ya se borraron el 2026-08-12)
- [x] `ActionFileMixin`, `EvidenceViewSet`, el campo `evidences` de los serializers de BP y `mainStore.saveFile` tampoco (sesión S3, 2026-08-12)
- [ ] Las migraciones de borrado corrieron en producción sin incidentes (la precondición del re-run quedó eliminada el 2026-08-12 con el retiro del comando; las `Evidence` huérfanas siguen pendientes de contar antes del borrado)
- [x] La razón para borrar `GroupAttachment` y `Evidence` quedó reconstruida o decidida de nuevo, y es compatible con [[task-68]] ([[adr-0010]])

Nota (2026-08-20): el punto del alcance que pedía cambiar el filtro `status_sending__is_final=False` por `status__role__isnull=False` está **desactualizado** y no cuenta para el cierre — el filtro ya no existe en `api/api/views/example/__init__.py`; la evidencia está en la sección anterior y en [[2026-08-20-inventario-de-usos-vivos-de-statuscontrol]].
