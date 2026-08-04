# Testing — api

## Niveles montados

Solo pruebas de backend con `pytest` + `pytest-django`, sobre `TestCase` / `APITestCase` de Django. No hay tests de unidad puros separados: cada clase toca base de datos porque lo que se prueba son reglas de flujo, permisos y serialización. Los e2e viven en `nuxt/` (ver `nuxt/TESTING.md`).

## Comandos

El intérprete es el del virtualenv (`venv/bin/python` en `api/`); la configuración está en `pytest.ini`.

```bash
pytest                                  # suite completa
pytest flow/tests.py                    # un archivo
pytest flow/tests.py::TurnNotificationTests   # una clase
pytest -q -k periodo                    # por nombre
```

## Qué cubre cada clase

| Archivo · clase | Cubre |
|---|---|
| `flow/tests.py` · `TransitionOwnershipTests` | una IES ajena no transiciona objetos de otra institución; la dueña y la revisora sí |
| `flow/tests.py` · `EventOwnershipTests` | mismo cerco sobre comentarios y timeline |
| `flow/tests.py` · `PackageActionOwnershipTests` | `discard` y listado no filtran paquetes de otras instituciones |
| `flow/tests.py` · `InitialStatusWiringTests` | todo participante creado sin status recibe el default de su grupo; `assign_auto_status` promueve en la primera captura y no revierte objetos avanzados |
| `flow/tests.py` · `SentAtPersistenceTests` | regresión: el envío persiste `sent_at` en base y el reenvío no lo pisa |
| `flow/tests.py` · `TestInstitutionPeriodLockTests` | con el periodo cerrado, el envío se rechaza para una IES real y pasa para una IES `is_test` (ganchos bp y gen, más los guards de vista `discard`/`reopen`); la revisora dictamina después del cierre |
| `flow/tests.py` · `TurnNotificationTests` | correo a la IES cuando el turno de un objeto raíz vuelve a ella o llega a un status final; nunca a revisoras ni por transiciones de hijo |
| `ies/tests.py` · `LoginPayloadInstitutionTests` | `is_test` viaja en el payload de `/login/` por `institution` e `institution_details` (red contra un cambio de `fields='__all__'` a lista explícita) |
| `ies/tests_recovery.py` | modelo del token de recuperación y las tres vistas del flujo de contraseña |
| `email_send/tests.py` | perfiles y plantillas de correo, `send_template_email` / `send_simple_email`, `EmailRecord` |

## Fixtures y credenciales

No hay credenciales compartidas: cada clase construye sus datos en `setUpTestData`. Dos patrones a conocer antes de escribir tests nuevos:

- `FlowSecurityTestCase` (`flow/tests.py`) es la base reutilizable: siembra el catálogo de status (`InitStatus()` + `seed_flow()`), un periodo abierto y dos instituciones con sus paquetes y usuarios. Hereda de ahí si no necesitas condiciones de periodo distintas.
- `TestInstitutionPeriodLockTests` **no** hereda de esa base a propósito: necesita el periodo ya cerrado antes de crear las instituciones, porque `Institution.save` aprovisiona los surveys sobre los periodos que existen en ese momento.
