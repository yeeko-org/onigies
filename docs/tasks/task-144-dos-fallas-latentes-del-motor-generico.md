---
type: task
id: task-144
title: "Dos fallas latentes del motor genérico del dashboard: aviso falso de useDynamicComponent y splice sin guarda en cleanDelete"
state: open
date: 2026-09-10
owner: ai
parent: "[[task-3]]"
source: ["[[2026-09-10-editor-por-bloques-cuestionario-abierto-y-retiro-del-seed]]"]
---

# Dos fallas latentes del motor genérico del dashboard: aviso falso de useDynamicComponent y splice sin guarda en cleanDelete

Encontradas durante el editor por bloques, sin corregir para no ampliar el alcance del deploy.

- `composables/useDynamicComponent.js` avisa en dev por cada `{Model}Edit.vue` ausente aunque exista `{Model}EditSimple.vue`, que reemplaza al `Edit` por completo: 42 avisos idénticos por carga de la lista de observables. Cortocircuitar el aviso cuando el `EditSimple` existe.
- `store.cleanDelete` hace `findIndex` y luego `splice(index, 1)` sin comprobar `-1`: cuando la fila no está en `cats`, `splice(-1, 1)` borra en silencio la última fila de ese catálogo en memoria. Hoy no se dispara porque las filas de pregunta sí viajan en `cats`; falta la guarda.

## Criterios de aceptación

- [ ] Sin aviso de `Edit` ausente cuando hay `EditSimple`
- [ ] `cleanDelete` no toca el store cuando la fila no está
