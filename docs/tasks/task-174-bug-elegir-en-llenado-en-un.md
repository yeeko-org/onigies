---
type: task
id: task-174
title: "Bug: elegir «En llenado» en un grupo «Por iniciar» con cambios termina en error de transición"
state: open
date: 2026-09-23
owner: ricardo
parent: "[[task-2]]"
related: ["[[2026-09-23-reunion-ruben]]", "[[2026-09-23-sesion-meeting-reunion-con-ruben]]", "[[task-169]]", "[[task-166]]"]
---

# Bug: elegir «En llenado» en un grupo «Por iniciar» con cambios termina en error de transición

## Origen

Ricardo lo vio en vivo con Rubén el 23 de septiembre de 2026, [[2026-09-23-reunion-ruben]] `[17:39]`: «en guardar decía guardar “en llenado” y lo intentó guardar como si fuera de “completado”; hasta que no pongas todo esto como completado no te deja guardarlo como completado. Ahora ya me dejó». Creyó después que no era bug y pidió verificarlo con Playwright antes de abrir task. La verificación del mismo día (agente ejecutor con el MCP de Playwright, contra API :8018 y Nuxt :3018 locales, IES de prueba FP, observable 4.1 «Proceso de armonización normativa», eje No violencia) lo reproduce en parte: el bug existe, con otra mecánica de la que Ricardo describió.

## Lo observado

**Caso 1, el bug.** Grupo «Armonización e institucionalización» en «Por iniciar», 2 de 9 preguntas contestadas, en el menú «Guardar ▾» se elige la transición «En llenado». Salen dos peticiones:

1. `PATCH /api/group_response/2974/` con las dos respuestas → 200, `status: cp_filling`, FlowEvent `cp_pre_start → cp_filling`. Es la promoción automática del primer guardado (`auto_on_first_save`). La respuesta trae además `completion.errors` con 7 «Falta responder: …».
2. `POST /api/flow/answer/groupresponse/2974/transitions/` con `{"target_status": "cp_filling"}` → 400, `La transición de 'En llenado' a 'En llenado' no está permitida.`

En pantalla: snackbar de error con ese texto, el chip ya dice «En llenado», y una alerta roja «Para marcar este bloque como completado falta: …» con los 7 faltantes. Las respuestas sí quedaron guardadas, pero la IES ve un error y una lista roja que menciona «completado»: eso es lo que Ricardo leyó como «no me deja guardarlo».

**Caso 1b.** Mismo grupo «Por iniciar», sin cambios, elegir «En llenado»: solo sale el POST de transición → 201, snackbar «Estatus cambiado a “En llenado”». Es el probable «ahora ya me dejó»: al segundo intento ya no hay nada que guardar o el grupo ya está en llenado.

**Caso 2, sano.** Grupo ya en «En llenado», una respuesta nueva, «Guardar y mantener como En llenado»: PATCH → 200, snackbar «Cambios guardados», sin POST de transición. La alerta roja de completitud sigue visible aunque no bloquea.

**Caso 3, rechazo esperado.** Grupo en «En llenado» con huecos, «Marcar como completado»: PATCH → 200 y POST `cp_completed` → 400 con la lista de faltantes; el chip se queda en «En llenado». Correcto.

## Causa, desde el código

- `nuxt/app/components/dashboard/answer/capture/CpGroupCard.vue`, `saveAndTransition()` (~líneas 154-157): `if (dirty && !(await save())) return null; return kernel.onSelect(t)`. Manda la transición elegida en el menú, renderizado cuando el estatus aún era `cp_pre_start`, sin comparar con el estatus que devolvió el guardado.
- `nuxt/app/components/dashboard/flow/FlowSaveMenu.vue` (~57-66): el primer ítem es siempre «Guardar y mantener como {estatus actual}», que en «Por iniciar» no tiene sentido porque el guardado promueve de todos modos; debajo van las transiciones (`FlowTransitionMenu.vue` ~19-32, etiqueta `action_name || public_name`; `cp_filling` no tiene `action_name`).
- `api/api/views/answer/__init__.py` (~255-263): el PATCH del grupo llama `assign_auto_status`, y `api/flow/services.py` (~253-293) promueve del estatus `is_default` (`cp_pre_start`) al marcado `auto_on_first_save` (`cp_filling`; `cp_in_adjustment` también lo es). `services.py` ~82-85 rechaza cualquier transición ausente de `next_statuses`.
- `api/answer/group_validation.py` ~25 y ~199-213: `VALIDATED_TARGETS = ('cp_completed', 'cp_adjusted')`; solo esas transiciones validan completitud. Mantener «en llenado» nunca valida.

No verificado en navegador, mismo patrón probable: `cp_need_changes → cp_in_adjustment` al guardar con cambios y elegir «Iniciar ajustes». Tampoco se probaron los tipos B, alcance, planes ni especial; la lógica de guardado es la misma (`CpGroupCard`).

## Opciones (decisión de Ricardo)

1. Ocultar la transición `cp_filling` del menú cuando el grupo está en «Por iniciar» y renombrar el ítem principal (por ejemplo «Guardar avance»), porque el guardado ya promueve. Cambio solo de frontend; el menú deja de prometer algo que el backend hace solo.
2. En `saveAndTransition`, comparar `group.status` tras el guardado con `t.name` y omitir el POST si ya coincide. Cambio mínimo y general (cubre `cp_in_adjustment`), pero el menú sigue ofreciendo una opción redundante.
3. Dejar de promover en el PATCH (quitar `auto_on_first_save` del guardado) y que la transición sea siempre explícita. Cambia comportamiento de backend recién deployado y el backfill de `provision_cp_responses`; más caro.

Recomendación del coordinador: 2 como corrección inmediata y 1 como limpieza de UX en la misma task; 3 no.

## Alerta

El `v-alert type="error"` de `completion.errors` (`CpGroupCard.vue` ~267-280) se llena tras cada guardado y dice «Para marcar este bloque como completado falta:». Propuesta: tono informativo o warning por defecto, y rojo solo tras un intento rechazado de «Marcar como completado». Es UX, no bug; queda aquí para no perderlo.

## Datos que dejó la prueba en la base local

IES FP (usuario 80): observable 1012 (4.1) pasó a `cp_filling` con la inicial en «Sí»; GroupResponse 2974 en `cp_filling` con q178=Sí, q186=No, q183=Sí, q184=No; GroupResponse 2988 en `cp_filling` vacío; FlowEvents 444 y 445. No se revirtió.

El punto 11 de [[task-169]] describe este mismo bug y remite a esta task.

## Criterios de aceptación

- [ ] Ricardo elige la opción de arreglo (1, 2 o 3 de §Opciones)
- [ ] En un grupo «Por iniciar» con cambios sin guardar, elegir «En llenado» guarda las respuestas, deja el grupo en «En llenado» y muestra «Cambios guardados» sin snackbar de error
- [ ] Si el guardado ya promovió el estatus al destino de la transición elegida, no sale el POST de transición o el cliente lo trata como hecho
- [ ] Lo mismo vale para «Requiere ajustes» → «Iniciar ajustes» con cambios (cp_in_adjustment también es auto_on_first_save)
- [ ] La alerta de completitud tras un guardado no se lee como rechazo cuando la IES no pidió «completado» (decisión de UX aparte, ver §Alerta)
- [ ] Propuesta de test de regresión presentada a Ricardo (api/answer/tests.py o el e2e de cp de task-166)
- [ ] Revertir en la base local los datos que dejó la verificación (IES FP, observable 1012, GroupResponse 2974 y 2988, FlowEvents 444 y 445)
