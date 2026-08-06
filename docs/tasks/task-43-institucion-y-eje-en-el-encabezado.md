---
type: task
id: task-43
title: Institución y eje en el encabezado de la tarjeta de buena práctica
state: open
date: 2026-08-03
owner: ai
parent: "[[task-6]]"
source: ["[[2026-07-28-reunion-flujo-bp-e-informacion-base]]"]
---

# Institución y eje en el encabezado de la tarjeta de buena práctica

En la lista de buenas prácticas, el encabezado de cada panel muestra el nombre de la práctica pero no de qué institución es ni a qué eje pertenece. `[02:12]` «en el header o en la cosa que aparece al principio, que sepas de qué institución es. Porque ahorita solo dice el nombre, pero no dice como de qué institución, y creo que eso es importante». `[02:49]` «El estatus en el que está. Y, pues, de qué eje a qué eje pertenece».

Estado actual: `nuxt/app/components/dashboard/example/good_practice/GoodPracticeCard.vue` muestra el nombre, un chip con el número de características activas, otro con los archivos de evidencia, el contador de evaluados (solo para revisoras) y el `FlowStatusChip`. El estatus ya está resuelto; faltan institución y eje.

**Mismo patrón, otro objeto (2026-08-06):** [[task-82]] hace lo equivalente en el header de la **institución** —siglas visibles y nombre completo con tooltip debajo—. Conviene fijar un solo criterio de identificación en headers y aplicarlo en ambos.

El eje ya viaja en el objeto (`GoodPracticeHeader.vue` lo despliega con `DisplayGroup` sobre el grupo de filtro `axes`), así que el trabajo es de presentación en la tarjeta, no de contrato de datos. La institución hay que confirmar que venga en el serializador de lista.

## Criterios de aceptación

- [ ] La tarjeta de cada práctica muestra la institución
- [ ] La tarjeta muestra el eje al que pertenece
- [ ] Se ve en la vista de la revisora, que es donde conviven prácticas de varias instituciones
