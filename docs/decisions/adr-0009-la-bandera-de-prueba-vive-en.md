---
type: decision
id: adr-0009
title: La bandera de prueba vive en Institution y las secciones publicadas en una constante de frontend
state: accepted
date: 2026-08-04
origin: ricardo
deliberation: dialogued
rationale: recorded
source: ["[[task-53]]"]
affects: ["api/ies/models.py", "nuxt/app/pages/respuestas/[period].vue", "nuxt/app/pages/respuestas/index.vue"]
---

# La bandera de prueba vive en Institution y las secciones publicadas en una constante de frontend

Dos mecanismos que se combinan, definidos en diálogo sobre el reconocimiento del código (ver [[task-53]]):

## 1. Institución de prueba: `Institution.is_test`

`BooleanField(default=False)` en `Institution`. Una IES de prueba es una institución ficticia completa, con survey y datos desechables.

- **Herencia**: los usuarios la heredan por su FK `User.institution`; no hay bandera en `User`. Las invitaciones ya llevan la institución, así que la marca se propaga sola. La revisora (sin institución) no se ve afectada.
- **Semántica**: levanta las restricciones de sección en el frontend (ve todo) y los candados de cierre de periodo en el backend (`is_bp_submission_closed` / `is_gen_submission_closed` no la bloquean), para poder probar el flujo completo de envío y validación.
- **Exclusión aguas abajo**: todo cálculo, indicador o exporte futuro debe excluir `is_test=True`. Queda anotado en `api/CLAUDE.md` porque hoy no existe ninguno.
- **Llegada al frontend**: gratis, porque los serializers de `Institution` usan `fields='__all__'`.
- **Siembra**: al hacer deploy se marcan como test las IES de prueba que ya existen en producción (son evidentes); puede ocurrir en otra sesión.

## 2. Sección publicada o interna: constante en el frontend

`PUBLISHED_SECTIONS = ['bp']` en un módulo único, consumido por los dos lugares que enumeran secciones (`respuestas/[period].vue` y `respuestas/index.vue`). **'base' no está publicada**: se prueba internamente antes de abrirse a las IES — ese es el motivo de la task.

- Regla: IES real → solo secciones publicadas; IES de prueba → todo.
- Granularidad gruesa: `base` / `bp` / `cp` en bloque (los ejes no se publican uno por uno).
- **Es transicional**: el mecanismo definitivo se decide cuando Rubén (encargado de ONIGIES) apruebe cada sección; entonces se evalúa si sube a BD. Por eso no se crea entidad «Sección» — en el backend el grupo (`bp`/`cp`/`gen`) es solo un choice de texto en `flow.Status` y no hay dónde colgar un interruptor sin inventar esquema.

## Descartado

- Bandera en `User`: duplicaría lo que la FK ya da y exigiría sembrarla en cada invitación.
- Catálogo de secciones en BD: esquema nuevo para un interruptor transicional.
- `Period.results_published` no se toca ni se absorbe: está reservado para la futura página pública de resultados.
