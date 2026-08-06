---
type: task
id: task-67
title: Indicar visualmente que un campo de captura es numérico
state: open
date: 2026-08-06
owner: ai
parent: "[[task-41]]"
source: ["[[2026-08-06-temas-reunion-fer]]"]
---

# Indicar visualmente que un campo de captura es numérico

§7 de la reunión con Fernanda, `[13:34]`–`[14:14]`. Fernanda intentó escribir texto en un campo y no la dejó. Ricardo confirmó que el campo está definido como numérico, pero **nada lo indica visualmente**: no hay etiqueta ni los controles de incremento/decremento típicos de un `input type="number"`. La usuaria descubre la restricción al chocar con ella.

Salió en la captura de la información base (`nuxt/app/components/dashboard/survey/GeneralNumberInput.vue`), pero la decisión de cómo señalar un campo numérico conviene tomarla una sola vez y aplicarla a toda la captura, no solo a generales.

## Análisis hecho, decisión pendiente (2026-08-06)

La sesión duo ([[2026-08-06-sesion-duo-adjuntos-sobre-flow-y]]) produjo el análisis UX completo. Hallazgos clave: `v-number-input` no usa `type="number"` (renderiza texto), fija `inputmode="decimal"` — incorrecto para enteros —, no anuncia nada a lectores de pantalla y sus spinners son `aria-hidden` (reactivarlos solo señala a vidente-con-ratón); 26 de los 31 campos numéricos viven en tablas densas sin espacio para hints, y los años de BP usan otro idioma (`v-text-field type="number"` nativo). **Recomendación:** ícono `123` en `prepend-inner` + `inputmode="numeric"` + texto sr-only vía `aria-describedby`; alternativa: placeholder «p. ej. 1250» con `persistent-placeholder`. La elección es de Ricardo y quedó batcheada en [[task-93]]; la aplicación consistente se ejecuta al resolverse.

## Criterios de aceptación

- [ ] Un campo numérico se reconoce como tal antes de intentar escribir en él
- [ ] El criterio elegido se aplica de forma consistente en toda la captura, no solo en la información base
