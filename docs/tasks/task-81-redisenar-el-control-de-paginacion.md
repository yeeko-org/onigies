---
type: task
id: task-81
title: Rediseñar el control de paginación
state: open
date: 2026-08-06
owner: ai
parent: "[[task-3]]"
source: ["[[2026-08-06-temas-reunion-fer]]"]
related: ["[[task-22]]"]
---

# Rediseñar el control de paginación

§14 de la reunión con Fernanda, `[43:57]`–`[49:43]`, dictado por Ricardo. El control de «página 1 de 2» debe ser muy pequeño y reordenarse: primero el **número de resultados**, luego «página X de Y», y al final los botones anterior/siguiente, **solo si aplican**. Tamaño chico, color azul, claramente clicables, sin ocupar más altura de la necesaria.

Archivo: `nuxt/app/components/dashboard/common/main/PanelsResult.vue`. **Es el mismo archivo que toca [[task-22]]** (no mutar props en `PanelsResult` y `PanelList`): conviene agendarlas en la misma sesión para no diffear dos veces sobre lo mismo.

## Criterios de aceptación

- [ ] El orden es: número de resultados, «página X de Y», botones de navegación
- [ ] Los botones aparecen solo cuando hay más de una página
- [ ] El control no gana altura respecto de hoy y los controles se leen como clicables
