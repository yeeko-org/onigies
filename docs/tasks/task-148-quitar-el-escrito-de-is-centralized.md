---
type: task
id: task-148
title: Quitar el escrito de is_centralized sobre encuestas existentes en _preload_centralized
state: open
date: 2026-09-10
owner: ricardo
parent: "[[task-101]]"
source: ["[[2026-09-10-deploy-del-editor-por-bloques-y-ultima-siembra]]"]
related: ["[[task-139]]"]
---

# Quitar el escrito de is_centralized sobre encuestas existentes en _preload_centralized

`_preload_centralized` (`api/ies/models.py:90`) corre en cada `Institution.save()` y, cuando la respuesta general `is_centralized` de una encuesta existente está en nulo, la rellena con el valor del catálogo de instituciones. Nunca pisa una respuesta capturada, pero sí escribe sobre una encuesta que ya está en manos de la IES: si dejó el campo vacío a propósito, guardar la institución desde el dashboard —o correr `load_questionnaire --sync-institutions`— lo llena. Por eso el deploy del 10 de septiembre corrió sin `--sync-institutions`.

Postura de Ricardo en esa sesión:

> No deberíamos modificar is_centralized en ningún sentido, ya hay IES que han respondido.

Queda por decidir qué pasa con las encuestas nuevas: hoy la precarga al crear la encuesta es el único momento en que el valor del catálogo llega a la respuesta, y el docstring del método la presenta como su propósito («Solo al crear el survey o mientras nadie haya contestado»). La opción mínima es dejar la precarga solo en `survey_created` y quitar la rama «mientras nadie haya contestado»; la máxima es no precargar nunca y que la IES lo conteste siempre.

## Criterios de aceptación

- [ ] Decidido si la precarga se conserva solo al crear la encuesta o se retira por completo
- [ ] Guardar una institución ya no escribe `is_centralized` en ninguna encuesta existente
- [ ] `load_questionnaire --sync-institutions` deja de tocar respuestas generales
