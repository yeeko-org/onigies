---
type: task
id: task-142
title: Conteo de respuestas por pregunta en los serializers de familia para graduar la confirmación de borrado
state: open
date: 2026-09-10
owner: ai
parent: "[[task-3]]"
source: ["[[2026-09-10-editor-por-bloques-cuestionario-abierto-y-retiro-del-seed]]"]
---

# Conteo de respuestas por pregunta en los serializers de familia para graduar la confirmación de borrado

Borrar una pregunta desde el editor pide siempre la palabra de confirmación porque ningún payload trae cuántas respuestas cuelgan de ella. Con un conteo por pregunta (`count_fields` en los schemas de familia o una anotación en el serializer de lista), la confirmación puede ser proporcional al daño y decir «se borran las N respuestas capturadas». Ricardo lo dejó a criterio del asistente y se pospuso: hasta que las IES contesten, el conteo es cero en todas partes y no cambia nada.

## Criterios de aceptación

- [ ] Las cinco familias exponen el conteo de respuestas por pregunta
- [ ] El diálogo de borrado del editor lo usa: sin respuestas no pide palabra; con respuestas la pide y dice cuántas
