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

**2026-09-07**: la versión maquetada y final del instrumento resultó textualmente equivalente a la que ya está sembrada ([[2026-09-07-cotejo-del-instrumento-maquetado]]), así que el primer criterio queda cumplido y [[task-19]] cerró vacua. La task sigue abierta por los dos frentes que el documento final no resolvió: los pesos ([[task-15]], que el .docx tampoco trae) y la redacción pendiente de definición de la CIGU ([[task-16]], [[task-17]], [[task-88]], [[task-50]]).

## Criterios de aceptación

- [x] El seed corre en producción con el instrumento definitivo (2026-09-07)
- [ ] Los observables tienen pesos reales, no el fallback por tipo de pregunta
- [x] La captura de Generales existe en el frontend ([[task-41]], sesión 2026-08-03/04)
