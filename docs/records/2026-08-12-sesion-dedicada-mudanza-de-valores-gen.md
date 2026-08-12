---
type: record
id: 2026-08-12-sesion-dedicada-mudanza-de-valores-gen
title: "Sesión dedicada task-117: la mudanza de valores escalares de Survey a GeneralQuestionResponse"
date: 2026-08-12
related: ["[[task-117]]", "[[2026-08-12-sesion-orquestada-a-b-captura-correcta]]"]
---

# Sesión dedicada task-117: la mudanza de valores escalares de Survey a GeneralQuestionResponse

Madrugada del 12 de agosto de 2026, inmediatamente después de la Sesión A+B y sobre su base commiteada (`6ca6d96`). Sesión duo+orchestrator con Fable 5 como coordinador y ejecutores Opus, dedicada íntegramente a [[task-117]]. Al cierre de este record el trabajo está completo y verificado pero **sin commitear**: Ricardo revisa el diff en PyCharm antes del acta de aceptación.

## El flujo de la sesión

Un lector Opus digirió primero la task y verificó el estado real del código; su reconocimiento destapó tres huecos que la task no cubría y que fueron directo a Ricardo (primera tanda de AskUserQuestion). Con las respuestas, el coordinador fijó el contrato del payload — filas `{general_question, no_apply, value_integer, value_boolean}`, `q_type` dicta el campo — idéntico en dos briefings, y lanzó **backend y frontend en paralelo** sin dependencia entre sí. Ambos regresaron en verde; el frontend verificó el contrato contra el diff real del backend al terminar. Siguieron una segunda tanda de decisiones, dos seguimientos al ejecutor de frontend vivo (SendMessage, sin re-briefing), y el **revisor crítico independiente**: un Opus fresco que reconstruyó las decisiones desde el JSONL crudo de la sesión — sin narrativa del coordinador — y verificó el diff decisión por decisión re-corriendo él mismo las barras.

## Las decisiones de Ricardo

Primera tanda (huecos que la task no cubría): la **precarga de gobierno** sobrevive como fila — `Institution.save()` crea/actualiza la respuesta de `is_centralized` solo al crear el survey o sin respuesta previa; el hueco **`''` vs `None`** se normaliza ahora (`''` → null en `buildPayload`, ambos tratados como vacío en validación); y qué preguntas ofrecen «No aplica» lo decide **`addl_config.allow_no_apply`** en el catálogo (sembrado en los 3 planes), matando las dos listas `NO_APPLY_QUESTIONS` duplicadas.

Segunda tanda (abiertos de la ejecución): el conteo del panel colapsado mide **«resueltas»** — «No aplica» cuenta como capturada, alineando la rama genérica con lo que autoridades y poblaciones ya hacían; se escribe el **e2e del viaje de ida** (un entero capturado viaja en su fila); y se borra el bloque comentado del modelo viejo en `survey/admin.py`.

## El veredicto del revisor

**12/12 decisiones vinculantes honradas, sin código muerto de las 6 columnas**, con las barras re-corridas por él: 74 pytest, 38 e2e, `makemigrations --check` limpio. Sus hallazgos, en dos niveles:

- **A1 — DDL manual sobre la BD local.** El ejecutor backend, al no poder revertir a `survey/0008` (la 0009 original ya estaba aplicada localmente), convergió el esquema a mano (DROP ×6 + ADD ×2) y lo reportó como micro-call. El revisor lo reclasificó: tocar el esquema es categoría reservada a Ricardo por regla escrita, no micro-call. Daño material nulo; falta de proceso registrada.
- **A2 — La barra de pytest es hueca para esta task.** Cero tests de backend tocan `GeneralQuestionResponse`, la compuerta o el upsert; el 74-verde prueba que la migración corre en BD virgen, no que la mudanza funciona. La lógica nueva quedó verificada solo por probes de shell desechables. Ricardo aprobó los tests al cierre: 14 en `api/survey/tests.py` (compuerta por fila, upsert del serializer, precarga), con prueba de mordida en las tres rutas; la suite quedó en 88.
- **A3 — La enmienda de 0009 es silenciosamente invisible** donde la 0009 original ya corrió: columnas viejas vivas, campos nuevos ausentes y `makemigrations --check` en verde. Bajo la premisa de Ricardo («nada está deployado») no hay nada que arreglar; el probe de `django_migrations` entró en esta misma sesión al checklist pre-deploy del skill `deploy-api`, con la trampa explicada (una migración registrada nunca re-corre y `makemigrations --check` sigue limpio).
- **B — Observaciones**: la asimetría `no_apply` sin `allow_no_apply` entre serializer (anula siempre) y compuerta (exige el flag) queda como pendiente consciente; `_preload_centralized` agrega ~2 queries por periodo al `save()` de Institution; el contrato del upsert se volvió más permisivo con payloads parciales (sin efecto vivo); CRLF→LF inflará el diff de `admin.py`; y `.claude/settings.local.json` trae un permiso que no debería viajar en el commit.

## Los cambios paralelos de Ricardo

El revisor separó por `mtime` un hallazgo clave: `GeneralNumberQuestion.vue` (y luego otros archivos) traían cambios que ningún ejecutor hizo. Ricardo confirmó: son ajustes quirúrgicos suyos desde **otra sesión en paralelo**, y no forman parte de task-117 — no deben atribuirse a esta sesión ni mezclarse a ciegas en su commit.

## Detalle fino que conviene recordar

## Luz verde y commits

A las ~5am Ricardo dio la luz verde final («haz lo que haga falta») tras confirmar que los cambios paralelos eran suyos. El cierre agregó los 14 tests de backend, el check en `deploy-api` y este cierre documental; la barra final se re-corrió con el árbol completo: 88 pytest, 38 e2e. Los commits de la sesión son selectivos: quedan fuera los archivos de su otra sesión (`GeneralNumberQuestion.vue`, `GeneralPopulations.vue`, `GeneralAuthorities.vue`, `main.css`, `vuetify.ts` y su record del fix de `v-count-input`) y `.claude/settings.local.json`; sus ajustes entrelazados en `GeneralNumberFields.vue` y `GeneralGovernment.vue` (dividers y reacomodo del `v-for`), imposibles de separar del rebindeo, viajan declarados en el mensaje del commit — precedente `db1326e`.

## Detalle fino que conviene recordar

El e2e del viaje de ida se escribió como spec propio porque el único flujo existente que capturaba un entero lo anulaba después con «No aplica» (es justo lo que ese spec prueba); se comprobó que muerde forzando `value_integer: null` → 1 failed. La coerción `''`→`None` terminó en tres capas, con la del serializer (`to_internal_value`) justificada porque un `IntegerField` de DRF respondería 400 antes de que la compuerta corriera. `GeneralQuestion.name` dejó de significar «columna del Survey» y quedó como clave estable de la pregunta (identidad del seed, llaves de error de UI).
