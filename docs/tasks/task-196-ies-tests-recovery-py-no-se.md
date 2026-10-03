---
type: task
id: task-196
title: ies/tests_recovery.py no se recolecta y 6 de sus 28 tests fallan
state: open
date: 2026-10-02
owner: ai
source: ["[[2026-10-02-comentarios-editables-y-valvula-de-admin]]"]
---

# ies/tests_recovery.py no se recolecta y 6 de sus 28 tests fallan

`pytest.ini` tiene `python_files = tests.py test_*.py *_tests.py`, así que `api/ies/tests_recovery.py` nunca entra a la suite por defecto. Corrido a mano el 2026-10-02 da 6 fallos y 22 pasan: cuatro por `AttributeError: recovery_views has no attribute '_send_recovery_email'` y dos por `KeyError: 'errors'` en `PasswordRecoveryConfirmViewTest`. Renombrarlo a `test_recovery.py` metería seis fallos a la suite hasta arreglarlos; conviene arreglar primero (los tests parchean un helper que ya no existe) y luego renombrar. `api/TESTING.md` ya anota el hueco de recolección.

## Criterios de aceptación

- [ ] Los seis tests pasan o se borran con razón escrita
- [ ] El archivo entra a la suite por defecto
- [ ] api/TESTING.md actualizado
