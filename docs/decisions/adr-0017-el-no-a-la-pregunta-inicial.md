---
type: decision
id: adr-0017
title: "El «No» a la pregunta inicial vale cero, es terminal y no se revisa: estatus cp_not_present para observable y grupos"
state: accepted
date: 2026-09-22
origin: ricardo
deliberation: dialogued
rationale: recorded
source: ["[[2026-09-22-cierre-cuestionario-principal-captura-y-borrado]]"]
affects: ["api/flow/seed.py", "api/answer/services.py", "api/answer/models.py", "nuxt/app/components/dashboard/answer/capture/CpObservablePanel.vue"]
related: ["[[adr-0016]]", "[[adr-0010]]", "[[task-28]]"]
---

# El «No» a la pregunta inicial vale cero, es terminal y no se revisa: estatus cp_not_present para observable y grupos

## Contexto y planteamiento del problema

Cada observable del cuestionario principal abre con una pregunta inicial sí/no (`Observable.init_question`, «¿La IES cuenta con…?»); el instrumento 2024 y el 2026 dicen «No (pasar a la pregunta del siguiente observable)». Al construir la captura había que decidir qué es un «No» para el índice y para el flujo de revisión, y qué pasa con los grupos de respuesta (`GroupResponse`) del observable, que existen desde la creación de la institución (eager) y tienen estatus propio. Sin regla, un observable en «No» no podía completarse (la regla de hijos exige sus grupos completados), un eje podía enviarse con observables «pospuestos» sin tocar, y un grupo devuelto por la revisora quedaba varado si la IES cambiaba a «No».

## Criterios de decisión

- Que el índice mida distancia al estado deseable: no tener la medida no es «no aplica», es la distancia máxima.
- No irritar a Rubén ni a las IES con revisiones de una ausencia declarada.
- Que el motor de flujo vea el estado sin filtros implícitos repartidos por consultas, colecciones y ETL.
- Reversibilidad barata: Rubén prevé el «pienso que no, pero le abro y sí tengo sala» (reunión del 4 de septiembre).

## Opciones consideradas

- **Dejar los grupos tal cual y filtrar por `ObservableResponse.value`** en cada consulta. Más barato de construir; regla implícita que se olvida (lección de gen) y grupos devueltos que siguen al tope de la cola por prioridad.
- **Estatus terminal propagado a los grupos**, al estilo de `bp_discarded`: visible, autocontenido, reversible.
- **Un estatus «no aplica»**, además del «No». Descartado: el análisis de los 41 observables del 2026-09-22 (Fable, sobre el texto real de las preguntas iniciales y el padrón de 66 IES) no encontró ninguno que una IES mexicana pueda responder legítimamente como «no aplica»; el único candidato con argumento sustantivo es el 1.14 (investigación con perspectiva de género) en una IES sin función de investigación, y va a la reunión con Rubén. Todo lo parcial (IES sin bachillerato, sin posgrado, sin cuerpo colegiado) ya se declara en Información de base (`is_present`, `no_apply`).

## Resultado

El «No» **vale 0, entra al promedio, es terminal y no se revisa**. Un solo estatus nuevo, `cp_not_present` (nombre público «Sin la medida» y color `blue-grey` desde el 2026-09-23, antes «No cuenta con la medida» y gris —[[2026-09-23-diseno-de-la-captura-cp-y-decisiones-pendientes]]—; ícono `block`, sin rol, sin `next_statuses`), aplica a observable y a grupo. Al guardar `value=False`, el dominio (`answer/services.py::set_init_value`, con `flow.services.assign_status_tree`) lleva el observable y todos sus grupos a ese estatus, con un `FlowEvent` por objeto; las respuestas tipadas ya capturadas se conservan. Salir de «No» (a «Sí» o a sin responder) regresa el árbol a `cp_filling`; ese cambio solo se dispara desde el observable. El cambio a «No» se bloquea mientras algún grupo tenga revisión activa (`cp_need_changes`, `cp_in_adjustment`, `cp_adjusted`, `cp_approved`, `cp_partial`, `cp_partial_approved`; desde [[adr-0020]] los grupos sin captura no cuentan); el arrepentimiento tras aprobación va por `cp_voluntary_readjust` del eje. `cp_not_present` cuenta como hijo válido para completar, enviar, aprobar, reenviar, ajustar, parcial y necesita cambios. Un observable sin responder (`value=None`) no puede completarse. Se cerró de paso el hueco de «pospuesta»: `cp_postponed` exige grupos en completado, pospuesta, parcial o no cuenta.

No existe «no aplica» a nivel observable. Si Rubén decide otra cosa para el 1.14, esa excepción se resuelve en el cálculo (task-28), no con un estatus.

### Consecuencias

- **Bueno:** la revisora ve el «No» cerrado sin nada que validar; el motor y las colecciones no necesitan filtros; el «No» es reversible sin perder captura.
- **Malo:** un «No» de una IES que sí podría tener la medida cuenta 0 sin que nadie lo cuestione; es el diseño del instrumento, no de la plataforma.
- **Malo:** las reglas 0/0 de calificación (especial del 1.14 con cero proyectos, B administrativa con cero instancias) siguen sin definir; no dependen de este estatus.

### Cómo se comprueba

`api/answer/tests.py`: `InitValueTests` (el «No» mueve el árbol con eventos y conserva respuestas; la vuelta a «Sí»; el bloqueo con revisión activa) y `ObservableFlowRulesTests` (`cp_postponed` exige grupos resueltos; `cp_not_present` como hijo válido). `seed_flow` crea el estatus.

## Más información

Sesión del 2026-09-22: [[2026-09-22-cierre-cuestionario-principal-captura-y-borrado]]. La pregunta del 1.14 y la unidad de análisis en IES no autónomas van en la agenda con Rubén.
