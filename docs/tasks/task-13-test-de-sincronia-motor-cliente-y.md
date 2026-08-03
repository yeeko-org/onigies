---
type: task
id: task-13
title: Test de sincronía motor/cliente y orden por prioridad
state: open
date: 2026-08-03
owner: ai
parent: "[[task-1]]"
source: ["[[2026-07-03-auditoria-y-mejoras-del-flujo]]"]
---

# Test de sincronía motor/cliente y orden por prioridad

Sesión S7, opcional. Dos cosas chicas: un test que garantice que `get_available_transitions` del servidor y el cálculo del cliente no divergen (hallazgo B9), y usar `priority` para ordenar las colecciones del dashboard — hoy el frontend ignora `order` y `priority` (hallazgo F8).

## Criterios de aceptación

- [ ] Existe el test de sincronía
- [ ] Las colecciones del dashboard se ordenan por prioridad
