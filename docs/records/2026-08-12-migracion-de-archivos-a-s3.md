---
type: record
id: 2026-08-12-migracion-de-archivos-a-s3
date: 2026-08-13
---

# Migración de archivos a S3: planeación, implementación y deploy

Sesión duo (coordinador + ejecutores Opus/Sonnet) que llevó los archivos subidos de producción del disco del EC2 a un bucket privado de S3, el mismo día en que se planeó.

## Planeación

Ricardo pidió recuperar el patrón de la migración equivalente en dev/ibero/ocsa (2026-07-21). Un ejecutor la analizó por ingeniería inversa: switch por flag `USE_S3_FILES`, `upload_to` intacto con el prefijo en `location` (cero data migration), comando idempotente en fases dry-run → subida → verify que copia antes de encender el flag, nada se borra del disco. Otro ejecutor confirmó que no existía ADR ni task sobre almacenamiento de archivos (solo el runbook del skill deployment), y un tercero levantó la foto local: config S3 dormida en settings, código limpio (todo por la API de storage, cero usos de `.path`).

## Decisiones de Ricardo

Quedaron registradas en [[adr-0013]]: switch global (no per-field como ocsa), bucket privado `onigies-v3-temporal` con credenciales IAM compartidas con ocsa, solo media, endpoint de descarga con permisos y 302 firmado, `is_public` con semántica «cualquier persona, anónimos incluidos», S3 como puente hasta el servidor UNAM. Además aprobó el corte legacy nivel 2 ([[task-7]]): stack API de `Evidence` y modelos huérfanos `GroupAttachment`/`GeneralGroupAttachment`.

## Revisión crítica

Un agente crítico con acceso a la transcripción encontró dos bloqueadores confirmados: (1) `custom_domain` hace que django-storages emita URLs sin firmar — fatal con bucket privado; la firma correcta exigió `signature_version: s3v4` + `addressing_style: virtual` (verificado por matriz de pruebas); (2) el chip de descarga era un `href` plano sin header `Authorization`, así que toda descarga privada daba 401 — se resolvió con la opción (a): el endpoint gana `?redirect=false` (JSON con la URL firmada) y `FlowAttachments.vue` lo llama vía `$api`. También se corrigió la enumeración anónima (404 en vez de 401 sobre privados), la región dejó de tener default silencioso (falla ruidosa si falta) y las credenciales se pasan explícitas para no caer al instance profile del EC2.

## Deploy (2026-08-12, noche)

Commit `b45afe1` en main, fast-forward a production. Secuencia continua de ~8 minutos: respaldo de BD (914K), migraciones flow/0009 + answer/0004 + survey/0010 limpias, credenciales copiadas de ocsa a onigies dentro del servidor (nunca pasaron por la conversación), dry-run 692 archivos en BD todos en disco (+ 125 huérfanos informativos = los 817 del respaldo matutino), subida real 692/692 sin fallos en 1m20s, flag encendido con HUP, verify por tamaño limpio. Smokes: catálogos 200, URL firmada 200, `/files/` viejo 404, anónimo sobre privado 404. El disco queda intacto como respaldo hasta la mudanza a la UNAM. Suite local: 94 tests en verde.

## Propuestas pendientes sin decisión

- Fix de una sola query en `verify_flow_data.count_evidence_mirrors` (hoy hace N+1, y la compuerta imprimirá «REVISAR» permanentemente cuando alguien borre legítimamente un adjunto migrado).
- Renombrar a inglés los tests en español que quedan en `email_send/tests.py`, `ies/tests_recovery.py` y `survey/tests.py` (los de `flow/tests/test_attachments.py` ya se renombraron en esta sesión).
