---
type: task
id: task-78
title: Etiqueta de institución de prueba en los headers
state: open
date: 2026-08-06
owner: ai
source: ["[[2026-08-06-temas-reunion-fer]]"]
related: ["[[adr-0009]]", "[[task-62]]"]
---

# Etiqueta de institución de prueba en los headers

§12 de la reunión con Fernanda, `[29:43]`–`[34:37]`. Hoy el header de un envío de buenas prácticas muestra solo siglas y año; nada indica que la institución sea de prueba, y en un listado mezclado eso desorienta a la revisora. Ricardo pidió poner la etiqueta «IES test» como **icono identificador** —ya existe uno, tipo frasco de laboratorio— y usarlo también en los headers de las instituciones que sean de prueba.

**Sin restricción de visibilidad** (decisión de Ricardo, 2026-08-06): da igual quién lo vea, incluida la propia IES de prueba.

El dato ya viaja al frontend gratis, porque los serializers de `Institution` usan `fields='__all__'` — ver [[adr-0009]]. Superficies: `nuxt/app/components/dashboard/example/good_practice_package/GoodPracticePackageHeader.vue`, `nuxt/app/components/dashboard/example/good_practice/GoodPracticeHeader.vue` y `nuxt/app/components/dashboard/ies/institution/InstitutionHeader.vue`. La casilla para marcarla es [[task-62]].

## Criterios de aceptación

- [ ] El header de un envío de una institución de prueba muestra el icono identificador
- [ ] El header de una institución de prueba muestra el mismo icono
- [ ] El icono es el que ya existe, no uno nuevo
