---
type: task
id: task-58
title: "Guiar a la revisora en la doble transición al devolver: grupo y paquete"
state: open
date: 2026-08-04
owner: ai
source: ["[[task-41]]"]
---

# Guiar a la revisora en la doble transición al devolver: grupo y paquete

Decisión de Ricardo (2026-08-04, sesión de la sección de información base): gen_need_changes de un grupo NO propaga hacia arriba (idéntico a bp) y la doble transición se queda manual — pero la UI debe guiarla, porque hoy una revisora puede devolver un grupo y dejar el paquete en gen_sent, con lo que la IES no puede editar nada (la raíz manda en canEditContent). Ricardo reconoce que hay trabajo pendiente de diseño en este flujo; no es de esta sesión. El humo integrado del 2026-08-04 documentó el caso exacto.

## Criterios de aceptación

- [ ] La revisora entiende desde la UI que devolver un grupo no devuelve el paquete, y el flujo la lleva a completar ambas transiciones sin conocer el motor
- [ ] La solución aplica igual a bp y gen (misma mecánica de motor)
