---
type: task
id: task-125
title: Podar collection_data.parent, leído pero nunca producido
state: open
date: 2026-08-19
owner: ricardo
source: ["[[task-23]]"]
---

# Podar collection_data.parent, leído pero nunca producido

El typedef de `collection_data` escrito en [[task-23]] dejó a la vista una propiedad fantasma: `parent`. Dos lugares la leen —`dashboard.vue` (~línea 167) y `PanelCommon.vue` (~línea 56)— y ningún productor la asigna en ninguna parte del flujo. Como el typedef nuevo no la incluye, el IDE ya marca ambas lecturas como propiedad inexistente, así que el ruido es permanente hasta que se resuelva.

La decisión es de Ricardo y tiene dos salidas: podar las dos lecturas (y con ellas la rama de código que dependía de un valor que siempre fue `undefined`), o reconocer que `parent` debía producirse y falta el productor, en cuyo caso esto no es poda sino un bug de datos. Antes de tocar nada hay que mirar qué hacía cada lectura cuando el valor llegaba `undefined`.

## Criterios de aceptación

- [ ] Ricardo decidió entre podar las lecturas o reponer el productor
- [ ] El IDE deja de marcar `collection_data.parent` en dashboard.vue y PanelCommon.vue
