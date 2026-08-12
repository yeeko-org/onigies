---
type: record
id: 2026-08-12-fix-del-colapso-del-alias-vcountinput
title: "Fix del colapso del alias VCountInput: inline-grid en vez de d-inline-flex"
date: 2026-08-12
related: ["[[2026-08-12-sesion-orquestada-a-b-captura-correcta]]", "[[2026-08-09-sesion-task-93-y-drift-del-harness]]"]
---

# Fix del colapso del alias VCountInput: inline-grid en vez de d-inline-flex

Tras la sesión [[2026-08-12-sesion-orquestada-a-b-captura-correcta]] apareció un bug de layout en todos los `v-count-input` (alias nacido en [[2026-08-09-sesion-task-93-y-drift-del-harness]]): el campo visible colapsaba a ~55 px aunque la caja exterior respetara el `width` pedido (120 px en las matrices, 160 px en el renglón numérico). Un primer intento (Opus 4.8) no encontró la causa y dejó un parche local `:deep` en `GeneralNumberQuestion.vue`; esta sesión lo revirtió y arregló la raíz.

## Diagnóstico

`.v-input` de Vuetify 3 no es un flex: es `display: grid` con `grid-template-columns: max-content minmax(0,1fr) max-content`, y el control llena el ancho gracias al track `minmax(0,1fr)`. La utilidad `d-inline-flex` que el alias ponía en sus defaults (para que el `text-align` de la celda posicionara el campo en las tablas matriz) destruye ese grid con `!important`: los hijos pasan a flex items con `flex: 0 1 auto` y `.v-input__control` se encoge al contenido — con etiqueta flotante (absoluta, sin ancho propio), el colapso es total.

## Decisión

Conservar la intención (caja inline posicionable por `text-align`) sin romper el layout interno: regla global `.v-count-input { display: inline-grid; }` en `nuxt/app/assets/styles/main.css`, junto al `text-align: right` del alias que ya vivía ahí. Se descartaron los parches `:deep(.v-input__control)` por componente (curan el síntoma en un solo lugar y pelean contra internals de Vuetify) y el wrapper component (prohibido por convención del CLAUDE.md de nuxt: las convenciones transversales viven en defaults/aliases, no en envolturas).

## Cambios

`nuxt/app/plugins/vuetify.ts` (el default `class` del alias queda en `v-count-input`, sin `d-inline-flex`), `nuxt/app/assets/styles/main.css` (la regla `inline-grid` con su porqué), y `nuxt/app/components/dashboard/survey/GeneralNumberQuestion.vue` (se elimina el parche `:deep` y la clase `general-question__count`). Ricardo verificó el fix directamente en el navegador en los tres consumidores: la matriz de poblaciones, la de autoridades y los renglones numéricos.
