---
type: decision
id: adr-0020
title: Los grupos sin captura nacen en cp_approved y no salen de ahí
state: accepted
date: 2026-09-23
origin: ricardo
deliberation: dialogued
rationale: recorded
source: ["[[2026-09-23-diseno-de-la-captura-cp-y-decisiones-pendientes]]"]
affects: ["api/answer/models.py", "api/answer/services.py", "api/flow/seed.py", "api/answer/management/commands/provision_cp_responses.py", "nuxt/app/components/dashboard/answer/capture/CpGroupCard.vue"]
related: ["[[adr-0017]]", "[[adr-0018]]", "[[task-168]]"]
---

# Los grupos sin captura nacen en cp_approved y no salen de ahí

## Contexto y planteamiento del problema

Cada observable tiene un `GroupResponse` por tipo de pregunta que le aplica, incluido «Distribución de población» (`QuestionType.population`), cuyo dato se captura en Información base y se califica en el observable: no hay nada que llenar ni revisar en ese grupo. Hasta el 23 de septiembre nacía en `cp_pre_start` y el «Sí» a la pregunta inicial lo promovía a `cp_filling` junto con los demás; en la interfaz mostraba módulo de estatus, comentarios y evidencia como cualquier grupo. Ricardo, al ver la captura: «No tiene sentido que tenga status, o lo ideal en todo caso es que tenga el mismo o el equivalente que preguntas generales cuando estas se aprueban. No hay nada nuevo que validar que no se haya validado ya.»

## Criterios de decisión

- Que el grupo no pida acciones a la IES ni a la revisora.
- Que no bloquee ni distorsione el estatus agregado del observable.
- Sin estatus nuevo que explicar en catálogo, propagación y filtros.

## Opciones consideradas

- **Nacer en `cp_approved` al provisionar.** Elegida. Terminal en la práctica gracias a una guarda, porque `cp_approved` tiene rol IES y una salida («Solicitar reajuste») que aquí no tiene sentido.
- **Un estatus propio «sin captura», sin rol.** Descartada por Ricardo («creo que no») y por el modelo: un caso único que dice lo mismo que «Aprobado».
- **Nacer en «Por iniciar» y finalizar cuando se apruebe Información base.** Más exacta en teoría, pero como `gen_finished` es prerrequisito para que la IES vea cp ([[adr-0018]]), el grupo siempre estaría ya finalizado cuando alguien lo mira: maquinaria extra sin efecto visible.

## Resultado

El criterio «sin captura» es `QuestionType.model_response IS NULL` (hoy solo `population`; [[task-168]] punto 6). Esos grupos nacen en `cp_approved` al provisionar (`answer.models.provision_cp_responses`) y `provision_cp_responses --apply` mueve ahí los existentes en «Por iniciar» o «En llenado» (`approve_groups_without_capture`, idempotente, sin `FlowEvent`). `GroupResponse.validate_flow_transition` rechaza toda salida de `cp_approved` para un grupo sin captura («Este bloque no lleva captura ni revisión: su dato se registra en la información base.»). `cp_approved` entra a las reglas de hijos válidos de `cp_completed`, `cp_postponed`, `cp_partial` y `cp_partial_approved`; la guarda del «No» ([[adr-0017]]) no cuenta a los grupos sin captura como revisión activa; al salir de «No», `assign_status_tree` los regresa a `cp_approved` y no a `cp_filling`. En la interfaz el grupo muestra solo el chip de estatus y el aviso que remite a Información base: sin módulo de estatus, comentarios ni evidencia.

### Consecuencias

- **Bueno:** la IES no ve acciones sobre algo que no capturó; el observable se completa con sus grupos reales.
- **Malo:** «Aprobado» significa aquí «no aplica revisión», no «la revisión validó»; la guarda y el hint lo explican, pero el catálogo no lo distingue.
- **Deploy:** exige `seed_flow` antes del backfill ([[task-163]]).

### Cómo se comprueba

`api/answer/tests.py`: `test_groups_without_capture_stay_approved`, los tests de regresión del 23 sobre el backfill y las reglas de hijos, y un test de la guarda (un `cp_voluntary_readjust` sobre el grupo población devuelve `WITHOUT_CAPTURE_MESSAGE`) que el ejecutor agrega en el cierre de la sesión.

## Más información

[[2026-09-23-diseno-de-la-captura-cp-y-decisiones-pendientes]].
