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
affects: ["api/answer/services.py", "api/answer/models.py", "nuxt/app/composables/useFlowActions.js", "nuxt/app/store/flow.js"]
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

`answer/services.py::review_turn_errors`: si el usuario es revisora y el eje está en un estatus de rol `ies`, toda transición sobre observables y grupos se rechaza con «El eje aún no se ha enviado a revisión…». Enganchado en `validate_flow_transition` de `ObservableResponse` y `GroupResponse`; en el cliente, `flowStore.getRootNotInTurn` y `useFlowActions` con `options.root` pintan el candado con el motivo. Aplica solo a cp. Extenderla a gen y bp, donde hoy la revisora puede aprobar un grupo o práctica con el paquete en borrador, queda como decisión abierta de Ricardo.

### Consecuencias

- **Bueno:** la revisión empieza con el envío, como dice el hint; nada queda a medio dictaminar antes de la entrega.
- **Malo:** se pierde la revisión anticipada; en ejes grandes la revisora espera al envío completo.
- **Malo:** la cola «En turno de la revisión» del encabezado del eje sigue contando grupos completados aunque el eje no se haya enviado (pendiente).

### Cómo se comprueba

`api/answer/tests.py::ObservableFlowRulesTests::test_reviewer_waits_for_the_axis_to_be_sent` y `test_reviewer_waits_on_the_observable_too`.

## Más información

[[2026-09-22-cierre-cuestionario-principal-captura-y-borrado]].
