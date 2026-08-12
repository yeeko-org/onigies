---
type: task
id: task-67
title: Indicar visualmente que un campo de captura es numérico
state: closed
date: 2026-08-06
owner: ai
parent: "[[task-41]]"
source: ["[[2026-08-06-temas-reunion-fer]]"]
---

# Indicar visualmente que un campo de captura es numérico

§7 de la reunión con Fernanda, `[13:34]`–`[14:14]`. Fernanda intentó escribir texto en un campo y no la dejó. Ricardo confirmó que el campo está definido como numérico, pero **nada lo indica visualmente**: no hay etiqueta ni los controles de incremento/decremento típicos de un `input type="number"`. La usuaria descubre la restricción al chocar con ella.

Salió en la captura de la información base (`nuxt/app/components/dashboard/survey/GeneralNumberQuestion.vue`), pero la decisión de cómo señalar un campo numérico conviene tomarla una sola vez y aplicarla a toda la captura, no solo a generales.

## Análisis hecho, decisión pendiente (2026-08-06)

La sesión duo ([[2026-08-06-sesion-duo-adjuntos-sobre-flow-y]]) produjo el análisis UX completo. Hallazgos clave: `v-number-input` no usa `type="number"` (renderiza texto), fija `inputmode="decimal"` — incorrecto para enteros —, no anuncia nada a lectores de pantalla y sus spinners son `aria-hidden` (reactivarlos solo señala a vidente-con-ratón); 26 de los 31 campos numéricos viven en tablas densas sin espacio para hints, y los años de BP usan otro idioma (`v-text-field type="number"` nativo). **Recomendación:** ícono `123` en `prepend-inner` + `inputmode="numeric"` + texto sr-only vía `aria-describedby`; alternativa: placeholder «p. ej. 1250» con `persistent-placeholder`. La elección es de Ricardo y quedó batcheada en [[task-93]]; la aplicación consistente se ejecuta al resolverse.

## Cierre (2026-08-11): no habrá señal visual

Veredicto de Ricardo, tomado con criterio visual propio tras probar las dos alternativas que salieron del análisis: **el campo numérico va «bien pelón»**. El ícono `123` se probó y se descartó; el `tag` (#) se aplicó después y se descartó también. No queda ninguna señal en el campo y no se busca una tercera.

Lo que resuelve el problema original —que Fernanda descubriera la restricción al chocar con ella— es otra cosa: **el `label` corto del campo ayuda en las preguntas donde lo que se cuenta no son personas** («Planes», «Instancias»), y sobre todo **las instrucciones claras del bloque**, que a partir de [[task-107]] y [[task-108]] serán editables por el equipo de Rubén en vez de vivir en el código.

Rubén vio la captura en la demo del 11 de agosto y dio validación global de la sección. La task se cierra: la pregunta que la abrió está respondida, aunque la respuesta sea que no se señala nada.

Nota para quien lea el histórico: la primera implementación y su rediseño viven en [[task-93]] y [[task-96]]; el veredicto sobre los íconos se registró en esta última.

## Criterios de aceptación

- [x] Decidido cómo se señala un campo numérico: no se señala, y la carga la llevan el `label` y las instrucciones del bloque
- [x] El criterio elegido se aplica de forma consistente en toda la captura: no hay señal en ninguna parte, así que no hay inconsistencia que corregir
