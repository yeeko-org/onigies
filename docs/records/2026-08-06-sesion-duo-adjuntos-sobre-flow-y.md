---
type: record
id: 2026-08-06-sesion-duo-adjuntos-sobre-flow-y
title: "Sesión duo: adjuntos sobre flow y ajustes de generales"
date: 2026-08-06
---

# Sesión duo: adjuntos sobre flow y ajustes de generales

Bitácora de la sesión duo (coordinador Fable 5, ejecutores Opus 5 y Sonnet 5) sobre la épica [[task-41]]: tasks [[task-66]], [[task-67]] y [[task-68]].

## Qué pasó

1. **Barrido previo** (subagente): ninguna otra tarea huérfana toca el bloque de generales; se detectaron desfases de checklist en [[task-1]], [[task-2]] y [[task-8]] (corregidos en este cierre) y el cuerpo desactualizado de [[task-55]].
2. **Desenredo de [[task-7]]** (subagente, verificado por el coordinador): la premisa «los archivos de BP corren sobre flow» era falsa — corrían sobre `example.Evidence`, la única subida viva del sistema; `flow.Attachment` era un modelo sin API ni frontend, poblado solo por `migrate_flow_data`. La razón del borrado planeado sí estaba escrita (una línea del diseño del 2026-06-05: consolidación arquitectónica) pero nunca se argumentó como decisión de producto.
3. **Corrección de alcance de Ricardo**: había confundido nombres — los adjuntos van por `GroupResponse` (cp) y `GeneralGroupResponse` (gen); `Observable` nunca lleva adjuntos directos. Eso coincide exactamente con los modelos viejos y con las ramas ya existentes de `resolve_upload_path`.
4. **Decisión central** ([[adr-0010]]): stack unificado de adjuntos sobre `flow.Attachment`, anclados al objeto (no al evento del timeline), y BP migrado en la misma obra (opción b, elegida por Ricardo).
5. **Implementación** (ejecutor Opus): endpoints genéricos `GET/POST/DELETE /flow/<app>/<model>/<pk>/attachments/`, `flow_delegate` en el registry para satélites (`FeatureGoodPractice` → `GoodPractice`), `user_can_edit_flow_content` como espejo servidor de `canEditContent`, `FlowAttachments.vue` montado en `GeneralGroupPanel` (doble audiencia), `GoodPracticeEditSimple` y `FeatureItem` (×2); `Evidences.vue` borrado y ninguna llamada a `add_file`/`/evidence/` sobrevive en el front. Cierra de paso el hueco de seguridad del `EvidenceViewSet` (cualquier autenticado podía borrar evidencias ajenas).
6. **task-66** (ejecutor Sonnet): prop `maxWidth` en `GeneralNumberInput` + `110px` en las celdas de la tabla de poblaciones.
7. **task-67**: análisis UX completo (subagente con el skill ux-designer); recomendación: ícono `123` en `prepend-inner` + `inputmode="numeric"` + texto sr-only vía aria-describedby. Hallazgo: `v-number-input` fija `inputmode="decimal"`, no expone nada a lectores de pantalla y sus spinners son aria-hidden. La decisión quedó pendiente ([[task-93]]).

## Verificación

pytest 68/68 en verde; `makemigrations --check` sin cambios (cero migraciones de esquema); `migrate_flow_data` + `verify_flow_data` en local con la sección de adjuntos `[ok]` (51 `Evidence` → 51 `Attachment`). Reglas de permisos smoke-testeadas por el ejecutor (IES ajena 403, revisora solo lectura, paquete enviado 403, delegación de característica).

## Pendiente al cierre

Las decisiones que Ricardo no alcanzó a tomar quedaron en [[task-93]]; los tests de regresión propuestos, en [[task-94]]. En producción: re-correr `migrate_flow_data` en el deploy y contar las `Evidence` huérfanas antes del borrado de [[task-7]].

## Colaterales detectados

- `nuxt/CLAUDE.md` decía tema rojo/naranja; el real es índigo/turquesa del design-system (corregido en este cierre).
- Vuetify instalado es 3.12.8 (el package.json pide ^3.10.7); la migración a 3.13 quedó en [[task-91]].
- `mainStore.saveFile` quedó sin consumidores; se borra en [[task-7]].
