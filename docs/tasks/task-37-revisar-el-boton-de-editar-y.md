---
type: task
id: task-37
title: Revisar el botón de editar y el reuso del enlace de invitación
state: open
date: 2026-08-03
owner: ai
parent: "[[task-6]]"
source: ["[[2026-04-16-prueba-con-usuarias-reales]]"]
---

# Revisar el botón de editar y el reuso del enlace de invitación

Dos tropiezos de la prueba con usuarias: el botón de editar de una práctica guardada no respondió, y una usuaria que abandonó a medias no pudo volver porque el enlace respondió «la invitación ya ha sido usada» — una invitación consumida debería llevar al login, no a un muro. Ambos son de abril; hay que confirmar si siguen vivos antes de arreglarlos.

## Criterios de aceptación

- [ ] Se reprodujo o se descartó cada uno
- [ ] Los que siguen vivos están corregidos

Ojo antes de empezar: la rama `claude/gallant-jemison` (commit `111e7c1`, sin mergear) toca `GoodPracticeCard.vue`, `GoodPracticeEditSimple.vue` y `RegisterForm.vue` — los tres archivos de estos dos hallazgos. Revisar qué resolvió esa rama antes de reimplementar, y decidir si se mergea.
