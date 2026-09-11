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
- `GeneralQuestionTestCase` (`survey/tests.py`) — catálogo mínimo a mano en vez de `load_questionnaire`. Los grupos y preguntas se crean **antes** que la institución: `Institution.save` aprovisiona los `GeneralGroupResponse` sobre lo que exista en ese momento.
- `seed_questionnaire()` (`question/tests.py`) — `InitQuestionTypes()` + `load_sectors` + `load_questionnaire` completo; el contrato del re-seed solo se ve con el cuestionario entero. Su helper `run_seed()` pasa `--force`: desde el candado de siembra, `load_questionnaire` aborta si `QuestionnaireSettings.seeded_at` ya tiene fecha.
- `TestInstitutionPeriodLockTests` no hereda de `FlowSecurityTestCase` a propósito: necesita el periodo ya cerrado antes de crear las instituciones.
