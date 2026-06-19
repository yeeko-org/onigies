# Progreso — Frontend del motor de flujo (Buenas Prácticas)

Estado al **2026-06-16**. Complementa `PLAN_flujo_validacion.md` (diseño del
motor) con el avance del **frontend** y la migración de Buenas Prácticas (bp).
Plan de esta sesión: `~/.claude/plans/swift-twirling-cerf.md`.

## Concepto clave (no volver a confundir)

`Status.role` = **de quién es el turno**: `ies` actúa la institución,
`reviewer` la revisora, `None` terminal. **Todo el front se decide por
`status.role`, nunca por nombre de status.** `has_good_practices` es ortogonal
al flujo (no es un status). Detalle completo en el skill `flow`
(`~/.claude/skills/flow/SKILL.md`).

Dos superficies separadas:
- **IES** → `/respuestas/[period]` (`GoodPracticeList.vue`): la pregunta,
  descartar/reabrir, enviar, lista y alta.
- **Revisora** → dashboard (colecciones), `GoodPracticePackageEditSimple.vue`
  (paquete) + `GoodPracticeEditSimple.vue` en modo staff (práctica, sliders).
  **Sin** la pregunta de la IES.

## Hecho (bp)

- ✅ Skill `flow` (modelo, catálogo, separación IES/revisora, componentes y
  endpoints). **Sin** la convención de auto-carga del dashboard.
- ✅ `nuxt/.../flow/FlowComments.vue` (nuevo): timeline + comentarios,
  `GET/POST /flow/{app}/{model}/{pk}/events/`. Reutilizable paquete y práctica.
- ✅ Reusados: `flow/FlowStatusChip.vue`, `flow/FlowTransitions.vue`.
- ✅ IES `GoodPracticeList.vue`: `editionAvailable`/alerta por `status.role`;
  `canReopen` por `has_good_practices`; enviar/reenviar vía motor (transición
  disponible) con confirmación + `NotReadyDialog`; chip + comentarios.
- ✅ IES `GoodPracticeEditSimple.vue`: `FlowStatusChip` + `FlowTransitions` +
  `FlowComments`; fuera `StatusToggle`/`StatusDetail`/prompt "Lista para enviar".
  Sigue dual por `isStaff` (revisora ve sliders).
- ✅ `NewGoodPractice.vue`: sin `status_sending` (default del modelo `bp_draft`).
- ✅ Revisora `GoodPracticePackageEditSimple.vue`: cabecera + chip +
  `FlowTransitions(reviewer)` + lista solo-lectura + comentarios; **sin**
  `has_good_practices`/radio/enviar/descartar.
- ✅ Backend: jubilada la acción `/send` en
  `api/api/views/example/__init__.py` (`sent_at` lo fija el hook de
  `GoodPracticePackage.save()` al pasar a `bp_sent`/`bp_resent`).
- ✅ Verificado: `py_compile` backend OK; cero status hardcodeados en
  componentes bp/flow; sin variables huérfanas.

## Pendiente

1. **Verificación manual de bp** (no se corrió `pnpm run dev` en la sesión):
   - IES: responder "Sí" → agregar → `FlowTransitions` marca completada →
     "Enviar a revisión" (confirmación + faltantes) → `bp_sent` + `sent_at`.
     "No" cierra; "Cambiar respuesta" reabre. Comentar en paquete y práctica.
   - Revisora (dashboard, colección GoodPracticePackage/GoodPractice): no ve la
     pregunta de la IES; ve status, transiciones de revisora, comentarios,
     sliders. Ejecutar `bp_sent→bp_finished` (requiere hijos en
     `bp_for_ruling`/`bp_rejected`).
2. **CP (cuestionario principal) y gen (generales) en el front** — no iniciado.
   `FlowTransitions`/`FlowStatusChip`/`FlowComments` son genéricos y sirven;
   falta incorporarlos a las páginas de respuesta de CP y a su revisión.
3. **Skill de la convención de auto-carga del dashboard**
   (`{Model}Edit/EditSimple/Sheet`). Borrador: `nuxt/DASHBOARD_AUTOLOAD_DRAFT.md`.
4. **`discard`/`reopen` backend** siguen tocando `status_sending` viejo
   (coexistencia). Funcionan porque el front se guía por `has_good_practices` +
   `status` nuevo, pero migrarlos/limpiarlos en la fase de borrado.
5. **`filters.js` / `fetch.js`** aún referencian `status_sending`/
   `status_register` para los paneles de filtros — sin actualizar.
6. **Fase de borrado §8** (tras verificar en producción con `verify_flow_data`):
   quitar `status_sending`/`status_register` de los 6 modelos, modelos viejos de
   comentarios/adjuntos, `ies.StatusControl`, y ajustar el filtro de
   `api/api/views/example/__init__.py` (`status_sending__is_final=False` →
   `status__role__isnull=False`).
