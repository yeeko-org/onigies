---
type: task
id: task-98
title: Flujo — UX de estatus y transiciones para las dos audiencias
state: open
date: 2026-08-11
owner: ai
source: ["[[2026-08-11-auditoria-del-arbol-de-trabajo-y-reorganizacion]]"]
---

# Flujo — UX de estatus y transiciones para las dos audiencias

Raíz nueva. Agrupa ocho tareas que hasta hoy colgaban sueltas y que son, todas, la misma costura del motor de flujo asomándose a las dos audiencias: la IES que captura y la revisora que dictamina. Se abren como raíz propia y no bajo [[task-1]] porque aquélla es deuda de migración —retirar StatusControl, tests de sincronía, borrar el mapa de status viejo— y esto es diseño de experiencia sobre un motor que ya funciona en producción.

[[task-58]] ya lo había anticipado por su cuenta: anota que se resuelve con el skill `ux-designer`, que es un problema de diseño y no de implementación, y que [[task-72]] es «su hermana por el otro lado del mostrador». Ese es exactamente el criterio de agrupación.

Hijas: [[task-45]], [[task-46]], [[task-58]], [[task-72]], [[task-73]], [[task-74]], [[task-75]] y [[task-76]].

Dos de ellas, [[task-75]] y [[task-76]], dependen de que ocurra el taller de estados con Rubén, [[task-26]], que la reunión del 11 de agosto no tocó.

## Criterios de aceptación

- [ ] Las ocho hijas están cerradas o abandonadas
- [ ] La doble transición (grupo y paquete) se resuelve con el mismo criterio en bp y en gen
