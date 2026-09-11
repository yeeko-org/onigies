---
type: task
id: task-147
title: Revisar que ningún otro EditSimple pinte el campo order
state: closed
date: 2026-09-10
owner: ai
parent: "[[task-3]]"
source: ["[[2026-09-10-editor-por-bloques-cuestionario-abierto-y-retiro-del-seed]]"]
---

# Revisar que ningún otro EditSimple pinte el campo order

Regla de Ricardo del 10 de septiembre, ya escrita en `dashboard-collections`: `order` nunca es un campo de un editor, ni de solo lectura; se cambia con el switch «Reordenar» de las listas. Se aplicó al marco genérico (`EditCommonFields`), al editor de observable, a `QuestionTypeEditSimple` y a los cinco editores sueltos de familia. Falta barrer los demás `*EditSimple.vue` y `*Edit.vue` de `components/dashboard/`.

## Criterios de aceptación

- [x] Ningún editor del dashboard expone `order`

## Cierre (10 de septiembre de 2026)

Barrido hecho al cierre de la sesión: `GeneralQuestionEditSimple.vue` era el único editor que aún exponía `order` editable y se quitó; `GeneralGroup` solo lo imprime como texto.
