---
type: task
id: task-45
title: Cerrar el diálogo de detalle al concluir la acción de flujo
state: open
date: 2026-08-03
owner: ai
parent: "[[task-98]]"
source: ["[[2026-07-28-reunion-flujo-bp-e-informacion-base]]"]
---

# Cerrar el diálogo de detalle al concluir la acción de flujo

Al ejecutar una transición desde el detalle de una buena práctica, el diálogo de detalle se queda abierto aunque la acción ya no tenga sentido allí. Salió tres veces en la demo: `[11:46]` «no sé si se debería cerrar solito algunas veces, como cuando ya lo mandas pues ya no tiene sentido que siga apareciendo»; `[16:56]` «Creo que hay que cerrar el diálogo, esa acción me falta»; `[18:33]` «esto se tiene que cerrar solito».

Quedó comprometido como corrección mínima a subir el mismo día: `[37:50]` «voy a intentar como incorporar de una vez las correcciones estas mínimas, como que cierre el diálogo cuando ya concluyes».

Estado actual: `nuxt/app/composables/useFlowActions.js` ya llama a `closeDialog()` tras una transición exitosa, pero eso cierra el diálogo *de transición*, no el diálogo de detalle que lo contiene. El kernel ya devuelve el resultado de `onSelect` precisamente para que el consumidor decida si cierra el suyo; falta que los consumidores lo usen.

## Criterios de aceptación

- [ ] Tras una transición exitosa desde el detalle, el diálogo de detalle se cierra
- [ ] Si la transición falla o se cancela, el diálogo permanece abierto
