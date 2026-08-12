---
type: decision
id: adr-0008
title: El contenido de las generales se escribe contra Survey, con sincronización total de poblaciones
state: accepted
date: 2026-08-04
origin: ricardo
deliberation: dialogued
rationale: recorded
source: ["[[2026-08-04-sesion-seccion-informacion-base]]"]
affects: ["api/api/views/survey/serializers.py", "nuxt/app/composables/useGeneralSurvey.js"]
related: ["[[adr-0012]]"]
---

# El contenido de las generales se escribe contra Survey, con sincronización total de poblaciones

## Contexto y planteamiento del problema

Al rehacer la captura de la sección de información base (flujo `gen`) espejando Buenas Prácticas, había que decidir dónde escribe la IES el contenido. A diferencia de bp, las respuestas de gen no viven en el wrapper de flujo: están repartidas en columnas de `Survey`, el M2M `sectors` y filas de `PopulationQuantity`; los `GeneralGroupResponse` solo llevan flujo.

## Decisión

1. **El contenido se escribe siempre contra `Survey`** (PATCH a `/survey/{id}/`): escalares, `sectors` y `population_quantities` anidadas. El wrapper por grupo no acepta contenido; el flujo va por los endpoints genéricos de `/flow/`. Se descartó el serializer por grupo con campos virtuales: más código y la traducción grupo→destino metida en el backend, cuando el espejo de bp que importa es el ciclo de flujo y la UX, no el destino físico del save.
2. **`population_quantities` tiene semántica de sincronización total**: si la clave viaja, la lista ES el estado final (upsert por `(survey, sector)`, borrado por omisión); si no viaja, no se toca nada — por eso el frontend guarda con PATCH, nunca PUT.
3. **Solo persisten filas con algún conteo.** La existencia de una población vive en `sectors`; una fila sin hombres ni mujeres no aporta y la sincronización la borra. Ricardo evaluó pre-sembrar la matriz completa en null (la idea original de `no_apply`) para facilitar la lectura pública, y se descartó: la fila null de un sector no marcado no significa nada sin cruzar contra `sectors`, y chocaría con el borrado por omisión. La lectura uniforme se resolverá en la capa de lectura del sitio público, con la respuesta de [[task-56]] en la mano.
4. **`no_apply` no se captura hoy** ni en poblaciones ni en autoridades; su destino depende de Rubén ([[task-56]]).

## Enmienda (2026-08-11): el punto 3 quedó modificado

[[adr-0012]] cambia **el punto 3 de arriba y la premisa del punto 4**. Ya no es cierto que solo persistan filas con algún conteo: la existencia de una población deja de vivir en `sectors` y pasa a una columna de tres estados en `PopulationQuantity`, y la fila se persiste en cuanto hay respuesta —sí o no— aunque no lleve ningún conteo. `Survey.sectors` sobrevive como propiedad derivada, no como fuente.

**Los puntos 1 y 2 siguen íntegros y vigentes:** el contenido se escribe siempre contra el Survey con un solo PATCH, y `population_quantities` conserva su semántica de sincronización total. Por eso esta decisión no se marca como reemplazada — solo uno de sus cuatro puntos cambió, y retirarla entera dejaría sin autoridad escrita lo que sí sigue gobernando.

No leer los puntos 3 y 4 sin leer [[adr-0012]].

## Consecuencias

- Un solo endpoint de escritura y el guardar de cualquier grupo persiste la sección entera (los 5 grupos comparten recurso).
- `PopulationQuantity.name` pasó a opcional (migración 0008 de survey) para capturar filas de sectores estándar sin inventar nombres.
- Quien lea composición debe cruzar `sectors` (existencia) con `population_quantities` (conteos); «Titular de la IES» no entra a `sectors` y se lee solo de sus filas.
