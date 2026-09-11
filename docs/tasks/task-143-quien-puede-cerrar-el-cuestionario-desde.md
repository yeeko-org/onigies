---
type: task
id: task-143
title: Quién puede cerrar el cuestionario desde la barra del dashboard
state: open
date: 2026-09-10
owner: ricardo
parent: "[[task-2]]"
source: ["[[2026-09-10-editor-por-bloques-cuestionario-abierto-y-retiro-del-seed]]"]
related: ["[[adr-0015]]"]
---

# Quién puede cerrar el cuestionario desde la barra del dashboard

La barra del interruptor y el PATCH de `questionnaire_settings` van con el permiso genérico de escritura en catálogos: cualquier usuario del dashboard con ese permiso puede cerrar el cuestionario. Como el cierre es de ida y con diálogo de confirmación, el daño de un cierre accidental es que Ricardo lo reabra en el admin. Decidir si se restringe a staff (una condición en `QuestionnaireGate` y un permiso en el viewset) o si conviene que Rubén mismo pueda cerrarlo cuando termine.


Antes de cerrar el cuestionario, quien lo cierre toma un dump de producción a `~/databases/` (compromiso de [[task-139]] y del adr-0015): con el seed retirado, ese respaldo es la única vía para restaurar una pregunta borrada.

## Criterios de aceptación

- [ ] Decisión registrada y, si se restringe, aplicada en backend y frontend
