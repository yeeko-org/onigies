---
type: record
id: 2026-08-04-deploy-de-informacion-base-reparacion-de
title: Deploy de información base, reparación de sent_at y endurecimiento
date: 2026-08-04
---

# Deploy de información base, reparación de sent_at y endurecimiento

Sesión operada en modo duo (coordinador + ejecutores Opus). Deploy a producción del rango 1b3e288..cc1a729 — sección de información base ([[task-41]]), fix del motor (save() completo) y snackbar global — más cinco commits propios de la sesión.

## Deploy y seeds

Backup pg_dump (_backups/onigies_pre_geninfo_20260804_160902.dump), 3 migraciones (survey 0008, indicator 0008, ies 0012), seed_flow, load_sectors y load_questionnaire --sync-institutions (5 grupos generales, 62 instituciones re-guardadas). Hallazgo de runbook: load_sectors es prerrequisito de load_questionnaire y no estaba documentado — ya está en el skill deploy-api. Humo completo en verde, incluido el puente UNAM. Con esto corrió por primera vez load_questionnaire en producción ([[task-14]], criterio 1).

## Reparación de sent_at ([[task-59]], cerrada)

Dimensionamiento en producción: 62 paquetes bp, 36 reparables por FlowEvent, 1 sin evento (id=64, de prueba — null deliberado por decisión de Ricardo), 3 ya con fecha; gen sin envíos. Comando idempotente repair_sent_at (flow/, dry-run por defecto) aplicado y verificado. Test de regresión en flow/tests.py: el envío persiste sent_at en BD y el reenvío no lo pisa; se verificó que muerde revirtiendo temporalmente el fix.

## Endurecimiento ([[task-24]], cerrada; [[task-4]] criterio 1)

DEBUG=False vía .env (ya era env-driven), CORS de allow-all a allowlist env-driven (puente UNAM, Netlify, localhost dev), /static/ con re_path explícito como /files/ + collectstatic para que el admin sobreviva sin DEBUG, ALLOWED_HOSTS=apionigies.yeeko.org, SECURE_PROXY_SSL_HEADER, cookies Secure y HSTS de un año. Humo: 404 sin traza, preflight niega orígenes ajenos, headers verificados. Se registró Period en el admin de Django — no existía y bloqueaba fijar gen_submission_deadline, que sigue pendiente de Ricardo a mano.

## Skills ([[task-60]], cerrada)

flow, dashboard-collections y gen-general-info alineados con la sesión de generales; segunda ronda siguiendo create-skill añadió los campos faltantes de Status y corrigió una deriva real: el skill documentaba requires_comment, que no existe (es comment_type). deploy-api ganó el orden de seeds.

## Hallazgos que quedan fuera

- El default_server del nginx de Yeeko responde a Hosts arbitrarios con otra app Django del servidor corriendo DEBUG=True (fuga de URLconf; infraestructura multi-tenant de Yeeko, no de este API).
- El backup .env.bak_task24 y los dumps de _backups/ siguen en el servidor ([[task-4]], criterio 2).
