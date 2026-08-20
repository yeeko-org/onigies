---
type: task
id: task-129
title: PyCharm no resuelve las actions destructuradas del store
state: open
date: 2026-08-20
owner: ai
related: ["[[task-119]]"]
---

# PyCharm no resuelve las actions destructuradas del store

Detectado el 20 de agosto de 2026 al revisar los commits de la sesión en piloto automático. Ricardo lo dejó pendiente en el momento: «está complejo, ahora no podría resolverlo».

**El síntoma.** En `nuxt/app/composables/save_elements.js`, las actions que se sacan del store por desestructuración —`const { patchSimple, patchCatalog } = mainStore`— no resuelven: Ctrl+click sobre `patchCatalog` no lleva a su definición en `nuxt/app/store/index.js`. No es un caso aislado: los diagnósticos del IDE marcan como «unused» también `deleteCatalog`, `fetchElements`, `exportData` y otras actions del mismo store, que sí están en uso. Es decir, el IDE no está viendo la relación entre el store y sus consumidores, no solo entre dos archivos.

**Hipótesis principal: índice viciado.** Lo que apunta hacia ahí es que `patchCatalog` fue la única action cuyo cuerpo se reescribió en `673dd34` —el fix de la PK de texto de [[task-119]]—, así que el archivo cambió bajo el índice. Que el resto de las actions marcadas «unused» tampoco resuelvan es consistente con un índice desactualizado del store completo, y no con un error de sintaxis en una función.

**Hipótesis alterna, sin descartar: el JSDoc.** La anotación de tupla que llevan esos parámetros (`@param {[collection_data, string, Object]}`) podría estar rompiendo la inferencia de PyCharm. La prueba de falsación está pendiente y es barata: comentar el `@param` de tupla y reintentar el Ctrl+click. Si resuelve, el problema es la anotación; si no, queda el índice.

**Remedio a probar primero:** Invalidate Caches / Restart. Si el problema desaparece ahí, era índice y la tarea cierra con eso.

**Hallazgo lateral, independiente de lo anterior.** `.idea/onigies.iml` excluye `.venv-tools`, `api/venv`, `.playwright-mcp` y `nuxt/.output`, pero **no** `nuxt/.nuxt`. Ese directorio es salida generada de Nuxt, cambia en cada build y contiene copias y re-exportaciones del código de la app: indexarlo infla el índice y puede sembrar definiciones duplicadas que compitan con las reales. Vale excluirlo aunque no sea la causa de lo de arriba.

## Criterios de aceptación

- [ ] Ctrl+click sobre patchCatalog desde save_elements.js llega a su definición en el store
- [ ] Las actions en uso dejan de aparecer como «unused» en los diagnósticos del IDE
- [ ] Está escrito cuál de las dos hipótesis era, con el resultado de la prueba de falsación del @param de tupla
- [ ] nuxt/.nuxt está excluido en .idea/onigies.iml
