---
type: task
id: task-95
title: Sacar el frontend de onigies por completo del servidor EC2 de yeeko
state: open
date: 2026-08-08
owner: ricardo
---

# Sacar el frontend de onigies por completo del servidor EC2 de yeeko

La app `onigies` sigue apareciendo en el dump de resurrect de pm2 (`~/.pm2/dump.pm2`) del EC2 de yeeko, pero no está corriendo. La decisión, tomada el 2026-08-08 durante una sesión de limpieza de pm2 en ocsa-nuxt, es retirarla por completo del servidor: su entrada en pm2, sus archivos y cualquier configuración de nginx asociada. Mientras tanto, no correr `pm2 save` a la ligera en ese servidor, porque borraría otras apps apagadas a propósito (backup-ocsa).

## Criterios de aceptación

- [ ] La entrada de onigies ya no existe en pm2 ni en el dump de resurrect
- [ ] Los archivos del front fueron retirados del servidor
- [ ] Nginx no referencia a onigies
