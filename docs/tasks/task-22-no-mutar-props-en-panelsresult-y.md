---
type: task
id: task-22
title: No mutar props en PanelsResult y PanelList
state: open
date: 2026-08-03
owner: ai
parent: "[[task-3]]"
source: ["[[2026-06-19-recomendaciones-del-dashboard]]"]
---

# No mutar props en PanelsResult y PanelList

Recomendación 7 de la auditoría. Ambos componentes mutan `props.results` directamente (`unshift`, `splice`, asignación por índice) tras guardar o borrar. Funciona en Vue 3, pero el dueño del array es `CollectionDisplay`. Salida: emitir el cambio hacia arriba (los eventos `@item-saved`/`@item-deleted` ya existen) y que el dueño aplique la mutación. Es deuda de prolijidad, no un bug.

## Criterios de aceptación

- [ ] Ningún Panel* muta `props.results`
