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

Desde un worktree paralelo (otra copia del repo corriendo tests a la vez) hay que separar la base de pruebas, o las dos corridas se pisan `test_<base>`: `TOX_PARALLEL_ENV=<sufijo> pytest` hace que `pytest-django` le agregue el sufijo (`test_<base>_<sufijo>`). El worktree no trae el `.env` de la API: se enlaza el del checkout principal, parado en la carpeta de la API del worktree (`ln -s ~/dev/unam/onigies/api/.env .env`), y se usa el `venv/bin/pytest` del checkout principal; el enlace se borra al terminar.

Fuera de la suite, desde la raíz del monorepo: `api/venv/bin/pytest -c api/pytest.ini api/.claude/smoke_content_gate.py -q` — sonda de la compuerta del cuestionario (13 comprobaciones contra los endpoints reales: alta y baja abiertas, 403 cerradas, orden y fila puente automáticos, banderas, cierre de ida, 405 del catálogo de ajustes).

Dos sondas más de la captura cp, contra la base local, desde `api/`:

- `venv/bin/python manage.py shell -c "exec(open('.claude/smoke_cp_capture.py').read())"` — recorre el contrato real con una IES y una revisora (compuerta cerrada por fecha y por generales, lectura del eje, «Sí», PATCH por tipo, transición con faltantes, «No» con revisión activa y vuelta a «Sí», la revisora solo lee) e imprime los JSON; corre en una transacción que se revierte.
- `venv/bin/python manage.py shell -c "exec(open('.claude/gen_reviewer_transitions.py').read())"` — una revisora sin `is_staff` (como las reales) transiciona grupos y paquetes de generales por HTTP: aprobar y solicitar ajustes con el paquete enviado (201), aprobar con el paquete en borrador (400); corre en una transacción que se revierte.
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
| `flow/tests/test_comments.py` · `CommentEditTests` | edición y borrado de comentarios del timeline: cualquiera del mismo lado mientras la raíz esté en su turno; borrar un comentario puro quita la fila, el de una transición solo vacía el texto |
| `flow/tests/test_comments.py` · `CommentRoundTests` | editar y borrar solo en la ronda en curso: en la segunda vuelta la revisión ya no toca su comentario de la primera (403) y sí el nuevo; lo mismo para la IES; un movimiento dentro del mismo lado no abre ronda |
| `flow/tests/test_comments.py` · `CommentRootTurnTests` | regresión: el alta de comentarios sigue el turno de la raíz, no el rol del status propio |
| `flow/tests/test_admin_override.py` · `AdminOverrideTests` | válvula de admin: solo `is_admin`, nunca sobre la raíz ni con la raíz del lado de la IES, solo destinos de la revisión, rechaza un destino legal (400, va por el menú), comentario obligatorio; el motivo no se borra (403) y solo `is_admin` lo corrige; `transitions/` sigue rechazando lo que sale del grafo; el comentario de una transición dentro del grafo no es cambio administrativo |
| `flow/tests/test_admin_override.py` · `AdminTargetCatalogTests` | `admin_target_names` derivado del grafo y viajando como `admin_targets` en cada fila del catálogo |
| `flow/tests/test_admin_override.py` · `AdminOverrideChildrenRuleTests` | la válvula salta `next_statuses` pero no la regla de hijos |
| `answer/tests.py` · `ProvisioningTests` | `Institution.save` aprovisiona ObservableResponse y GroupResponse (idempotente, backfill); `approve_groups_without_capture` lleva a `cp_approved` los grupos sin captura en `cp_pre_start`/`cp_filling`, no toca `cp_not_present` ni los grupos con captura |
| `answer/tests.py` · `InitValueTests` | pregunta inicial: el «No» lleva el árbol a `cp_not_present`, la vuelta a «Sí» reabre, bloqueos con revisión activa, eje fuera de turno y revisora |
| `answer/tests.py` · `ObservableFlowRulesTests` | ganchos del observable y del grupo: pregunta inicial sin responder, `cp_not_present` como hijo válido, pospuesta con grupos resueltos, la revisión espera a que la IES envíe el eje, el grupo sin captura aprobado no frena `cp_completed` y rechaza el reajuste voluntario |
| `answer/tests.py` · `GroupValidationTests` | reglas de completitud por tipo (A, B, alcance, planes, especial) |
| `answer/tests.py` · `CaptureGateTests` | compuerta de respuesta (fecha + generales validadas), solo cierra a la IES |
| `answer/tests.py` · `CaptureApiTests` | endpoints `/axis_value/`, `/observable_response/`, `/group_response/`: cerco por institución, revisora solo lee, upsert y promoción, `completion` embebido; el alcance no ofrece los sectores que la IES declaró ausentes en generales (`is_present=False`) y los «No aplica» de autoridades (`no_apply`), sí los nulos |
| `answer/tests.py` · `InstrumentProtectionTests` | regresión: `confirm-delete` de una pregunta con respuestas da 409 (manejador global de `ProtectedError`/`RestrictedError` en `api/exception_handler.py`) y la respuesta sobrevive |
| `survey/tests.py` · `GeneralValidationTests` | reglas de completitud de las generales: qué cuenta como respuesta y cuándo exime «No aplica» |
| `survey/tests.py` · `GeneralReviewTurnTests` | la revisión no transiciona un grupo `gen_completed` con el paquete en `gen_draft`; sí con `gen_sent` |
| `example/tests.py` · `PracticeReviewTurnTests` | lo mismo en bp: práctica `bp_completed` con el paquete en `bp_draft` contra `bp_sent` |
| `example/tests.py` · `CriterionCommentsLockTests` | la nota privada por criterio (`FeatureGoodPractice.comments`): la revisión la cambia solo con el paquete en su turno, un valor sin cambios pasa fuera de turno, y el `''` que reenvía la IES se descarta sin perder su guardado |
| `example/tests.py` · `GoodPracticeFenceTests` | cerco de `/good_practice/`: sin sesión 401, otra IES no lee ni borra (404, la fila sigue), no crea ni mueve prácticas al paquete ajeno (403); la dueña edita, crea y borra; la revisora lista las de todas |
| `example/tests.py` · `CriterionFieldsTests` | `/feature_good_practice/`: la IES no califica (`final_option` se descarta), el criterio no cambia de práctica; el alta suelta solo para la IES dueña (otra IES y la revisora, 403) |
| `example/tests.py` · `PracticeContentTurnTests` | el contenido de bp sigue el turno en el servidor: la IES no edita criterio ni práctica ni la borra con el envío en `bp_sent` (403, sin cambios), sí en `bp_draft`; su `final_value` se descarta; la revisión califica con el envío enviado y su escritura de contenido se descarta |
| `survey/tests.py` · `GeneralQuestionResponseSyncTests` | upsert de `question_responses` anidado: columna por `q_type`, normalización del `''`, sin duplicar |
| `survey/tests.py` · `PreloadCentralizedTests` | precarga de la forma de gobierno desde el catálogo de instituciones |
| `indicator/test_add_tsu_sector.py` · `AddTsuSectorTests` | `add_tsu_sector` idempotente: la segunda corrida no duplica sector, presencia, pregunta ni respuesta; no pisa lo que la IES ya capturó y pasa a «No» la presencia nula |
| `question/tests.py` · `SeedTextOwnershipTests` | de los textos manda el dashboard; `--overwrite-texts` los repone, salvo `Axis.name` |
| `question/tests.py` · `TypeWeightSyncTests` | el re-seed repone la fila puente borrada, no pisa un `weight` capturado, y deja los conteos 2026 (41/41/35/1/1/1) |
| `question/tests.py` · `FinalWeightTests` | ponderación efectiva: la propia; la del tipo solo cuando el observable tiene exactamente el trío estándar (A + orgánica + sectorial); `None` sin fila puente |
| `ies/tests.py` · `LoginPayloadInstitutionTests` | `is_test` viaja en el payload de `/login/` |
| `ies/tests_recovery.py` · `PasswordRecovery*` | token de recuperación y las tres vistas del flujo de contraseña. El nombre del archivo no entra en `python_files` de `pytest.ini`: la suite por defecto no lo recoge, se corre nombrándolo |
| `email_send/tests.py` | perfiles y plantillas, `send_template_email` / `send_simple_email`, `EmailRecord` |

## Fixtures y credenciales

No hay credenciales compartidas: cada clase construye sus datos en `setUpTestData`.

- `FlowSecurityTestCase` (`flow/tests/base.py`) — base reutilizable: catálogo de status, periodo abierto, dos instituciones con paquetes y usuarios.
- `CpCatalogTestCase` (`answer/tests.py`) — catálogo cp mínimo a mano (un eje, tres observables), periodo con `cp_open_at` pasado, dos IES con generales en `gen_finished` y una revisora; helper `force()` fija un status sin pasar por el motor.
- `GeneralQuestionTestCase` (`survey/tests.py`) — catálogo mínimo a mano en vez de `load_questionnaire`. Los grupos y preguntas se crean **antes** que la institución: `Institution.save` aprovisiona los `GeneralGroupResponse` sobre lo que exista en ese momento.
- `seed_questionnaire()` (`question/tests.py`) — `InitQuestionTypes()` + `load_sectors` + `load_questionnaire` completo; el contrato del re-seed solo se ve con el cuestionario entero. Su helper `run_seed()` pasa `--force`: desde el candado de siembra, `load_questionnaire` aborta si `QuestionnaireSettings.seeded_at` ya tiene fecha.
- `TestInstitutionPeriodLockTests` no hereda de `FlowSecurityTestCase` a propósito: necesita el periodo ya cerrado antes de crear las instituciones.
