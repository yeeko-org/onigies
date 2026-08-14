---
type: decision
id: adr-0013
title: Los archivos suben a S3 como puente hasta el servidor de la UNAM
state: accepted
date: 2026-08-13
origin: ricardo
deliberation: dialogued
rationale: recorded
source: ["[[2026-08-12-migracion-de-archivos-a-s3]]"]
affects: ["api/core/settings/__init__.py", "api/flow/attachment_views.py", "api/flow/serializers.py", "api/flow/management/commands/migrate_files_to_s3.py", "nuxt/app/components/dashboard/flow/FlowAttachments.vue"]
related: ["[[adr-0010]]", "[[task-100]]"]
---

# Los archivos suben a S3 como puente hasta el servidor de la UNAM

## Contexto y planteamiento del problema

Los archivos subidos (adjuntos de flow, evidencias históricas, logos) vivían en el disco del EC2 (Yeeko) y Django los servía bajo `/files/` sin ningún control de acceso. El servidor definitivo de la UNAM llegará en ~2 meses ([[task-100]]), así que cualquier inversión aquí debe ser barata de deshacer. El patrón se recuperó de la migración equivalente en dev/ibero/ocsa (2026-07-21), que allá no quedó documentada — el porqué vivía solo en comentarios de código y mensajes de commit; esta vez sí queda registrado.

## Decisión

- **Switch global de storage por `USE_S3_FILES`** (default off): todo el media va a S3 al encender el flag; en local y con el flag apagado, disco como siempre. No per-field como ocsa: allá solo migraban los documentos pesados; aquí el media es prácticamente puro adjunto, y el switch global no toca modelos ni genera migraciones.
- **Bucket privado `onigies-v3-temporal`** (us-west-2, misma cuenta AWS que ocsa, credenciales IAM compartidas — se copiaron de un `.env` a otro dentro del servidor). Sin Intelligent-Tiering ni CloudFront: con horizonte de 2 meses no rinden.
- **Acceso por endpoint de descarga** (`/flow/<app>/<model>/<pk>/attachments/<id>/download/`): valida permisos con el gate existente de flow y responde 302 a una URL firmada efímera. Se eligió sobre las capability-URLs (firmadas directas en el serializer) porque concentra la lógica de permisos en un solo punto que revalida en cada descarga. Para el frontend autenticado existe `?redirect=false`, que devuelve la URL en JSON vía `$api`.
- **`Attachment.is_public` default `False`**, con semántica estricta: público = cualquier persona, anónimos incluidos (pensado para la futura plataforma pública). Un anónimo sobre un adjunto privado recibe 404, no 401, para no permitir enumerar ids.
- **Solo media**: los estáticos se quedan siempre en storage local.
- **S3 es puente, no destino**: al llegar el servidor UNAM los archivos regresan a disco; el comando `migrate_files_to_s3` es bidireccional (`--download`) por eso mismo, idempotente por tamaño, y nunca borra nada en ningún sentido.

## Hallazgo técnico que condiciona la implementación

En django-storages 1.14.6, `custom_domain` (que ocsa usaba para evitar el redirect 307 regional) anula `querystring_auth`: las URLs salen sin firmar — inservible con bucket privado. La firma correcta exige quitarlo y configurar `signature_version: s3v4` + `addressing_style: virtual`; sin ellas boto3 emite SigV2 (rechazada por buckets posteriores a 2020) contra el endpoint global. Verificado empíricamente con matriz de pruebas.

## Consecuencias

- La privacidad llega con el switch: `MEDIA_URL` absoluta apaga sola la ruta abierta `/files/` (guard en `core/urls.py`), y el bucket sin bucket policy pública solo responde a URLs firmadas.
- La región y el bucket son obligatorios con el flag encendido (`ImproperlyConfigured` si faltan) y las credenciales se pasan explícitas al backend, para no caer en silencio al instance profile del EC2.
- El disco del EC2 conserva los 817 archivos como respaldo hasta la mudanza.
- La implementación completa del flag `is_public` (UI, qué ContentTypes lo admiten) queda como task aparte no urgente.
