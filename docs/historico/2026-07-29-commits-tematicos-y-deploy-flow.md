---
type: historico
id: 2026-07-29-commits-tematicos-y-deploy-flow
title: Reorganización en commits temáticos y segundo deploy de flow a producción
state: archivado
date: 2026-07-29
related: ["[[adr-0001]]"]
---

# Reorganización en commits temáticos y segundo deploy de flow a producción

> Inmutable. Este documento no se edita: registra algo que ya pasó. Si algo de
> aquí resultó estar mal, se escribe otro documento que lo corrija y se enlaza.

**Cuándo:** 2026-07-29
**Quiénes:** Ricardo + Claude (sesión de Claude Code)
**De dónde sale:** cierre de la sesión de reorganización de commits y deploy.

## Contenido

El working tree (rama `production`) acumulaba ~60 archivos sin commitear mezclando varios frentes de trabajo. Se aplicó por primera vez la estrategia de [[adr-0001]]:

1. `main` se fast-forwardeó hasta `production` (3 commits de junio que solo vivían allá) y sobre esa base se crearon 5 commits temáticos, con los destinados a producción primero:
   - `fde3295` — Flow backend: notificaciones por correo a la IES, permisos por institución (`flow/permissions.py`), `Period.submission_deadline` + cierre automático del envío, seed declarativo con `StatusDef`, lock anti-TOCTOU en `execute_transition`.
   - `3ffe820` — Flow frontend: `hint`/`hint_wait` por rol, tabs en /respuestas, deadline visible, mocks e2e y test `respuestas-tabs`.
   - `d41054a` — Archivos servidos bajo `/files/` (rename desde `/media/` por colisión con el sitio legado).
   - `78fde6b` — Docs y skills (planes a `docs/plans/`, skills cp-questionnaire y gen-general-info).
   - `9eadc9e` — Seed declarativo del cuestionario (**solo main**, no desplegado).
2. `production` avanzó con `--ff-only` hasta `78fde6b` y se pushearon ambas ramas. Se aceptó un desfase de minutos (front nuevo + API viejo) mientras corría el runbook, en vez de bloquear la publicación de Netlify.
3. Deploy del API en Yeeko, sin incidentes:
   - pg_dump previo (616K) en `api/_backups/`.
   - Migraciones `flow 0007-0008` e `ies 0011` aplicadas.
   - `seed_flow`: 32 Status actualizados, 0 creados; el riesgo previsto (borrado de `gen_pre_start`/`gen_filling` bloqueado por FK PROTECT) no aplicó — esos statuses nunca existieron en prod y los 62 `GeneralPackage` ya tenían status.
   - Cutover `media/` → `files/`: la carpeta `files/` vieja (copia parcial de jul-04, subconjunto estricto) se apartó a `api/_backups/files_stale_jul04` y `media/` se renombró a `files/`.
   - Recarga con `sudo kill -HUP` al master de gunicorn (corre como root; `supervisorctl` sigue roto).
   - Smoke: API root 200, evidencia PDF servida bajo `/files/` con 200, log sin errores nuevos, front 200 en Netlify y en el bridge de UNAM.

## Qué salió de aquí

- [[adr-0001]] — la estrategia de ramas que esta sesión estrenó.
- Pendientes que quedaron abiertos:
  - 🚧 [ask:ricardo] Confirmar en la UI de Netlify que el build del push quedó publicado y hacer smoke manual con login (/respuestas, un envío de BP, abrir una evidencia).
  - 🚧 [code:docs/meets/26_junio_26/seguimiento_pendientes.md] Marcar el §5 (cutover de archivos en el server) como hecho.
  - 🚧 [code:.claude/skills/deployment/references/roadmap.md] Reflejar el cutover `/files/` en el roadmap de la skill deployment.
  - 🚧 [open:confirmación de operación estable en prod] Borrar los respaldos del server (`api/_backups/`: dump y `files_stale_jul04`).
  - 🚧 [code:api/core/settings/__init__.py] Hardening pendiente en prod: `DEBUG=True` (se asomó en un 404 durante el smoke) y `CORS_ORIGIN_ALLOW_ALL=True` → allowlist.
  - 🚧 [open:fase de borrado §8 del plan de flujo] Quitar `StatusControl` y los campos/modelos viejos coexistentes (ver `docs/plans/flux/PLAN_flujo_validacion.md`).
  - 🚧 [open:respuestas del cliente a docs/questions/dudas_a_resolver_con_cliente.md] Resolver las dudas del cuestionario y decidir la ventana para desplegar el seed (`9eadc9e`) a producción.
