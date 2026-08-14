---
type: record
id: 2026-08-14-deploy-publicacion-de-la-seccion-de
title: "Deploy: publicación de la sección de Información base (gen) a las IES"
date: 2026-08-14
---

# Deploy: publicación de la sección de Información base (gen) a las IES

Cierre de [[task-41]]. La sección de Información base (grupo `gen` del motor de flujo) quedó visible para todas las IES reales en producción, no solo para las instituciones De prueba.

## El cambio

Un solo commit, frontend puro: se agregó `SECTION_BASE` a `PUBLISHED_SECTIONS` en `nuxt/app/utils/sections.js`. Ese es el mecanismo transicional que fija [[adr-0009]]: mientras el desarrollo va sección por sección, publicar una es un cambio de código —no un dato en la base— que se despliega con la sección misma. Antes solo estaba publicada Buenas Prácticas (`bp`); ahora `[SECTION_BASE, SECTION_BP]`. El cuestionario principal (`cp`) se dejó fuera a propósito: su contenido en `/respuestas` todavía es un placeholder de imágenes, no captura real.

La constante alimenta los dos únicos lugares que enumeran secciones a la IES: las pestañas de `pages/respuestas/[period].vue` y los chips de `pages/respuestas/index.vue`. La revisora no pasa por `/respuestas`, así que ya veía la colección en el dashboard sin depender de esto.

## Deploy

- Commit `fa15b1d` en `main`.
- `git push origin main:production` (fast-forward, disciplina de [[adr-0001]]); `origin/production` avanzó de `b45afe1` a `fa15b1d`, arrastrando también el commit docs-only `7e74d99` (retiro de `migrate_flow_data`). Chequeo de drift de migraciones en el rango: limpio, sin cambios de `models.py`/`migrations`.
- El push a `production` dispara el build de Netlify (~2-3 min). Cambio frontend puro: no hizo falta el runbook del API en Yeeko.

Se publicó el jueves **14**, un día después del jueves 13 comprometido en la reunión del 11 de agosto ([[2026-08-11-reunion-con-ruben-sobre-la-informacion-base]]). Rubén validó la sección con su equipo antes de abrir; el anuncio a las personas enlace se hizo en la reunión del viernes 14.

## Candado de periodo: deliberadamente sin fecha de cierre

`Period.is_gen_submission_closed` existe en el modelo pero **no está enforced** (solo `is_bp_submission_closed` bloquea envíos). No es un bug ni un olvido: **Rubén decidió dejar la captura de generales sin fecha de cierre por ahora**, para monitorear cómo avanzan las IES y fijar el deadline más adelante. No «arreglar» esto activando el candado sin decisión previa.
