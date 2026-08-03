---
type: task
id: task-18
title: "Frontend de Generales: captura de poblaciones y autoridades"
state: open
date: 2026-08-03
owner: ai
parent: "[[task-2]]"
source: ["[[2026-07-04-seed-del-cuestionario]]"]
---

# Frontend de Generales: captura de poblaciones y autoridades

Quedó fuera del alcance del seed: la captura de `PopulationQuantity` por sector — la composición sexo-genérica que alimenta el observable 1.7 — y el checklist de autoridades (`Sector.is_authority`). El modelo de datos ya existe; falta la superficie. Contexto en el skill `gen-general-info`.

## Criterios de aceptación

- [ ] La IES captura poblaciones y autoridades desde /respuestas
- [ ] Los datos aterrizan en `PopulationQuantity` y en los grupos generales correspondientes
