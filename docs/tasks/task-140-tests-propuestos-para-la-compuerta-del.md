---
type: task
id: task-140
title: Tests propuestos para la compuerta del cuestionario, los pesos y el editor por bloques
state: open
date: 2026-09-10
owner: ricardo
parent: "[[task-2]]"
source: ["[[2026-09-10-editor-por-bloques-cuestionario-abierto-y-retiro-del-seed]]"]
---

# Tests propuestos para la compuerta del cuestionario, los pesos y el editor por bloques

Lista propuesta al cierre de la sesión del 10 de septiembre, para que Ricardo la recorte, extienda o redirija antes de escribir nada. Hoy existe solo la sonda `api/.claude/smoke_content_gate.py` (13 comprobaciones contra los endpoints reales, fuera de la suite).

Backend (pytest):

1. Cerrado, POST y DELETE en `/catalogs/a_question/` responden 403 con el mensaje de cierre.
2. Abierto, POST de una AQuestion a un observable con 3 opciones queda con `order == 4` y crea la fila puente de `a_questions`.
3. PATCH de `observable` sobre una pregunta existente lo deja intacto (solo se escribe al crear).
4. Cerrado, PATCH de `includes_admin` o `has_main_sectors` se ignora; abierto, aterriza.
5. Borrar la única ReachQuestion deja viva la fila puente de `reach`.
6. Segunda corrida de `load_questionnaire` aborta con CommandError; con `--force` corre y refresca `seeded_at`.
7. Fila puente sin peso propio en un observable que además tiene `plans` devuelve `final_weight is None` (muerde directo la regla del trío estándar).
8. Trío estándar → `uses_default_weights=True`, `weights_pending=False`; agregar `plans` voltea ambas.
9. Catálogo de ajustes: POST y DELETE 405, PATCH de `content_open` a falso 200, PATCH de vuelta a verdadero 400, `seeded_at` ignorado al escribir.
10. POST de una pregunta con `text: ''` responde 400 (fija el porqué del texto provisional «Nueva pregunta»).

Frontend (Vitest / Playwright con backend mockeado):

1. Vitest sobre las reglas de peso extraídas a un helper puro (peso efectivo, herencia solo en el trío, pendientes, hint por estado), incluida la trampa del 1.12 donde `default_weight=5` sigue dando «falta capturar». Exige sacar esa lógica de `ObservableEditSimple` a `app/utils/`.
2. e2e: editar un texto, el snackbar nombra el bloque y la petición lleva solo ese recurso.
3. e2e: marcar un tipo → aparece el bloque y el aviso lista los cuatro; desmarcar → diálogo → ambos desaparecen.
4. e2e: agregar pregunta → numerada al final y el chip de la fila crece; borrar con la palabra → revierte; palabra equivocada no borra nada.
5. e2e: con `content_open: false` mockeado, banner presente, cero «Agregar pregunta», cero botones de borrar, casillas de tipo inertes.
6. e2e: la barra cierra vía diálogo y emite el PATCH; cerrada, pinta texto sin switch.
7. e2e: el desplegable de sectores muestra los dos subencabezados, deshabilita los principales con `has_main_sectors` y recalcula el total.
8. e2e o manual: el foco tras agregar pregunta y tras marcar tipo, y Ctrl+Enter ([[task-145]]).

## Criterios de aceptación

- [ ] Lista acordada con Ricardo
- [ ] Los tests acordados escritos y en verde, con prueba de que muerden
- [ ] `api/TESTING.md` y `nuxt/TESTING.md` actualizados
