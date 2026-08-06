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

- [ ] Ningún modelo conserva `status_register`/`status_sending`
- [ ] CP y gen se operan desde el motor en el frontend (gen cumplido el 2026-08-04; falta CP — [[task-8]])
- [ ] El validador de deuda del front (`filters.js`/`fetch.js`) ya no menciona los campos viejos
