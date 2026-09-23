---
type: task
id: task-1
title: Cerrar la migración al motor de flujo
state: open
date: 2026-08-03
owner: ai
source: ["[[2026-06-05-diseno-del-motor-de-flujo]]", "[[2026-06-23-progreso-frontend-del-flujo]]", "[[2026-07-03-auditoria-y-mejoras-del-flujo]]"]
---

# Cerrar la migración al motor de flujo

El motor `flow` está en producción desde 2026-06-26 y buenas prácticas ya corre entero sobre él. Falta lo que la coexistencia con `ies.StatusControl` dejó pendiente y las dos superficies que nunca se migraron (cuestionario principal y generales). El mapa vivo del motor es el skill `flow`; estos nodos son lo que sigue abierto de su ejecución.

## Criterios de aceptación

- [x] Ningún modelo conserva `status_register`/`status_sending` ([[task-7]], 2026-09-22)
- [x] CP y gen se operan desde el motor en el frontend (gen 2026-08-04; cp 2026-09-22, [[task-8]])
- [x] El validador de deuda del front ya no menciona los campos viejos (`filters.js` se borró entero el 2026-09-22)

**2026-09-22:** los tres criterios se cumplen en la rama `cp-backend`; la task se cierra cuando el deploy ([[task-163]]) los lleve a producción. Record [[2026-09-22-cierre-cuestionario-principal-captura-y-borrado]].
