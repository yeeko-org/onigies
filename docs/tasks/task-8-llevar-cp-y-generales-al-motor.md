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

## Criterios de aceptación

- [ ] La IES opera CP y generales por transiciones del motor, sin status hardcodeados
- [ ] La revisora los revisa desde el dashboard con chip, transiciones y comentarios
