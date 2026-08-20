---
type: task
id: task-126
title: Evaluar dónde más conviene el patrón JSDoc del frontend
state: open
date: 2026-08-20
owner: ai
source: ["[[task-23]]"]
related: ["[[task-119]]", "[[task-125]]"]
---

# Evaluar dónde más conviene el patrón JSDoc del frontend

La [[task-23]] tipó `collection_data` y `field` con typedefs JSDoc en `nuxt/app/types/collection.js`: autocompletado y aviso de propiedad inexistente en el IDE, sin migrar a TypeScript. Ricardo decidió **no** migrar a TS, así que JSDoc es el mecanismo de tipado del frontend, no un paso intermedio hacia otro.

El patrón ya demostró que paga más allá del autocompletado: al escribir el typedef salió a la luz `collection_data.parent`, una propiedad leída en dos lugares y producida en ninguno ([[task-125]]), y la revisión del mismo contrato destapó el bug de PK de texto en `patchCatalog` ([[task-119]]). Tipar un contrato es, de paso, auditarlo.

Falta decidir dónde más aplicarlo. Candidatos a revisar, sin comprometerse todavía con ninguno: el store (`nuxt/app/store/index.js` y lo que expone en `cats`), los composables con contrato de payload (`cats.js`, `filters.js`, `save_elements.js`, los de flow), la forma de las respuestas del API que el frontend consume repetidas veces, y las props de los componentes genéricos del dashboard que hoy reciben objetos sueltos.

El criterio de selección es el que ya funcionó: tipar donde el objeto viaja entre capas y nadie lo declara —no donde el valor nace y muere en el mismo archivo—. La tarea es primero el barrido y la propuesta, y después aplicar solo lo que Ricardo apruebe.

## Criterios de aceptación

- [ ] Existe la lista de contratos candidatos del frontend, cada uno con por qué sí o por qué no
- [ ] Ricardo validó cuáles se tipan
- [ ] Los aprobados tienen typedef y el IDE avisa de propiedades inexistentes
