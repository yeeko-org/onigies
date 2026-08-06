---
type: record
id: 2026-08-04-deploy-is-test-y-secciones-publicadas
title: Deploy de is_test y secciones publicadas (task-53)
date: 2026-08-04
---

# Deploy de is_test y secciones publicadas (task-53)

Bitácora del deploy a producción de la bandera `is_test` y las secciones publicadas solo en frontend. Referencia de diseño: [[adr-0009]]. Rango desplegado en `main`/`production`: 228fc29 (feature + migración 0013), 8bbe515 (tests + TESTING.md), 819c2ee (docs).

## Pre-deploy

- `pytest`: 68 passed sobre 819c2ee.
- Drift: único cambio de esquema es `is_test` en Institution, cubierto por la migración `0013_institution_is_test` (columna con `default=False`). Los cambios en `survey/models.py` (property `is_test`) y `example`/`survey` (`validate_flow_transition`) no llevan columna.
- `production` (8c86457) ancestro de `main` (819c2ee): fast-forward limpio de 3 commits. Push OK.

## Hallazgo: el servidor iba detrás del baseline del runbook

El skill `deploy-api` asume que tras el deploy anterior el servidor quedó en el último commit empujado (8c86457). **No era así: el servidor estaba en 0a96aed**, dos commits atrás. Los dos commits faltantes (0a96aed..8c86457) eran **solo docs y skills** (ni un `.py`, ni settings, ni migraciones) — los commits de cierre documental del deploy previo, que se empujaron a origin pero nunca se re-pullearon al server.

Verificación de que el hallazgo era benigno: `showmigrations` en el servidor reportó **cero migraciones pendientes** en su árbol (0a96aed), y el único archivo de migración en 0a96aed..819c2ee era `0013`. Es decir, el plan de migración era idéntico a lo planeado pese al baseline distinto. Se consultó a Ricardo antes de seguir (instrucción explícita de detenerse ante contradicción con el runbook) y dio luz verde.

**Lección para el runbook:** un deploy no termina hasta re-pullear el servidor, aunque el commit de cierre sea solo docs; si no, el server queda detrás de origin/production y el siguiente deploy arranca desde un baseline distinto al que el runbook asume. Pendiente anotarlo en el skill `deploy-api`.

## Runbook ejecutado (Yeeko, apionigies:6018)

- Backup: `pg_dump -Fc` con credenciales del `.env` → `_backups/onigies_pre_istest_20260804_192033.dump` (640K, pg_dump 16.14).
- `git pull origin production` → 819c2ee (ff limpio, arrastró los docs atrasados).
- `migrate`: aplicó solo `ies.0013_institution_is_test`.
- `makemigrations --check --dry-run`: «No changes detected».
- Sin cambios en requirements ni en `question/seed_data/`: sin pip install, sin seeds.
- Reload zero-downtime con SIGHUP al master de gunicorn (master 1304539 sobrevive, 3 workers nuevos).

## Frontend

Push a `production` disparó el build de Netlify automáticamente (misma rama). Skew benigno (campo aditivo). `/login` en netlify → 200 con el frontend nuevo.

## Siembra (dato de producción, propuesto antes de escribir)

`is_test=True` en 4 IES de prueba, evidentes por nombre, confirmadas por Ricardo: **63 UA PRUEBA, 64 A UNI2, 65 AIES Prueba, 68 Secretaria Edu Pub (SEP)**. Ricardo descartó explícitamente la 73 (Universidad Humani Mundial): es real.

## Smoke funcional (en vivo, vía inyección de cookie `auth_onigies` con tokens DRF temporales; solo lectura)

- (a) IES de prueba UA PRUEBA ve las 3 secciones en /respuestas (Datos base, los 4 ejes = cp, Buenas prácticas). ✓
- (b) IES real UNAM ve solo Buenas prácticas; deep-link `?tab=base` cae en el tab bp (único disponible, seleccionado). ✓
- (c) Dashboard de revisora: chip «Test» en las 4 marcadas; filtro «De prueba»=«Sí» → «Página 1 de 1 | 4 Resultados». ✓
- (d) Login de IES real intacto: hidratación completa vía token, y `POST /login/` con password incorrecto → 400 «Credenciales inválidas» (sin 500 por la serialización de is_test). ✓

Smoke de API: `/api/catalogs/all/` (canario del incidente 2026-07-29) y `/api/` → 200; `error.log` sin tracebacks tras el HUP.

**Nota de seguridad:** el smoke usó tokens DRF de usuarios reales (revisora jen.esc.med, IES ruuarte y ruuarte+test2). Son sus tokens de sesión normales (`get_or_create`); no se borran para no invalidar sesiones activas. Solo se navegó en lectura.
