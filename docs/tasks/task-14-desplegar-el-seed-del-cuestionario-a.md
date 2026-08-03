---
type: task
id: task-14
title: Desplegar el seed del cuestionario a producción
state: open
date: 2026-08-03
owner: ricardo
parent: "[[task-2]]"
source: ["[[2026-07-29-commits-tematicos-y-deploy-flow]]", "[[2026-07-04-seed-del-cuestionario]]"]
---

# Desplegar el seed del cuestionario a producción

El código y el esquema del seed ya llegaron a producción con el fast-forward que resolvió el incidente del 500, pero `load_questionnaire` nunca se ha corrido allá. La ventana de despliegue depende de que el cliente resuelva los textos abiertos: sembrar antes obliga a re-sembrar después.

## Criterios de aceptación

- [ ] `load_questionnaire` corrió en producción
- [ ] Los ejes, componentes y observables visibles corresponden al instrumento definitivo
