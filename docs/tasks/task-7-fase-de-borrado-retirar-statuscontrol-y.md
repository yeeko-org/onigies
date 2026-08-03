---
type: task
id: task-7
title: "Fase de borrado: retirar StatusControl y los modelos viejos"
state: open
date: 2026-08-03
owner: ai
parent: "[[task-1]]"
source: ["[[2026-06-05-diseno-del-motor-de-flujo]]"]
---

# Fase de borrado: retirar StatusControl y los modelos viejos

El §8 del diseño del motor, que quedó fuera de los dos deploys. Quitar `status_register`/`status_sending` de los seis modelos; borrar `ObservableComment`, `GroupComment`, `GroupAttachment`, `GeneralGroupComment`, `GeneralGroupAttachment`, `Evidence`, el `Comment` abstracto y los helpers de upload viejos; quitar `comments` (TextField) de los tres modelos de `example`; borrar `ies.StatusControl`, su admin, `InitStatus` y sus choices; simplificar `Institution.save()`; y cambiar el filtro `status_sending__is_final=False` por `status__role__isnull=False` en `api/api/views/example/__init__.py`.

Precondición: haber verificado los datos migrados en producción con `verify_flow_data`. Las migraciones las corre Ricardo.

## Criterios de aceptación

- [ ] `grep -r status_sending\|status_register api/` no devuelve nada
- [ ] `ies.StatusControl` y los modelos de comentarios/adjuntos viejos ya no existen
- [ ] Las migraciones de borrado corrieron en producción sin incidentes
