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

## Construido, y por qué no se cierra todavía (2026-08-11)

La casilla ya existe: el trabajo sin commitear de Ricardo la agregó a la edición de institución del dashboard, y el campo es escribible sin pasar por el admin porque el serializer de institución expone todos los campos y no lo marca de solo lectura. Los dos criterios originales están cumplidos ([[2026-08-11-auditoria-del-arbol-de-trabajo-y-reorganizacion]]).

Lo que la mantiene abierta es el lenguaje. La convención del repositorio, ya anotada en el `CLAUDE.md` raíz, es **«De prueba», nunca «test»**, para instituciones de prueba y toda etiqueta relacionada. Hoy conviven dos infracciones, ambas del mismo trabajo sin commitear: la casilla nueva dice «¿Es para tests internos?» y el filtro del esquema de catálogo del API pasó de «De prueba» a «Es test» — este último, en dirección contraria a la convención.

El error al guardar desde el dashboard de institución que se le había anotado aquí el 11 de agosto **se confirmó como el mismo bug del logo** y vive completo en [[task-104]], con su diagnóstico y su cura. Aquí no queda nada de eso.

## Criterios de aceptación

- [x] La edición de una institución desde el dashboard permite marcarla y desmarcarla como institución de prueba
- [x] El cambio se refleja sin pasar por el admin de Django
- [ ] Ninguna etiqueta de la interfaz ni del esquema de catálogo dice «test»: la casilla y el filtro usan «De prueba»
