---
type: task
id: task-8
title: Llevar CP y generales al motor de flujo en el frontend
state: open
date: 2026-08-03
owner: ai
parent: "[[task-1]]"
source: ["[[2026-06-23-progreso-frontend-del-flujo]]"]
---

# Llevar CP y generales al motor de flujo en el frontend

`FlowStatusActions`, `FlowStatusChip` y `FlowComments` son genéricos y ya sirven; falta incorporarlos a las páginas de respuesta del cuestionario principal y de generales, y a su revisión en el dashboard. Buenas prácticas es el modelo a seguir (skill `bp-validation-ux`).

**Acotada a CP (2026-08-06):** la sesión de generales del 2026-08-04 dejó `gen` corriendo entero sobre el motor (captura de la IES, revisión, envío gateado), verificado en la sesión duo ([[2026-08-06-sesion-duo-adjuntos-sobre-flow-y]]). Lo que queda de esta task es únicamente el cuestionario principal (cp), ligado a la superficie de [[task-42]].

## Criterios de aceptación

- [ ] La IES opera CP por transiciones del motor, sin status hardcodeados (generales ya cumplido, 2026-08-04)
- [ ] La revisora revisa CP desde el dashboard con chip, transiciones y comentarios
