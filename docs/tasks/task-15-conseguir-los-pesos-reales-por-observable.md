---
type: task
id: task-15
title: Conseguir los pesos reales por observable
state: open
date: 2026-08-03
owner: ricardo
parent: "[[task-2]]"
source: ["[[2026-07-04-seed-del-cuestionario]]"]
---

# Conseguir los pesos reales por observable

Bloqueado: el cliente no ha entregado la fuente de ponderaciones. Mientras tanto los pesos quedan en `null` y aplica el fallback a `QuestionType.default_weight` (a=60, b=40), lo que significa que cualquier índice calculado hoy es provisional.

**2026-09-07:** la versión maquetada y final del instrumento **no trae ponderaciones** ([[2026-09-07-cotejo-del-instrumento-maquetado]]). Se descarta la vía más plausible de desbloqueo: el documento del cliente no es la fuente de los pesos, así que hay que pedirla aparte o cerrar la task documentando el fallback como decisión definitiva.

**2026-09-07, segunda nota:** cambió la estructura, no los valores. Los pesos ya no son columnas de `Observable` sino filas de `ObservableQuestionType` (una por observable y tipo, `weight` nullable, efectivo = propio o `QuestionType.default_weight`), editables desde el dashboard por su catálogo ([[adr-0014]]). Siguen todos en `null`. Ponderación tentativa acordada con Rubén por WhatsApp: armonización e institucionalización 5, transversalidad sectorial 2.5, orgánica 2.5, sobre 10, pendiente de simular con él ([[task-135]]).

## Criterios de aceptación

- [ ] Los pesos están sembrados desde una fuente entregada por el cliente, o se documenta que el fallback es la decisión definitiva
