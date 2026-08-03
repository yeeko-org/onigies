---
type: task
id: task-10
title: Endurecer en el backend el candado de periodo cerrado
state: open
date: 2026-08-03
owner: ai
parent: "[[task-1]]"
source: ["[[2026-07-03-auditoria-y-mejoras-del-flujo]]"]
---

# Endurecer en el backend el candado de periodo cerrado

Follow-up que dejó abierto la sesión S4: `GoodPracticeViewSet.update` no valida periodo ni turno, a diferencia de `discard`/`reopen`, que sí. Hoy el candado de periodo vive solo en el frontend (`canEdit` exige `periodOpen`), así que una petición directa lo salta.

## Criterios de aceptación

- [ ] Una petición de actualización con el periodo cerrado responde 403
- [ ] Hay un test que lo cubre
