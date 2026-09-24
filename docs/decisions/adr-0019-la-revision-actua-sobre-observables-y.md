---
type: decision
id: adr-0019
title: La revisión actúa sobre observables y grupos solo cuando el eje ya está en su turno
state: accepted
date: 2026-09-22
origin: ricardo
deliberation: confirmed
rationale: recorded
source: ["[[2026-09-22-cierre-cuestionario-principal-captura-y-borrado]]"]
affects: ["api/flow/permissions.py", "api/answer/models.py", "api/survey/models.py", "api/example/models.py", "nuxt/app/composables/useFlowActions.js", "nuxt/app/store/flow.js", "nuxt/app/components/dashboard/survey/GeneralGroupPanel.vue", "nuxt/app/components/dashboard/example/good_practice/GoodPracticeEditSimple.vue"]
related: ["[[adr-0002]]"]
---

# La revisión actúa sobre observables y grupos solo cuando el eje ya está en su turno

## Contexto y planteamiento del problema

Un grupo u observable en `cp_completed` tiene rol revisora aunque su eje siga en `cp_filling` (turno de la IES). Al construir la revisión en el dashboard, la revisora pudo devolver el observable 1.1 de una IES de prueba sin que el eje se hubiera enviado. El hint de `cp_completed` dice «se revisará cuando envíes el eje», pero el motor no lo exigía.

## Criterios de decisión

- El envío del eje es el acto de entrega de la IES; dictaminar antes de ese acto confunde a las dos partes.
- Coherencia con la regla de contenido que ya gobierna: la raíz manda (`user_can_edit_flow_content`).

## Opciones consideradas

- **Dejarlo:** la revisora adelanta revisión a medida que la IES completa; útil en ejes de 17 observables. Era la recomendación del modelo.
- **Exigir el turno de la raíz** para toda transición de la revisora sobre hijos. Elegida por Ricardo (recordaba haberla aplicado antes en gen o bp; no existía en ninguno de los dos).

## Resultado

`flow/permissions.py::root_turn_errors` (hasta el 2026-09-23 vivía en `answer/services.py::review_turn_errors` y aplicaba solo a cp): si el usuario es revisora y la raíz del objeto (`resolve_flow_root`) está en un estatus de rol `ies`, toda transición sobre hijos se rechaza con el mensaje de esa raíz (`root_not_sent_message`, un atributo de clase en `AxisValue`, `GeneralPackage` y `GoodPracticePackage`, expuesto en sus serializers como `not_sent_message`). Enganchado en `validate_flow_transition` de `ObservableResponse`, `GroupResponse`, `GeneralGroupResponse` y `GoodPractice`; en el cliente, `flowStore.getRootNotInTurn` y `useFlowActions` con `options.root` pintan el candado con el motivo. Ricardo extendió la regla a gen y bp el 2026-09-23 ([[task-168]] punto 1): la revisora ya no puede aprobar un grupo de generales ni una práctica mientras su paquete siga en borrador.

### Consecuencias

- **Bueno:** la revisión empieza con el envío, como dice el hint; nada queda a medio dictaminar antes de la entrega.
- **Malo:** se pierde la revisión anticipada; en ejes grandes la revisora espera al envío completo.
- **Malo (resuelto el 2026-09-23):** la cola «En turno de la revisión» del encabezado del eje contaba grupos completados aunque el eje no se hubiera enviado; ahora, con el eje en turno de la IES, dice «N completados por la institución, eje sin enviar».

### Cómo se comprueba

`api/answer/tests.py::ObservableFlowRulesTests::test_reviewer_waits_for_the_axis_to_be_sent` y `test_reviewer_waits_on_the_observable_too`; `flow/tests/test_notifications.py` adaptado (el paquete bp se fuerza a `bp_sent`); los tests de regresión para gen y bp de la sesión del 23.

## Más información

[[2026-09-22-cierre-cuestionario-principal-captura-y-borrado]].
