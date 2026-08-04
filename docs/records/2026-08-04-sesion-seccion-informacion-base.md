---
type: record
id: 2026-08-04-sesion-seccion-informacion-base
title: "Sesión: sección de información base capturable (task-41)"
date: 2026-08-04
---

# Sesión: sección de información base capturable (task-41)

Sesión duo (coordinador Fable 5, ejecutores Opus 4/agentes) del 2026-08-03/04. Se rehizo por completo la sección «Información base» (flujo `gen`) espejando Buenas Prácticas, frontend y backend, según decisión de Ricardo de no conservar `SurveyInitData.vue` ni el patrón viejo.

## Qué se construyó

- **Backend**: escritura de todo el contenido gen contra `Survey` ([[adr-0008]]), serializers/viewset de `GeneralPackage` espejo de bp, colecciones «Cuestionarios de las IES» y «Envíos de preguntas generales» (esta sin menú), `GeneralGroup.order`, banderas `Sector.is_standard_extra`/`is_ies_head`, candado `Period.gen_submission_deadline` + `is_gen_submission_closed` con hook server-side.
- **Frontend IES** (`/respuestas`, tab «Información base»): expansion panels con apertura múltiple todos-abiertos y auto-colapso al completar (híbrido decidido en diálogo con material de UX: ux-designer + spec MD3), tabla única de poblaciones (Existe/Hombres/Mujeres/Total, deshabilitado-no-oculto, extras sin conteo), autoridades con radio de titular + 3 filas fijas sin columna Existe, split-button guardar/transicionar, envío gateado por el motor.
- **Frontend revisora** (dashboard): `SurveyHeader`/`SurveyEditSimple`/`SurveySheet` reutilizando la misma sección dual-audiencia en solo lectura con transiciones por grupo y del paquete.
- **Arreglos transversales que salieron del humo integrado** (dos recorridos en navegador por agente): montaje de `FlowTransitionDialogs` por kernel (la revisora no podía transicionar), `GlobalSnackbar.vue` compartido (la cara IES no tenía snackbar: silenciaba errores también en bp), el motor de flow ahora guarda con `save()` completo (`sent_at` nunca persistía — afectaba bp), mensaje de compuerta sin dependencia de género, sincronización renglón↔detalle vía `item-saved` para `EditSimple`.

## Decisiones de Ricardo en sesión

- Rehacer todo espejando bp, con envío por grupo ([[task-41]]).
- Panels híbridos (todos abiertos, auto-colapso) sobre cards+diálogo o scroll puro.
- Tabla única poblaciones; autoridades sin columna Existe (no son poblaciones objetivo); `no_apply` fuera hoy ([[task-56]]).
- Contenido contra Survey, opción (a) ([[adr-0008]]); `PopulationQuantity.name` opcional.
- Banderas booleanas en Sector (no CHOICES); `GeneralGroup.order`; candado de período gen con migración.
- Revisora sin permiso de editar contenido (solo status y comentarios); preguntar a Rubí ([[task-57]]).
- `gen_approved`/`gen_finished` terminales en todos los sentidos: el seed reconstruye `next_statuses` de todos los statuses.
- Devolver un grupo no propaga al paquete; la UI guiará la doble transición después ([[task-58]]).
- Resúmenes: «11 marcadas · 2/9 con conteo», sin suma de personas.
- La task-42 (preguntas del cuestionario en dashboard) se difirió; hallazgos en su cuerpo.

## Notas de deploy (cuando task-41 pase a producción)

1. Migraciones: `survey 0008`, `indicator 0008`, `ies 0012`.
2. Re-correr seeds: `load_sectors` (banderas), `load_questionnaire` con `--sync-institutions` (order + backfill de GeneralGroupResponse), `seed_flow` (limpieza de terminales).
3. Fijar en el admin `Period.gen_submission_deadline = 2026-11-01` para 2025 (Ricardo lo hace a mano; en local ya está).
4. Evaluar la reparación de `sent_at` de bp ([[task-59]]) en la misma ventana.

Usuarios de humo locales (`smoke-ies@test.local` / `smoke-staff@test.local`) existen solo en la base local.
