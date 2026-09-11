---
type: task
id: task-141
title: Texto provisional «Nueva pregunta» al crear, o `blank=True` en las cinco columnas `text`
state: open
date: 2026-09-10
owner: ricardo
parent: "[[task-2]]"
source: ["[[2026-09-10-editor-por-bloques-cuestionario-abierto-y-retiro-del-seed]]"]
related: ["[[adr-0015]]"]
---

# Texto provisional «Nueva pregunta» al crear, o `blank=True` en las cinco columnas `text`

Las columnas `text` de AQuestion, BQuestion, ReachQuestion, PlanQuestion y SpecialQuestion son `TextField()` sin `blank=True`, así que el POST con texto vacío responde 400. El editor crea hoy la pregunta con el texto «Nueva pregunta» preseleccionado para que al escribir se reemplace. Ricardo decidió no tocar el esquema en el deploy del 10 de septiembre.

Riesgo que queda: una «Nueva pregunta» olvidada llega al instrumento publicado. La alternativa es `blank=True` en las cinco columnas más una migración, con la tarjeta nueva vacía y enfocada.

## Criterios de aceptación

- [ ] Decisión de Ricardo registrada
- [ ] Si se abre el vacío: migración aplicada y el editor crea la pregunta sin texto provisional
