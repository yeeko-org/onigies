---
type: task
id: task-169
title: Decisiones pendientes de Ricardo tras el diseño cp del 23 de septiembre
state: open
date: 2026-09-23
owner: ricardo
parent: "[[task-2]]"
source: ["[[2026-09-23-diseno-de-la-captura-cp-y-decisiones-pendientes]]"]
related: ["[[task-168]]", "[[adr-0020]]"]
---

# Decisiones pendientes de Ricardo tras el diseño cp del 23 de septiembre

Lo que la sesión del 23 de septiembre ([[2026-09-23-diseno-de-la-captura-cp-y-decisiones-pendientes]]) dejó abierto porque es llamado de Ricardo. Cada punto trae lo que es la pieza, por qué está en duda y la recomendación del modelo; nada de esto está implementado salvo donde se dice «hoy».

1. **Menú del chip para la IES en «Pospuesta» y «Aprobado».** Se acordó que la IES ve el chip de estatus del grupo solo como etiqueta y actúa por el botón «Guardar ▾» (`FlowSaveMenu`). Ese botón solo existe cuando el grupo es editable, y en «Pospuesta» (puede retomar y completar) y «Aprobado» (puede solicitar reajuste) no lo es. Hoy el chip conserva su menú en esos dos estatus. Opciones: dejarlo (recomendado; gen y bp no tienen esos estatus) u otro activador.
2. **Ver la línea de tiempo del estatus sin comentarios.** La tarjeta amarilla de comentarios (que abre el diálogo con comentarios e historia de estatus) aparece solo cuando hay comentarios reales (decisión del 23). Con cero comentarios y sin turno no hay forma de abrir la historia. Opciones: ícono `history` pequeño junto a comentarios en eje, observable y grupo, que abra el mismo diálogo en modo lectura (recomendado si la historia le sirve a la IES), o dejarlo.
3. **Orden de los paquetes gen y bp en el dashboard.** Los ejes pasaron a orden natural; los listados de `GeneralPackage` y `GoodPracticePackage` del dashboard siguen por urgencia (`ordering = ['-status__priority', 'id']`). Opciones: dejarlos (es una lista de trabajo para la revisora) o orden natural también.
4. **Contraste del ícono `pending`.** El ícono de «sin responder» toma el color de «Por iniciar», ahora `grey-lighten-1`, sobre el título teñido `lighten-5` del eje: ~1.8:1, por debajo del 3:1 de WCAG 1.4.11 para elementos con significado. Opciones: un gris más oscuro en el catálogo para «Por iniciar», o contorno en el ícono.
5. **Ancho global de `/respuestas`.** Se aplicó la opción 1 (cuerpo del panel del observable a 900 px). Ricardo descartó la opción 2 (dos columnas) y dejó la 3 (`v-container` no fluido para toda la vista, afecta gen y bp) para pensarla «con calma».
6. **`gen-capture.test.ts` falla con los workers por defecto de Playwright** («el tri-estado gobierna los conteos…» y «las poblaciones estructurales…»), y pasa sola y con `--workers=2`. Hipótesis de que es preexistente: la prueba con HEAD solo restauró `GeneralGroupPanel.vue`; siguen sin aislar `GeneralPopulations.vue` (edición manual de Ricardo), `FlowSaveMenu` y los componentes de flow. La captura del fallo muestra «Forma de gobierno» abierto y Poblaciones no visible: apunta al orden de apertura de paneles bajo carga o a `GeneralPopulations.vue`. Opciones: investigar `GeneralGroupList`, fijar `workers` en `playwright.config.ts`, o dejarlo.
7. **Adoptar `YesNoRadio` en gen y bp.** Candidatos reales: la pregunta de población no binaria en gen y `has_good_practices` en bp (radio vertical, sin `color="accent"`). `FeatureItem.vue` usa `disabled` donde el resto usa `readonly` (mismo problema de contraste que el punto 7 de [[task-168]]). Ricardo lo dejó para después de ver el componente en cp.
8. **La bandera «Te toca» no es enfocable.** El ícono `flag` junto al chip lleva `aria-label` pero no recibe foco; con teclado el hint solo llega por el tooltip del chip. Opción: `aria-describedby` del chip al texto del hint.
9. **Etiquetas de la pregunta especial hardcodeadas.** «Total proyectos» / «Dirigidos por mujeres» viven en `CpQuestionsSpecial.vue` porque la única pregunta especial de la siembra es 1.14. Una pregunta especial creada desde el dashboard con otro sujeto las heredaría.
10. **Revisar con Rubén los seis textos de `QuestionType.description`** (sembrados por `question.0011` como borrador; editables en el dashboard). En la reunión del mismo día ([[2026-09-23-reunion-ruben]]) Rubén quedó en revisarlos; lo cubre [[task-171]]; este punto se cierra por duplicado. Los grupos: Armonización e institucionalización, Transversalidad orgánica, Transversalidad sectorial, Planes de estudio, Pregunta especial, Distribución de población.
11. **Transición redundante tras el primer guardado** (bug, no decisión de diseño): elegir «En llenado» en el split-button de un grupo «Por iniciar» con cambios guarda bien pero el POST de transición `cp_filling → cp_filling` da 400 y la IES ve error; el alert de completitud aparece tras cualquier guardado. Detalle, evidencia y las tres opciones de arreglo en [[task-174]]; aquí solo la elección.

## Aplicado sin tu voto, pendiente de tu validación

- gen y bp adoptan `FlowSaveMenu` (unas 80 líneas duplicadas menos); el subtítulo «Evidencia probatoria» se oculta en gen y bp cuando no hay archivos ni edición; el texto del candado «aún no se ha enviado» ahora viene por raíz (`not_sent_message`). bp no tiene e2e que lo cubra.
- La comparación exhaustiva cp vs gen/bp/dashboard que pediste para validar no se entregó como tal; lo que se reutilizó y lo que quedó nuevo está en el record; queda pendiente como análisis.

## Hallazgos de los ejecutores que no llegaron a ningún nodo

- Descubribilidad del «Guardar ▾»: una IES puede no encontrar «Marcar como completado» dentro del menú del botón (relacionado con [[task-174]]).
- Área de toque de los radios `compact`: ~40 px, por debajo de los 44 recomendados.
- La colección GoodPractice del dashboard monta `GoodPracticeEditSimple` sin paquete, así que la revisora no ve el candado hasta el 400.
- Tras el fix del deep-link, un usuario staff en `/respuestas` sin `ies_data` ve la barra de progreso indefinida, igual que cualquier IES cuyo perfil o catálogos fallen.
- El prefijo «Error:» solo va en la primera línea de un error multilínea.

## Todos los Sí/No de la app (para corroborar)

| Lugar | Control | Ancho | Orientación | readonly / disabled |
|---|---|---|---|---|
| cp, pregunta inicial del observable | `YesNoRadio` booleano | etiqueta ≤560 px, radios 180 px | horizontal, Sí-No | readonly sin turno; disabled con compuerta cerrada o guardando |
| cp, cada fila A | `YesNoRadio` con ids de la escala global | igual | horizontal, Sí-No | readonly si no es editable; disabled en consulta previa o con compuerta cerrada |
| gen, «¿mide población no binaria?» | `v-radio-group inline` | sin ancho | horizontal | readonly |
| gen, «Está presente» por sector | `v-select` Sí/No en celda de tabla | 120 px, `solo-inverted` (cambio manual de Ricardo) | desplegable | readonly |
| gen, forma de gobierno | radio vertical de dos opciones largas | ancho completo | vertical | readonly |
| gen, sexo de la titular | radio inline Mujer/Hombre/(No binaria) | sigue al texto | horizontal | readonly |
| bp, `has_good_practices` | `v-radio-group` | 680 px | vertical, sin accent | no se pinta si no puede editar |
| bp, `FeatureItem` | `v-checkbox` | — | — | disabled (no readonly) |

## Criterios de aceptación

- [ ] Cada punto tiene respuesta registrada aquí o convertido en task propia
