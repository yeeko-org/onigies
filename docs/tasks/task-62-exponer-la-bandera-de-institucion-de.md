---
type: task
id: task-62
title: Exponer la bandera de institución de prueba en la edición del dashboard
state: open
date: 2026-08-06
owner: ai
source: ["[[2026-08-06-temas-reunion-fer]]"]
related: ["[[task-53]]", "[[adr-0009]]"]
---

# Exponer la bandera de institución de prueba en la edición del dashboard

§2 y §3 de la reunión con Fernanda, `[01:54]`–`[03:43]` y `[03:43]`. Fernanda quiso marcar como institución de prueba a la IES que acababa de crear («Fer» / «FP») y no encontró dónde: en la edición de una institución desde el dashboard no existe la casilla. Ricardo la marcó al vuelo desde el admin de Django durante la llamada y anotó que hay que exponerla también en la edición normal.

El modelo ya existe y está decidido: `Institution.is_test` en `api/ies/models.py`, definido en [[adr-0009]] y construido en [[task-53]] (cerrada). El hueco es de superficie: en `api/ies/catalog_schema.py` la bandera solo aparece como `ComponentFilter` con `TripleBooleanFilter` para filtrar el listado, no como campo editable; `nuxt/app/components/dashboard/ies/institution/InstitutionEdit.vue` no la menciona. El procedimiento para tocar el esquema está en el skill `manage-collections`.

No cuelga de [[task-53]] porque esa ya está cerrada; es un hueco de implementación detectado después, no una reapertura.

## Criterios de aceptación

- [ ] La edición de una institución desde el dashboard permite marcarla y desmarcarla como institución de prueba
- [ ] El cambio se refleja sin pasar por el admin de Django
