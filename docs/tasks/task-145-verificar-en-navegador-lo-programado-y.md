---
type: task
id: task-145
title: "Verificar en navegador lo programado y no visto correr: Ctrl+Enter, el foco al agregar y las colecciones sueltas de A, planes y especial"
state: open
date: 2026-09-10
owner: ricardo
parent: "[[task-2]]"
source: ["[[2026-09-10-editor-por-bloques-cuestionario-abierto-y-retiro-del-seed]]"]
---

# Verificar en navegador lo programado y no visto correr: Ctrl+Enter, el foco al agregar y las colecciones sueltas de A, planes y especial

Tres conductas del editor por bloques quedaron en código sin verse funcionar en el recorrido de humo del 10 de septiembre: Ctrl/Cmd+Enter en un textarea dispara el Guardar de esa tarjeta; al agregar una pregunta el foco cae en el textarea nuevo con «Nueva pregunta» seleccionado, y al marcar un tipo el foco va al «Agregar pregunta» de ese bloque; y las colecciones sueltas de preguntas A, de planes y especial del menú lateral (las de orgánica y sectorial sí se abrieron). Ricardo hizo dos recorridos visuales sin reportar fallas en estos puntos, pero no los probó expresamente.

## Criterios de aceptación

- [ ] Las tres conductas vistas funcionar, o corregidas

Credencial staff local para el recorrido: la de «Prueba manual contra el stack local» en `nuxt/TESTING.md`.

Observado en el humo de producción del 10 de septiembre ([[2026-09-10-deploy-del-editor-por-bloques-y-ultima-siembra]]): Ctrl+Enter en el campo «Nombre del observable» (un text field, no un textarea) no guarda; el botón Guardar sí. Coincide con el tooltip del botón («dentro del texto»), así que no contradice lo programado, pero el caso del textarea sigue sin verse correr.
