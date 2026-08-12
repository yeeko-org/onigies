---
type: task
id: task-25
title: Borrar los respaldos temporales del servidor
state: open
date: 2026-08-03
owner: ricardo
parent: "[[task-100]]"
source: ["[[2026-07-29-commits-tematicos-y-deploy-flow]]"]
---

# Borrar los respaldos temporales del servidor

En `api/_backups/` del servidor quedaron el volcado previo al deploy y `files_stale_jul04`, la copia parcial de la carpeta de archivos anterior al cutover `/media/`→`/files/`. Se dejaron a propósito hasta confirmar operación estable; ya pasó más de un mes.

## Criterios de aceptación

- [ ] `api/_backups/` en el servidor está vacío o solo con lo que se decida conservar
