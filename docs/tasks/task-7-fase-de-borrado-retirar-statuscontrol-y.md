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

## Duda abierta sobre los modelos de adjuntos (2026-08-06)

La revisión con Fernanda ([[2026-08-06-temas-reunion-fer]], §9) reactivó el requisito de adjuntar evidencia probatoria en las preguntas base e iniciales — acuerdo con Rubí, hoy [[task-68]]. Eso choca de frente con el borrado planeado de `GroupAttachment`, `GeneralGroupAttachment` y `Evidence`.

**Anotación de Ricardo (2026-08-06):** revisarlo en su momento. No tiene claro **por qué** se decidió quitar `GroupAttachment` y `Evidence` —¿era para adjuntos generales?— y sospecha que **la razón de ese cambio no quedó registrada** en ningún lado. Antes de correr las migraciones de borrado hay que reconstruir esa razón o decidirla de nuevo: si la evidencia nueva se construye sobre el mecanismo de `flow` (como ya ocurre con los archivos de las buenas prácticas), el borrado sigue en pie; si no, hay que acotarlo.

## Criterios de aceptación

- [ ] `grep -r status_sending\|status_register api/` no devuelve nada
- [ ] `ies.StatusControl` y los modelos de comentarios/adjuntos viejos ya no existen
- [ ] Las migraciones de borrado corrieron en producción sin incidentes
- [ ] La razón para borrar `GroupAttachment` y `Evidence` quedó reconstruida o decidida de nuevo, y es compatible con [[task-68]]
