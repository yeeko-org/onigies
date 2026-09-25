---
type: task
id: task-166
title: Pruebas e2e propuestas para la captura y la revisión del cuestionario principal
state: open
date: 2026-09-22
owner: ricardo
parent: "[[task-2]]"
source: ["[[2026-09-22-cierre-cuestionario-principal-captura-y-borrado]]"]
related: ["[[task-140]]", "[[task-161]]"]
---

# Pruebas e2e propuestas para la captura y la revisión del cuestionario principal

Propuestas por los ejecutores del 22 de septiembre; no se escriben hasta que Ricardo acuerde la lista (regla global de tests). Backend simulado según la skill `playwright-e2e`, con un `e2e/mocks/cp.ts` espejo de `gen.ts`: catálogo de estatus cp (14, con `role`, `content_editable`, `priority`, `next_statuses`, `valid_child_statuses`, `applicable_models`, confirmación de `cp_sent`), `cats.question_type`, `makeAxisValue({captureOpen, reason, observables})` con dos o tres observables pequeños (uno A+B, uno plans, uno population) y `gen_denominators`, handlers de `PATCH /observable_response/{id}/` (con variante 400), `PATCH /group_response/{id}/` (devuelve `completion`), `GET /observable_response/{id}/`, `GET /axis_value/?institution&period`, `GET /axis_value/{id}/`, `POST /flow/answer/{model}/{id}/transitions/` y `/flow/survey/axisvalue/{id}/transitions/`, y `axis_values` en el perfil de `mockIesRespuestasUser`.

**Captura de la IES (`/respuestas`):**
1. Compuerta cerrada (`cp_not_open` con `open_at`, y `gen_not_approved`): aviso con fecha o link, controles inhabilitados, sin Guardar ni menús.
2. Respuesta inicial: Sí → PATCH `{value:true}` → estatus y tarjetas editables; No → íconos atenuados y tarjeta «Ver preguntas» en solo lectura; un 400 de revisión activa muestra el `detail` y el control no cambia.
3. Guardado por grupo: Guardar aparece al editar, el PATCH lleva solo las filas cambiadas, desaparece al guardar, y se pintan `completion.errors` y `warnings`.
4. Oferta del siguiente paso: completar el último grupo → snackbar con acción → POST de la transición del observable; último observable resuelto → acción → diálogo de confirmación de `cp_sent`.
5. Tipos especiales: plan oculta el nivel `no_apply`; reach con planeación general deshabilita los sectores; special marca «cumplen > total»; population muestra la nota con link a base.

**Revisión (dashboard, staff):**
6. Lista por urgencia y renglón: sin `ordering` en la URL, «FP - 2025», el eje, el chip y los conteos.
7. Detalle en modo revisión: solo lectura, sin Guardar, cola «En turno de la revisión», aviso de compuerta en voz de revisión.
8. Devolver un grupo: «Solicitar ajustes» exige comentario, envía `cp_need_changes`, el chip cambia y la cola baja; con el eje en turno de la IES, el menú sale con candado y el motivo.
9. Regla de hijos: con un grupo aún completado, el menú del observable sale deshabilitado con el motivo; al devolver el segundo aparece la oferta.
10. «No cuenta con la medida»: chip sin menú y grupos sin transiciones; la sección «Cuestionario principal» del survey abre el diálogo del eje.
11. (agregado el 2026-09-25) Enlace de descarga del cuestionario en Word: `data-testid="cp-docx-link"` visible en `/respuestas/2025?tab=axis-N` y ausente en `?tab=base`; una línea en `respuestas-tabs.test.ts`, sin mock nuevo porque el enlace es un href fijo.

Además: el mock de `respuestas-tabs.test.ts` no cubre `/axis_value/{id}/` (hoy recibe el 501 del catch-all y sale un snackbar de error aunque el test pase).

## Criterios de aceptación

- [ ] Ricardo acordó la lista (recortada, ampliada o redirigida)
- [ ] Los e2e acordados existen y pasan; nuxt/TESTING.md los lista como flujos cubiertos
