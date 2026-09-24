---
type: decision
id: adr-0018
title: "Compuerta de respuesta del cuestionario principal: fecha del periodo y base validada, visible siempre, captura cerrada"
state: accepted
date: 2026-09-22
origin: ricardo
deliberation: dialogued
rationale: recorded
source: ["[[2026-09-22-cierre-cuestionario-principal-captura-y-borrado]]", "[[2026-09-04-reunion-con-ruben]]"]
affects: ["api/survey/cp_gate.py", "api/ies/models.py", "api/flow/permissions.py", "nuxt/app/components/dashboard/answer/capture/CpAxisCapture.vue"]
related: ["[[adr-0007]]", "[[adr-0009]]", "[[task-153]]", "[[task-168]]"]
---

# Compuerta de respuesta del cuestionario principal: fecha del periodo y base validada, visible siempre, captura cerrada

## Contexto y planteamiento del problema

[[adr-0007]] prometió que las IES no avanzan con los observables hasta tener validada su información base, y nada lo aplicaba en el código. [[task-153]] pidió que las IES vean el cuestionario completo sin poder responderlo hasta el 25 de septiembre, con fecha configurable y adelantable sin tocar código. Había que decidir un solo mecanismo para las dos cosas y qué significa «ver sin responder».

## Criterios de decisión

- Una IES pide sus datos una sola vez: necesita ver el cuestionario completo antes de poder capturar.
- Los denominadores (información base) quedan congelados antes de cualquier captura calificable.
- La apertura la mueve Rubén o Ricardo desde el admin, sin deploy.
- Las IES de prueba ven el cuestionario como lo verá cualquiera, pero no esperan la fecha (Ricardo, 2026-09-23, [[task-168]] punto 10).

## Opciones consideradas

- **Ocultar el cuestionario hasta que gen esté aprobado** (lectura literal de adr-0007). Descartada por Ricardo el 2026-09-22: se ven las preguntas, se inhabilita todo lo que implique captura.
- **Solo la fecha**, dejando adr-0007 sin mecanismo. Descartada: Ricardo la calificó de fundamental.
- **Fecha y base validada, en una sola compuerta del lado del servidor.** Elegida.

## Resultado

`Period.cp_open_at` (fecha-hora nula por defecto, editable en el admin y expuesta en el catálogo de periodos) y la condición de que el `GeneralPackage` de la IES esté en `gen_finished` (el estatus terminal del paquete; `gen_approved` es de los grupos). Mientras falte una, la IES **ve** todo el cuestionario y **no captura nada**: ni respuestas, ni el booleano inicial, ni transiciones, ni adjuntos. El API responde 403 con `code` `cp_not_open` o `gen_not_approved` y el survey expone `cp_capture {open, reason, open_at}` para que el frontend inhabilite los controles y explique el motivo. La compuerta vive en `api/survey/cp_gate.py`, enganchada en `validate_flow_transition` del eje, del observable y del grupo, en el gancho `content_lock_errors` de la raíz (que `user_can_edit_flow_content` consulta, así que cierra también los adjuntos) y en las vistas de captura. Las instituciones de prueba están exentas de la fecha `cp_open_at` pero no del prerrequisito `gen_finished` (Ricardo, 2026-09-23, cerrando el punto 10 de [[task-168]]; así `api/CLAUDE.md` y esta compuerta dejan de contradecirse); [[adr-0009]] sigue: ven la sección, no capturan.

### Consecuencias

- **Bueno:** adr-0007 tiene mecanismo; la fecha del 25 se mueve desde el admin; una sola fuente de verdad para IES y revisora.
- **Malo:** una IES con la base devuelta por la revisora no puede capturar observables aunque la fecha haya pasado; es la intención de adr-0007.
- **Malo:** la revisión no se ve afectada por la compuerta, así que puede parecer que «ya abrió» desde el dashboard cuando para la IES no.

### Cómo se comprueba

`api/answer/tests.py::CaptureGateTests` (las dos razones, `test_test_institution_skips_date_not_gen`, el bloqueo de adjuntos por `content_lock_errors`).

## Más información

[[2026-09-22-cierre-cuestionario-principal-captura-y-borrado]]. Publicar la sección a las IES reales sigue siendo la constante `PUBLISHED_SECTIONS` de `nuxt/app/utils/sections.js` (adr-0009).
