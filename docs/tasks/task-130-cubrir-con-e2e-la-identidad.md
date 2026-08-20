---
type: task
id: task-130
title: Cubrir con e2e la identidad por pk de los paneles al borrar filas
state: open
date: 2026-08-20
owner: ai
parent: "[[task-61]]"
related: ["[[task-22]]", "[[task-3]]", "[[task-7]]"]
---

# Cubrir con e2e la identidad por pk de los paneles al borrar filas

Hueco detectado el 20 de agosto de 2026 al revisar los commits de la sesión en piloto automático: los cambios de `673dd34` quedaron sin verificación automatizada. Y el hueco es más ancho que ese commit — **el dashboard administrativo no tiene un solo e2e**: los 9 unitarios de Vitest cubren únicamente `app/utils/sections.js` y los 38 e2e van todos de autenticación, tabs de `/respuestas` e «Información base».

## El alcance: solo los paneles

`PanelList` / `PanelCommon`: que los paneles abiertos se identifiquen por `pk` al borrar una fila. Si la identidad del panel abierto se guarda por índice y no por `pk`, borrar una fila desplaza el array y el panel abierto salta a otro renglón. Es la regresión que importa, y toca la costura que [[task-22]] acaba de cambiar —los Panel\* dejaron de mutar `props.results` y ahora el dueño aplica la mutación—, así que el flujo entero de borrado pasa por código nuevo sin red.

Nivel: **e2e con Playwright y backend mockeado**. No es lógica pura —es interacción y estado compartido entre el listado y el panel—, así que Vitest no lo alcanza. Convenciones, fixtures y el flujo MCP ↔ tests en `nuxt/TESTING.md` y el skill `playwright-e2e`. Hay que abrir mocks de dashboard: hoy los interceptores de `e2e/mocks/` solo dan de comer a autenticación y a `gen`.

## Por qué se recortó

La versión original de esta task listaba dos huecos más, los dos de status: la etiqueta del select de `StatusDetail` y el snackbar de cambio de status en `EditCommon`. Ricardo los sacó el mismo día con una razón que no es de prioridad sino de vigencia: **son componentes que están por desaparecer**. Un inventario de esta misma sesión confirmó que `StatusControl` ya no gobierna nada, y su borrado —la §8 de [[task-7]]— se ejecuta pronto; en esta sesión ya se está retirando además la superficie visible de «Status de Envío» del dashboard. Testear eso sería trabajo desechable: los tests morirían con su feature antes de haber atrapado nada.

## Criterios de aceptación

- [ ] Un e2e ejercita borrar una fila con un panel abierto y verifica que el panel abierto sigue siendo el mismo objeto, no el mismo índice
- [ ] Los mocks del dashboard necesarios viven en `e2e/mocks/` junto a los que ya están
- [ ] `nuxt/TESTING.md` refleja el flujo nuevo
