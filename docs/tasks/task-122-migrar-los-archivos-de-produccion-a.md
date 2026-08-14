---
type: task
id: task-122
title: Migrar los archivos de producción a S3 y desplegar el nuevo stack de descarga
state: closed
date: 2026-08-13
owner: ai
source: ["[[2026-08-12-migracion-de-archivos-a-s3]]"]
related: ["[[adr-0013]]", "[[task-7]]"]
---

# Migrar los archivos de producción a S3 y desplegar el nuevo stack de descarga

Ejecutar [[adr-0013]]: settings con `USE_S3_FILES`, endpoint de descarga con permisos y 302 firmado, `Attachment.is_public`, corte legacy nivel 2, comando bidireccional `migrate_files_to_s3`, y el deploy completo (copia de archivos, flip del flag, smokes). Creada y cerrada el mismo día: deploy nocturno del 2026-08-12 con 692/692 archivos subidos en 1m20s, verify por tamaño limpio, smokes en verde (URL firmada 200, `/files/` viejo 404, anónimo sobre privado 404), disco intacto como respaldo y 125 huérfanos informativos.

## Criterios de aceptación

- [x] Los 692 archivos referenciados en BD viven en el bucket y verify sale limpio
- [x] Las descargas privadas exigen permisos y las públicas funcionan para anónimos
- [x] La ruta abierta /files/ deja de responder en producción
- [x] El disco del EC2 queda intacto como respaldo
