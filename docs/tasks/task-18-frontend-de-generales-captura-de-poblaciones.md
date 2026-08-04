---
type: task
id: task-18
title: "Frontend de Generales: captura de poblaciones y autoridades"
state: open
date: 2026-08-03
owner: ai
parent: "[[task-41]]"
source: ["[[2026-07-04-seed-del-cuestionario]]"]
related: ["[[task-2]]"]
---

# Frontend de Generales: captura de poblaciones y autoridades

Quedó fuera del alcance del seed: la captura de `PopulationQuantity` por sector — la composición sexo-genérica que alimenta el observable 1.7 — y el checklist de autoridades (`Sector.is_authority`). El modelo de datos ya existe; falta la superficie. Contexto en el skill `gen-general-info`.

Cuelga de [[task-41]], el compromiso de tener la sección de información base capturable para el 2026-08-03 y abierta a las IES el 2026-08-10. Sigue tocando el instrumento ([[task-2]]), pero su fecha y su condición de cierre las manda ahora la sección.

## Criterios de aceptación

- [ ] La IES captura poblaciones y autoridades desde /respuestas
- [ ] Los datos aterrizan en `PopulationQuantity` y en los grupos generales correspondientes
