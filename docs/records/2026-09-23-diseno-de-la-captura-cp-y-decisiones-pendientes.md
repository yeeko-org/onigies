---
type: record
id: 2026-09-23-diseno-de-la-captura-cp-y-decisiones-pendientes
date: 2026-09-23
parent: "[[task-2]]"
---

# Sesión del 23 de septiembre: diseño de la captura cp y las decisiones pendientes de ayer

Sesión de diálogo largo con Ricardo (session log `a7383a8d-28d4-4b8d-9391-a19b8bde2000`), en la rama `cp-backend`, sin deploy. Dos objetivos: ajustar el diseño de la vista `/respuestas/{year}` construida el 22 ([[2026-09-22-cierre-cuestionario-principal-captura-y-borrado]]) y resolver las trece decisiones de [[task-168]]. Ricardo pidió agrupar temas en pocos intercambios y dividir el trabajo en dos tandas; cada tanda salió a dos ejecutores Opus 5.5 en paralelo (frontend y backend) mientras el diálogo seguía. Ricardo se fue antes del cierre y dejó las decisiones que faltaban en [[task-169]].

## Primera tanda (decisiones cerradas por Ricardo al abrir, más el diálogo medio)

- La pestaña cp lleva el mismo `v-card` que Información base y Buenas prácticas (título con ícono, nombre, estatus y comentarios; descripción del eje en cursiva).
- Cero franjas laterales en toda la app: se retiraron `.cp-bar`, el `border-left` de los hints de flujo, los `v-alert border="start"` y el `border="end"` de `AlertInfo`. Única excepción, por decisión de Ricardo: los bloques por tipo de pregunta del detalle de observable del dashboard. Regla nueva en `nuxt/CLAUDE.md`, junto con «reutilizar antes de construir».
- Header del observable con la lógica del dashboard (`TitleCommon` a 520 px, dos líneas y tooltip; ícono de respuesta inicial, chip `x-small` e íconos por grupo pegados al título). Ícono `pending` cuando no hay respuesta.
- Sí/No como radios: componente compartido nuevo `YesNoRadio` (etiqueta ≤560 px a la izquierda, columna fija de radios a la derecha, siempre horizontal, Sí-No, `readonly` y `disabled` separados) para la pregunta inicial y las AQuestion. No existía ningún patrón previo: la tabla de todos los Sí/No de la app, actualizada, está en [[task-169]]. Sin «No aplica» en las A por ahora ([[task-164]]).
- Notas del instrumento como caption con ícono `info`, sin `v-alert`. Jerarquía de chips: eje `large`, observable `default`, grupo `small` tonal.
- Guardar por grupo con el split-button de gen/bp («Guardar y mantener como …» + transiciones), extraído a `FlowSaveMenu`; la IES ve el chip de solo lectura salvo en «Pospuesta» y «Aprobado» ([[task-169]] punto 1). Comentarios arriba, junto al chip; la tarjeta amarilla solo cuando hay comentarios reales (antes, cualquier evento de flujo la mostraba como «Comentarios (0)»).
- Secciones del grupo: cabecera (ícono neutro, nombre, chip, comentarios), divider, pregunta en `font-weight-medium` sin divider con la lista, divider y «Evidencia probatoria». Nada de `type.color` en `/respuestas`: manda el color del estatus. Mensajes de completitud con `v-alert` tonal como gen; sin hex sueltos.
- «Sin archivos adjuntos» y «Comentar» solo cuando es editable. El grupo «Distribución de población» solo con chip ([[adr-0020]]). Pregunta especial 1.14: «Total proyectos» / «Dirigidos por mujeres»; sin «No aplica» en el 1.14, consistente con lo hablado con Rubén ([[2026-09-23-reunion-ruben]]).
- Backend: [[task-168]] puntos 1, 10 y 11; frontend: puntos 2, 8 y 9 (ver ahí). Los ejes en orden natural y sin fechas de apertura por eje son consistentes con la reunión con Rubén.

## Segunda tanda (diálogo profundo)

- **Gris:** regla «gris puro = nada ha pasado». «Por iniciar» `grey-lighten-1`; `cp_not_present` se llama «Sin la medida» y es `blue-grey` (enmienda a [[adr-0017]]); «Finalizado» de gen y bp `green-darken-2`. Los íconos de respuesta inicial toman su color del catálogo: `toggle_off` el de «Sin la medida», `pending` el de «Por iniciar».
- **Expansion-panels como el dashboard, opción A:** título del observable teñido con el color del eje en `lighten-5`, cuerpo blanco, cards de grupo con sombra (`elevation="2"`; se probó primero el borde suave y la reunión con Rubén del mismo día lo cambió a sombra). La opción B (fondo de página `neutral-50` del design system) queda para [[task-38]].
- **«Te toca» solo en el eje.** En observable y grupo el hint va al tooltip del chip con un ícono `flag` cuando es el turno del usuario (`FlowStatusActions` prop `hint: box|tooltip`). Se retiró el módulo de estatus inferior del observable; queda el superior con «Sí». Hints con tokens del tema, sin hex.
- **Ancho, opción 1:** el contenido del panel del observable en una columna de 900 px; la vista sigue fluida. Ricardo descartó las dos columnas y dejó el tope global para después.
- **Tooltip por grupo:** campo nuevo `QuestionType.description` (migración `question.0011` con seis textos borrador, editable en el dashboard) mostrado con un botón `info` junto al nombre del grupo. Cubre lo que Rubén no vio en el ícono de info durante la reunión ([[2026-09-23-reunion-ruben]]); él revisará los textos.
- Más aire en los radios (columna 180 px, gap de 16 px, filas `py-2`). Badges de estatus en los íconos por grupo: probados y rechazados por Ricardo («horribles»), revertidos.
- Restos de gen/bp: `root` en la vista de la revisora del paquete bp, texto del candado por raíz (`not_sent_message`), evidencia oculta cuando no hay archivos ni edición, adopción de `FlowSaveMenu`.

## Verificación

API: 142 tests antes de los de regresión del cierre; `makemigrations --check` limpio con `question.0011`. Nuxt: 9 unitarios; Playwright 39/39 con `--workers=2` y 37/39 con los workers por defecto por dos fallos en `gen-capture`; que sean preexistentes es hipótesis: la prueba con HEAD solo restauró `GeneralGroupPanel.vue` y no aisló `GeneralPopulations.vue`, `FlowSaveMenu` ni los componentes de flow ([[task-169]]). La migración `question.0011` quedó aplicada en la base local por el ejecutor (solo agrega una columna; reversible); `seed_flow` no se corrió localmente. Regresión nueva del deep-link en `respuestas-tabs.test.ts`, probada contra HEAD. Capturas de pantalla con payload mockeado; no se probó contra el API real (el ejecutor no pudo leer el token del usuario de prueba). Backfill en dry-run local: 66 grupos.

## Bug conocido en el código de hoy, no corregido

Verificado con Playwright por la sesión de meeting contra el API real: en un grupo «Por iniciar» con cambios sin guardar, elegir «En llenado» en el split-button hace el PATCH (el backend ya promueve solo a `cp_filling` por el auto-estatus del primer guardado) y luego el POST de transición `cp_filling → cp_filling`, que el API rechaza con 400 «La transición de 'En llenado' a 'En llenado' no está permitida». Los cambios sí se guardan, pero la IES ve un snackbar de error. Causa: `CpGroupCard.vue` `saveAndTransition()` manda la transición elegida sin comparar con el estatus que devolvió el guardado; mismo patrón probable en `cp_need_changes → cp_in_adjustment`. Además, el `v-alert` de `completion.errors` aparece tras cualquier guardado y se lee como rechazo aunque no se pidió «completado». Tres opciones anotadas: ocultar la transición automática en el menú, comparar estatus tras el guardado y saltar la transición ya alcanzada, o no promover en el PATCH; la elección es de Ricardo y la task con la evidencia la abre la sesión de meeting. **La suite verde no cubre este caso: no darlo por sano.** La prueba dejó datos en la base local (IES FP, observable 4.1 en `cp_filling` con 4 respuestas).

## Desviaciones del coordinador

- Editó `api/CLAUDE.md` (la frase sobre IES de prueba y la compuerta) y una línea de `CpGroupCard.vue` (sombra en las cards de grupo) sin ok explícito de Ricardo.
- Las decisiones sobre el tamaño del chip del observable y el default «Sí» en `is_present` se habían reabierto por error en [[task-169]]; retiradas.

## Pasos de deploy pendientes (para task-163)

El orden del API, después del dump, pasa a ser:

1. `migrate`: incluye `question.0011`, que agrega `QuestionType.description` y siembra los seis textos borrador solo donde esté vacío.
2. `seed_flow`: aplica los colores nuevos («Por iniciar» `grey-lighten-1`, «Finalizado» `green-darken-2`), la etiqueta «Sin la medida» con color `blue-grey` para `cp_not_present`, y las reglas de hijos que aceptan `cp_approved` en «Completado», «Pospuesta», «Parcial» y «Parcialmente aprobado». Sin este paso las reglas nuevas no existen y el paso 3 deja grupos aprobados que el observable no reconoce.
3. `provision_cp_responses` en dry-run (comparar conteos) y luego `--apply`: además de provisionar, mueve a `cp_approved` los grupos sin captura («Distribución de población») que estén en «Por iniciar» o «En llenado» (localmente 66). Sin el backfill, un «Sí» ya no promueve esos grupos y un grupo en «Por iniciar» impide completar el observable ([[adr-0020]]).
4. `supervisorctl restart apionigies`.

## Fuera de la sesión

Deploy ([[task-163]], con los pasos nuevos), [[task-114]] abierta con cp como candidata, [[task-164]] ampliada con la revisión de «No aplica» en las AQuestion, el default «Sí» en `is_present` de poblaciones se deja como está (Ricardo, 23-sep). La reunión con Rubén del mismo día (14:49) manda sobre lo decidido aquí; su record es [[2026-09-23-reunion-ruben]] y de ahí salen los retoques de la captura cp y el análisis conjunto de dictamen y transversalidad.
