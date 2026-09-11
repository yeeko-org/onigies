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

El seed declarativo (`load_questionnaire`) sembró el instrumento reducido en producción por última vez el 2026-09-10 ([[task-139]]) y quedó retirado: desde entonces el dashboard es la única fuente del instrumento. Quedan huecos que dependen del cliente (pesos, dos textos), que Rubén captura desde el dashboard, y una superficie de captura sin construir (Generales). El modelo de dominio vive en el skill `cp-questionnaire`.

**2026-09-07**: la versión maquetada y final del instrumento resultó textualmente equivalente a la que ya está sembrada ([[2026-09-07-cotejo-del-instrumento-maquetado]]), así que el primer criterio queda cumplido y [[task-19]] cerró vacua. La task sigue abierta por los dos frentes que el documento final no resolvió: los pesos ([[task-15]], que el .docx tampoco trae) y la redacción pendiente de definición de la CIGU ([[task-16]], [[task-17]], [[task-88]], [[task-50]]).

**2026-09-07, tarde:** ponderación y aplicabilidad por tipo reestructuradas en un modelo intermedio, `QuestionType` como fuente de nombres y pesos default, y el dashboard manda sobre los textos del instrumento ([[adr-0014]], [[2026-09-07-rediseno-edicion-observables-pesos-y-nomenclatura]]). [[task-42]] cerró; el editor por bloques sigue en [[task-131]]. Riesgos del seed abiertos: [[task-133]] (borrado en cascada) y [[task-134]] (sectores duplicados). Para el siguiente deploy: correr `load_questionnaire --overwrite-texts` una sola vez (nadie ha editado textos aún) y `migrate_initial_data`, que solo re-afirma `order`, `required` y modelos; los nombres nuevos los aplica la migración `question/0006` al migrar. El seed aborta antes de escribir si algún componente fue renombrado desde el dashboard (pre-flight del 2026-09-08, [[task-134]]).

## Criterios de aceptación

- [x] El seed corre en producción con el instrumento definitivo (2026-09-07)
- [ ] Los observables tienen pesos reales, no el fallback por tipo de pregunta
- [x] La captura de Generales existe en el frontend ([[task-41]], sesión 2026-08-03/04)
