---
type: task
id: task-168
title: Decisiones pendientes de Ricardo tras la construcción de cp
state: closed
date: 2026-09-22
owner: ricardo
parent: "[[task-2]]"
source: ["[[2026-09-22-cierre-cuestionario-principal-captura-y-borrado]]"]
related: ["[[adr-0019]]", "[[task-13]]"]
---

# Decisiones pendientes de Ricardo tras la construcción de cp

Lo que la sesión del 22 de septiembre dejó abierto porque es llamado de Ricardo y no alcanzó a responderlo:

1. **Extender «raíz en turno» a gen y bp** ([[adr-0019]] aplica solo a cp): hoy la revisora puede aprobar o devolver un grupo `gen_completed` con el paquete en `gen_draft`, y una práctica `bp_completed` con el paquete en `bp_draft`. Opciones: dejarlo, o mover `review_turn_errors` a `flow/permissions.py` como helper genérico sobre `resolve_flow_root` y llamarlo desde `GeneralGroupResponse` y `GoodPractice`, con `root:` en `GeneralGroupPanel` y `GoodPracticeEditSimple`.
2. **La cola «En turno de la revisión»** del encabezado del eje (`CpAxisCapture`, `countInTurn`) cuenta por rol del estatus, así que muestra grupos completados aunque el eje no se haya enviado. ¿Cuenta 0 mientras el eje esté en turno de la IES, o se queda como «lo que la IES ya completó»?
3. **Etiqueta del filtro de estatus** de la colección de ejes: dice «Estatus»; el snackbar dice «Estado cambiado a…». Una palabra.
4. **Payload de login:** `InstitutionFullSerializer` cuenta observables por eje sin prefetch, 4 queries extra por survey. Dejarlo (una llamada por sesión) o prefetch en la vista de login/perfil.
5. **¿Sobra `cp_in_adjustment`?** `cp_need_changes` ya es editable; la duda viene de la sesión de rediseño del flujo y sigue abierta.
6. **Criterio «sin captura» del tipo de pregunta:** hoy `QuestionType.model_response IS NULL` (solo `population`). ¿Basta, o un booleano explícito `has_capture` con migración y siembra?
7. **Sí/No inicial para la revisora** se ve `disabled` (poco contraste); `v-btn-toggle` no tiene `readonly`.
8. **Deep-link `/respuestas/2025?tab=axis-1`** recargado cae en `?tab=base` contra el API real (probablemente `is_test` llega después del primer render); el e2e mockeado pasa. Preexistente, sin confirmar.
9. **`notifyApiError`** une con comas los `detail` en lista y el snackbar siempre es verde, incluso en errores. Preexistente.
10. **¿Las IES de prueba quedan exentas de la compuerta cp?** Hoy no lo están ([[adr-0018]]). Lo decidió la sesión, no Ricardo, y contradice la convención escrita en `api/CLAUDE.md` («test institutions see every section and ignore period deadlines»). Opciones: ratificar (no exentas: la IES de prueba ve lo mismo que una real, incluido el aviso); exentarlas solo de la fecha (siguen dependiendo de su base en `gen_finished`); o exentarlas de ambas (capturan siempre, útil para demos y pruebas, pero ya no muestran lo que verá una IES real).
11. **¿Los ejes se ordenan por prioridad del estatus por defecto?** Está implementado (`AxisValueViewSet.ordering` y `cat_params.extra_sorts`, commit `d804c5a`), pero Ricardo dijo «no estoy seguro» y no llegó a responder. Opciones: dejarlo, o volver al orden por eje y dejar la urgencia como orden opcional.
12. **Los 39 tests de `api/answer/tests.py`** se escribieron sin que Ricardo pidiera tests ni acordara la lista (la regla global es proponerlos, no escribirlos). Opciones: ratificarlos, recortarlos a los que prueban comportamiento prometido, o retirarlos.
13. **¿El módulo de estatus inferior del observable se oculta en «No»?** El superior, a la derecha de la pregunta inicial, ya se muestra solo con «Sí» (su spec: «solo cuando exista una respuesta en true»). El inferior (`CpObservablePanel.vue`, `v-if="answered"`) sigue visible también con «No», donde muestra el hint del estatus terminal. Opciones: dejarlo así u ocultarlo también.

## Respuestas de Ricardo (sesión del 23 de septiembre)

Todas registradas en [[2026-09-23-diseno-de-la-captura-cp-y-decisiones-pendientes]]; lo que abrió trabajo nuevo vive en [[task-169]].

1. **Extender «raíz en turno» a gen y bp: sí.** Hecho: `flow/permissions.py::root_turn_errors` sobre `resolve_flow_root`, con mensaje por raíz (`root_not_sent_message`, expuesto como `not_sent_message`); enganchado en `GeneralGroupResponse` y `GoodPractice`, y `root:` en `GeneralGroupPanel`, `GoodPracticeEditSimple` y `GoodPracticePackageEditSimple`. Enmienda en [[adr-0019]].
2. **La cola del eje: opción (a).** Mientras el eje esté en turno de la IES, la revisora lee «N completados por la institución, eje sin enviar»; una vez enviado, «En turno de la revisión: …». Hecho en `CpAxisCapture`.
3. **«Estatus» en todo.** Hecho (el snackbar decía «Estado cambiado a…»); Ricardo: no pasa nada si se cuela un «status».
4. **Payload de login: dejarlo.** Una llamada por sesión.
5. **`cp_in_adjustment` se queda.** Es el espejo de «En llenado» para la segunda vuelta: cuando la IES guarda tras «Requiere ajustes», el grupo pasa solo a «En ajustes» y eso sube al observable y al eje, así la revisora ve qué ya se está atendiendo sin esperar «Ajustes atendidos». Sin él, «Requiere ajustes» significaría a la vez «no lo han visto» y «están trabajando».
6. **Criterio «sin captura»: la implícita basta** (`QuestionType.model_response IS NULL`). El mismo criterio decide ahora que esos grupos nazcan en `cp_approved` ([[adr-0020]]).
7. **Sí/No inicial para la revisora:** resuelto al migrar el control a radios (`YesNoRadio`, que sí tiene `readonly`).
8. **Deep-link:** corregido en `pages/respuestas/[period].vue` (las pestañas esperan perfil y catálogos; el setter ignora escrituras prematuras); test de regresión en `e2e/respuestas-tabs.test.ts` que falla en HEAD y pasa con el fix. Se conserva `?tab=` (Ricardo preguntó por sub-ruta; se descartó: las pestañas son estado de una página).
9. **`notifyApiError`:** corregido (`useApiError` aplana los `detail`, snackbar en color `error` vía `dashStore.showError`).
10. **IES de prueba: exentas solo de la fecha**, no de `gen_finished`. Enmienda en [[adr-0018]].
11. **Orden de ejes: natural, sin orden opcional por urgencia.** Revertido `d804c5a` (`AxisValueViewSet.ordering`, `extra_sorts`). El «orden opcional» fue añadido del modelo, nadie lo pidió.
12. **Tests: quedan en manos del modelo** (Ricardo: «en general los tests yo termino pidiéndote que decidas»). Los 39 quedan ratificados sin revisión individual; el recorte a los que prueban comportamiento prometido no se hizo; hoy 3 adaptados y 4 de regresión nuevos en `api/`, más 1 e2e.
13. **Módulo de estatus inferior: retirado.** Queda solo el superior, junto a la pregunta inicial, con «Sí»; el hint «Te toca» vive solo en el eje.

## Criterios de aceptación

- [x] Cada punto tiene respuesta registrada aquí o convertido en task propia
