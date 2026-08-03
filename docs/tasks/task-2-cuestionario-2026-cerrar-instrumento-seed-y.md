---
type: task
id: task-2
title: Cuestionario 2026 — cerrar instrumento, seed y captura
state: open
date: 2026-08-03
owner: ai
source: ["[[2026-07-04-seed-del-cuestionario]]", "[[2026-07-03-reduccion-del-cuestionario]]"]
---

# Cuestionario 2026 — cerrar instrumento, seed y captura

El seed declarativo (`load_questionnaire`) ya siembra el instrumento reducido, pero no se ha desplegado a producción y quedan huecos que dependen del cliente (pesos, dos textos) y una superficie de captura sin construir (Generales). El modelo de dominio vive en el skill `cp-questionnaire`.

## Criterios de aceptación

- [ ] El seed corre en producción con el instrumento definitivo
- [ ] Los observables tienen pesos reales, no el fallback por tipo de pregunta
- [ ] La captura de Generales existe en el frontend
