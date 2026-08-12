---
type: task
id: task-46
title: "Transición única: ir directo al diálogo de confirmación"
state: open
date: 2026-08-03
owner: ai
parent: "[[task-98]]"
source: ["[[2026-07-28-reunion-flujo-bp-e-informacion-base]]"]
---

# Transición única: ir directo al diálogo de confirmación

Cuando solo hay una transición disponible, la interfaz obliga a tres clics: abrir el menú, elegir la única opción y confirmar. `[16:56]` «Creo que son muchos, muchos clics ahora que lo estoy volviendo a hacer. Como que, por ejemplo, si hay una sola opción, no debería... o sea, como que debería ser directo que le piques y ya te salga el diálogo de confirmación en lugar de que le piques, te salga una opción, le piques de nuevo, te salga el diálogo y ya envías».

Quedó junto con el cierre del diálogo en el lote de correcciones mínimas de `[37:50]`.

Estado actual: `nuxt/app/components/dashboard/flow/FlowStatusActions.vue` monta siempre el `v-menu` cuando `hasActions` es verdadero, sin caso especial para `transitions.length === 1`. El atajo consiste en llamar a `onSelect` directamente desde el chip cuando hay una sola transición; el diálogo de confirmación y el bloqueo por `entry_rules` siguen igual, porque ambos viven dentro de `onSelect`.

## Criterios de aceptación

- [ ] Con una sola transición disponible, el clic en el chip abre directo el diálogo de confirmación
- [ ] Con dos o más transiciones el menú sigue apareciendo
- [ ] El bloqueo por entry_rules se sigue mostrando en el caso de transición única
