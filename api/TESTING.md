# Testing — api

## Niveles montados

Solo backend: `pytest` + `pytest-django` sobre `TestCase` / `APITestCase`. Toda clase toca base de datos porque lo que se prueba son reglas de flujo, permisos y serialización. Los e2e viven en `nuxt/` (ver `nuxt/TESTING.md`).

## Comandos

Intérprete del virtualenv (`venv/bin/python` en `api/`); configuración en `pytest.ini`.

```bash
pytest                                        # suite completa
pytest flow/tests/test_notifications.py       # un archivo
pytest flow/tests/test_notifications.py::TurnNotificationTests   # una clase
pytest -q -k periodo                          # por nombre
```

Fuera de la suite, desde la raíz del monorepo: `api/venv/bin/pytest -c api/pytest.ini api/.claude/smoke_content_gate.py -q` — sonda de la compuerta del cuestionario (13 comprobaciones contra los endpoints reales: alta y baja abiertas, 403 cerradas, orden y fila puente automáticos, banderas, cierre de ida, 405 del catálogo de ajustes).

Dos sondas más de la captura cp, contra la base local, desde `api/`:

- `venv/bin/python manage.py shell -c "exec(open('.claude/smoke_cp_capture.py').read())"` — recorre el contrato real con una IES y una revisora (compuerta cerrada por fecha y por generales, lectura del eje, «Sí», PATCH por tipo, transición con faltantes, «No» con revisión activa y vuelta a «Sí», la revisora solo lee) e imprime los JSON; corre en una transacción que se revierte.
- `venv/bin/python .claude/measure_axis_queries.py [axis_value_id] [user_id] [-v]` — consultas y tiempo de `GET /axis_value/<id>/`; los ids por defecto (293, 80) son de la base local.

## Qué cubre cada clase

| Archivo · clase | Cubre |
|---|---|
| `flow/tests/test_ownership.py` · `TransitionOwnershipTests` | una IES ajena no transiciona objetos de otra institución |
| `flow/tests/test_ownership.py` · `EventOwnershipTests` | el mismo cerco sobre comentarios y timeline |
| `flow/tests/test_ownership.py` · `PackageActionOwnershipTests` | `discard` y listado no filtran paquetes ajenos |
| `flow/tests/test_status_wiring.py` · `InitialStatusWiringTests` | status default al crear; `assign_auto_status` promueve en la primera captura y no revierte |
| `flow/tests/test_status_wiring.py` · `SentAtPersistenceTests` | regresión: el reenvío no pisa `sent_at` |
| `flow/tests/test_period_lock.py` · `TestInstitutionPeriodLockTests` | periodo cerrado: bloquea a la IES real, exime a la `is_test`, deja dictaminar a la revisora |
| `flow/tests/test_notifications.py` · `TurnNotificationTests` | correo a la IES cuando el turno vuelve a ella o llega a status final; nunca a revisoras ni por hijos |
| `flow/tests/test_attachments.py` · `AttachmentTests` | tope de 30 MB, borrado del archivo físico, y la descarga vía endpoint (permisos, `is_public`, 404 anti-enumeración, `?redirect=false`) |
| `answer/tests.py` · `ProvisioningTests` | `Institution.save` aprovisiona ObservableResponse y GroupResponse (idempotente, backfill) |
| `answer/tests.py` · `InitValueTests` | pregunta inicial: el «No» lleva el árbol a `cp_not_present`, la vuelta a «Sí» reabre, bloqueos con revisión activa, eje fuera de turno y revisora |
| `answer/tests.py` · `ObservableFlowRulesTests` | ganchos del observable y del grupo: pregunta inicial sin responder, `cp_not_present` como hijo válido, pospuesta con grupos resueltos, y la revisión espera a que la IES envíe el eje |
| `answer/tests.py` · `GroupValidationTests` | compuerta de contenido por tipo (A, B, alcance, planes, especial) |
| `answer/tests.py` · `CaptureGateTests` | compuerta de respuesta (fecha + generales validadas), solo cierra a la IES |
| `answer/tests.py` · `CaptureApiTests` | endpoints `/axis_value/`, `/observable_response/`, `/group_response/`: cerco por institución, revisora solo lee, upsert y promoción, `completion` embebido |
| `survey/tests.py` · `GeneralValidationTests` | compuerta de contenido de las generales: qué cuenta como respuesta y cuándo exime «No aplica» |
| `survey/tests.py` · `GeneralQuestionResponseSyncTests` | upsert de `question_responses` anidado: columna por `q_type`, normalización del `''`, sin duplicar |
| `survey/tests.py` · `PreloadCentralizedTests` | precarga de la forma de gobierno desde el catálogo de instituciones |
| `question/tests.py` · `SeedTextOwnershipTests` | de los textos manda el dashboard; `--overwrite-texts` los repone, salvo `Axis.name` |
| `question/tests.py` · `TypeWeightSyncTests` | el re-seed repone la fila puente borrada, no pisa un `weight` capturado, y deja los conteos 2026 (41/41/35/1/1/1) |
| `question/tests.py` · `FinalWeightTests` | ponderación efectiva: la propia; la del tipo solo cuando el observable tiene exactamente el trío estándar (A + orgánica + sectorial); `None` sin fila puente |
| `ies/tests.py` · `LoginPayloadInstitutionTests` | `is_test` viaja en el payload de `/login/` |
| `ies/tests_recovery.py` | token de recuperación y las tres vistas del flujo de contraseña |
| `email_send/tests.py` | perfiles y plantillas, `send_template_email` / `send_simple_email`, `EmailRecord` |

## Fixtures y credenciales

No hay credenciales compartidas: cada clase construye sus datos en `setUpTestData`.

- `FlowSecurityTestCase` (`flow/tests/base.py`) — base reutilizable: catálogo de status, periodo abierto, dos instituciones con paquetes y usuarios.
- `CpCatalogTestCase` (`answer/tests.py`) — catálogo cp mínimo a mano (un eje, tres observables), periodo con `cp_open_at` pasado, dos IES con generales en `gen_finished` y una revisora; helper `force()` fija un status sin pasar por el motor.
- `GeneralQuestionTestCase` (`survey/tests.py`) — catálogo mínimo a mano en vez de `load_questionnaire`. Los grupos y preguntas se crean **antes** que la institución: `Institution.save` aprovisiona los `GeneralGroupResponse` sobre lo que exista en ese momento.
- `seed_questionnaire()` (`question/tests.py`) — `InitQuestionTypes()` + `load_sectors` + `load_questionnaire` completo; el contrato del re-seed solo se ve con el cuestionario entero. Su helper `run_seed()` pasa `--force`: desde el candado de siembra, `load_questionnaire` aborta si `QuestionnaireSettings.seeded_at` ya tiene fecha.
- `TestInstitutionPeriodLockTests` no hereda de `FlowSecurityTestCase` a propósito: necesita el periodo ya cerrado antes de crear las instituciones.
