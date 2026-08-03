---
type: decision
id: adr-0006
title: El menú del dashboard se declara a mano en el frontend
state: accepted
date: 2026-06-10
origin: ricardo
deliberation: unilateral
rationale: recorded
source: ["[[2026-06-10-port-de-ps-schema]]"]
affects: ["nuxt/app/layouts/dashboard.vue"]
---

# El menú del dashboard se declara a mano en el frontend

## Contexto

Con la configuración de colecciones generándose sola desde el registry (ver [[adr-0005]]), el menú lateral del dashboard podía armarse automáticamente a partir de ella: nivel, orden, ícono y color venían en el payload de `/catalogs/all/`.

## Opciones consideradas

- **Menú automático** — se deriva del catálogo; agregar una colección la hace aparecer sola en el menú, al costo de necesitar reglas de agrupación y orden que el backend no conoce bien.
- **Menú manual** — `dashboard.vue` declara sus secciones y sus ítems, refiriendo a las colecciones solo por `snake_name`.

## Resultado

Manual. Qué se muestra y cómo se agrupa es una decisión de producto, no una propiedad de los datos: **tener control total del menú sale más barato que inventar reglas intrincadas que de todos modos acaban con excepciones hardcodeadas**. Hoy `dashboard.vue` fija etiquetas, íconos, colores y orden propios, y por eso el frontend ignora `order` y `priority` del payload.

### Consecuencias

- **Bueno:** el menú se lee de un vistazo y se reordena sin tocar el backend; una colección nueva no se cuela sola a la navegación.
- **Malo:** agregar una colección exige dos ediciones, una en el esquema y otra en el layout; si se olvida la segunda, la colección existe en la API pero es invisible.
- Deja sin efecto el `order` que devuelve la API para las colecciones de catálogo, que hoy viaja en `null` sin que nada se rompa.
