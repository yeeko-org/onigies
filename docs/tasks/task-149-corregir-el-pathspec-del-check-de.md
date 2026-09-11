---
type: task
id: task-149
title: Corregir el pathspec del check de deriva de migraciones en el skill deploy-api
state: open
date: 2026-09-10
owner: ricardo
parent: "[[task-4]]"
source: ["[[2026-09-10-deploy-del-editor-por-bloques-y-ultima-siembra]]"]
---

# Corregir el pathspec del check de deriva de migraciones en el skill deploy-api

El checklist previo al deploy en `.claude/skills/deploy-api/SKILL.md` prescribe `git diff --stat <deployed-ref>..<target-ref> -- '*/models.py' '*/migrations/'`. Con la diagonal final el pathspec no empata ningún archivo: corrido sobre el rango del deploy del 10 de septiembre listó los dos `models.py` cambiados y ninguna de las siete migraciones, que es exactamente la salida que el propio checklist define como «stop-the-line». La forma correcta es `'*/migrations/*'`, que en ese rango da 9 archivos.

Es edición a un skill del proyecto y Ricardo no la decidió en la sesión:

> De la propuesta, no puedo decidir ahora

Mientras tanto, quien corra el check debe usar `'*/migrations/*'` a mano.

## Criterios de aceptación

- [ ] El skill prescribe `'*/migrations/*'` y explica en una línea por qué la diagonal final no sirve
