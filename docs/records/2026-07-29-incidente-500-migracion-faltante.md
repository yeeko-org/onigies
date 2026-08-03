---
type: record
id: 2026-07-29-incidente-500-migracion-faltante
title: Incidente post-deploy — 500 por migración separada de su cambio de modelo
date: 2026-07-29
related: ["[[2026-07-29-commits-tematicos-y-deploy-flow]]", "[[adr-0001]]"]
---

# Incidente post-deploy — 500 por migración separada de su cambio de modelo

> Inmutable. Este documento no se edita: registra algo que ya pasó. Si algo de aquí resultó estar mal, se escribe otro documento que lo corrija y se enlaza.

**Cuándo:** 2026-07-29, minutos después del deploy registrado en [[2026-07-29-commits-tematicos-y-deploy-flow]] (que cerró con "sin incidentes" — este documento lo corrige).
**Quiénes:** Ricardo (detectó el 500) + Claude (diagnóstico y fix).

## Qué pasó

`https://apionigies.yeeko.org/api/catalogs/all/` devolvía 500: `psycopg.errors.UndefinedColumn: column indicator_observable.reach_instances_question does not exist`. Todo endpoint que consultara `Observable` estaba caído.

## Causa raíz

- El campo `Observable.reach_instances_question` se agregó en `45e8635` (junio, "Commit previo a la verificación de Fable") **sin su migración**.
- La migración (`indicator/0005`) se generó semanas después y cayó en `9eadc9e` — el commit del seed del cuestionario, deliberadamente excluido de `production`.
- El server venía de `881f8ff` (anterior al campo): funcionaba. Al hacer pull a `78fde6b` llegó el código que consulta la columna, con la migración del otro lado del corte.
- Ni pytest local ni el smoke lo detectaron: el test DB local se construye con los archivos de migración presentes en disco (sin importar en qué commit viven), y el smoke solo pegó a `/api/` raíz, que no consulta `Observable`.

## Fix aplicado

`production` se fast-forwardeó hasta `9eadc9e` (= `main`, decisión de Ricardo: el código y esquema del seed entran, `load_questionnaire` sigue sin correrse) y en el server: pull + `migrate` (indicator 0005–0007, question 0002–0003) + `makemigrations --check` ("No changes detected") + `sudo kill -HUP`. `catalogs/all/` volvió a 200.

## Qué salió de aquí

- La lección: **un cambio de modelo y su migración viajan en el mismo commit**; el chequeo anti-drift debe correr sobre el rango a desplegar (`git diff <deployed>..<target> -- '*/models.py' '*/migrations/'`) y en el server (`makemigrations --check`) antes de recargar, y el smoke debe pegar a endpoints con modelos reales (`catalogs/all/`), no a la raíz.
- Skill nueva `.claude/skills/deploy-api/` con el runbook y ese checklist institucionalizado.
