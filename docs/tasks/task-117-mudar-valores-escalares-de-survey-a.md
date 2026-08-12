---
type: task
id: task-117
title: Mudar valores escalares de Survey a GeneralQuestionResponse
state: closed
date: 2026-08-12
owner: ai
parent: "[[task-101]]"
source: ["[[2026-08-12-sesion-orquestada-a-b-captura-correcta]]"]
related: ["[[task-107]]", "[[task-106]]"]
---

# Mudar valores escalares de Survey a GeneralQuestionResponse

Sesión dedicada de la misma noche del 12 de agosto, decidida por Ricardo sin ambigüedad: «no dejemos deudas técnicas de algo tan fundamental, hoy es el día», aprovechando que no hay datos reales de `gen` que deban sobrevivir. `GeneralQuestionResponse` nació en [[task-106]]/[[task-107]] como tabla de respuesta que hoy solo carga el metadato `no_apply`; esta task muda también los valores, para que agregar preguntas deje de exigir columnas en Survey y muera la generalidad silenciosa de la regla name→columna.

## Resoluciones firmes de Ricardo (no rediscutir)

1. **Columnas tipadas**: `value_integer` y `value_boolean`, ambas nulas; `q_type` dicta cuál aplica. Descartado el JSON: los indicadores y el ETL consultan columnas tipadas sin castear.
2. **Sin columnas muertas**: las 6 columnas migradas se eliminan del Survey en la misma ventana — `academic_instances`, `admin_instances`, `media_plans`, `superior_plans`, `postgraduate_plans`, `is_centralized`.
3. **`measures_non_binary` EXCLUIDA**: es operacional, no alimenta ningún indicador; se queda como columna del Survey. Queda como la única GeneralQuestion cuya respuesta vive en columna; su regla de limpieza del toggle (false → anula `number_non_binary` de las filas) se conserva tal cual.
4. **Sin backfill**: no hay datos reales de gen; local se resiembra y las capturas de prueba se rehacen.

También descartados por completo en el diálogo: `is_estimated`, `no_data` y `comment` por respuesta (los dos primeros fueron invención de un agente sin contexto; ver el record). El FK a la pregunta ya es `PROTECT` por política de Ricardo: ninguna pregunta muere una vez implementado todo.

## Mapa de rebindeo

- `api/api/views/survey/serializers.py` — el nested `question_responses` gana los campos de valor; **muere la regla genérica name→columna** de limpieza por `no_apply` (la exención pasa a vivir dentro de la propia fila).
- `nuxt/app/composables/useGeneralSurvey.js` — `buildPayload` y los helpers de `question_responses`.
- `nuxt/app/composables/useGeneralValidation.js` — el grupo numérico e `is_centralized` leen de filas, no de columnas del Survey.
- `api/survey/general_validation.py` — la compuerta backend, espejo de la anterior.
- `GeneralGovernment.vue` — el v-model directo a `survey.is_centralized` pasa a la fila de respuesta.
- `GeneralNumberFields.vue` / `GeneralNumberQuestion.vue` — binding de los 5 numéricos.
- `GeneralGroupPanel.vue` — la rama genérica del resumen cuenta hoy por `survey[q.name]`.

## Restricciones

- Una sola migración por app: `survey/0009` se amplía (nada está deployado; ya depende de `question/0004`).
- Los e2e de gen (`nuxt/e2e/gen-*.test.ts`, 10 specs) y los 74 de pytest son la barra: en verde al cierre.
- Hallazgo heredado de la revisión: el frontend trata `''` como vacío y el backend solo `None` — hoy equivalente por ser todo entero/booleano; divergiría con columnas de texto. Resolverlo o documentarlo al mudar.

## Cierre (2026-08-12, madrugada, sesión dedicada duo+orchestrator)

Entregada la misma noche, sin commitear aún (pendiente de la revisión de Ricardo). A las 4 resoluciones firmes se sumaron 6 decisiones suyas en la sesión: la precarga de gobierno pasa de `Institution.save()`→columna a `Institution.save()`→fila (`_preload_centralized`, solo al crear el survey o sin respuesta previa); el hueco `''` vs `None` se resolvió normalizando en tres capas (`buildPayload` con `''`/`NaN`→null, `to_internal_value` del serializer, y la compuerta que trata ambos como vacío); qué preguntas ofrecen «No aplica» lo gobierna `addl_config.allow_no_apply` (sembrado en los 3 planes, mueren las dos listas `NO_APPLY_QUESTIONS`); el conteo del panel colapsado mide «resueltas» (con dato o `no_apply`), alineando la rama genérica con autoridades y poblaciones; se escribió el e2e del viaje de ida (spec propio en `gen-capture.test.ts`, probado que muerde: forzar null → 1 failed) y se borró el bloque comentado del modelo viejo en `survey/admin.py`.

Desviaciones de ejecutor aceptadas: la coerción `''`→`None` vive en `to_internal_value` (un `IntegerField` de DRF daría 400 antes de la compuerta), la property `value` de conveniencia en el modelo, y el test de ida como spec propio en vez de contaminar el spec de «No aplica» (el único flujo existente anulaba el entero capturado).

Deuda documentada por el revisor crítico independiente: (a) **asimetría `no_apply` sin `allow_no_apply`** — el serializer anula ambos valores ante cualquier `no_apply=true` sin mirar el flag, la compuerta sí lo exige; resultado coherente (bloquea), regla asimétrica, pendiente consciente; (b) el ejecutor backend aplicó **DDL manual sobre la BD local** (DROP ×6 + ADD ×2, la 0009 original ya estaba aplicada) sin consultar — falta de proceso registrada, sin daño (cero drift, pytest construye BD virgen); (c) la **enmienda de 0009 es silenciosamente invisible** en cualquier entorno donde la 0009 original ya corrió — mitigada en esta misma sesión: el probe de `django_migrations` entró al checklist pre-deploy del skill `deploy-api`; (d) la barra de 74 pytest no cubría la lógica nueva de gen — resuelta al cierre: Ricardo aprobó los tests y se escribieron 14 en `api/survey/tests.py` (compuerta por fila, upsert del serializer, precarga; con prueba de mordida en las tres rutas), suite en 88.

## Criterios de aceptación

- [x] `GeneralQuestionResponse` tiene `value_integer` y `value_boolean` y las respuestas escalares viven ahí
- [x] Las 6 columnas migradas ya no existen en Survey ni en ningún serializer
- [x] La regla genérica name→columna desapareció; la exención por `no_apply` vive en la fila
- [x] `measures_non_binary` sigue como columna operacional y su limpieza del toggle intacta
- [x] pytest y los e2e de gen en verde (88 pytest con los 14 nuevos de `survey/tests.py`, 38 e2e con el spec nuevo de ida); captura probada de ida y vuelta (e2e de ida + tests de serializer y probes del ejecutor y del revisor)
