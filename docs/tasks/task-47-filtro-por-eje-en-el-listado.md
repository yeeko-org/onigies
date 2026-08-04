---
type: task
id: task-47
title: Filtro por eje en el listado de buenas prácticas
state: open
date: 2026-08-03
owner: ai
parent: "[[task-6]]"
source: ["[[2026-07-28-reunion-flujo-bp-e-informacion-base]]"]
---

# Filtro por eje en el listado de buenas prácticas

Anotado por él mismo al final de la reunión, pensando en cuando estén cargadas todas las prácticas: `[40:52]` «De una vez voy a anotar que cuando se muestren todas las buenas prácticas, bueno, una falta del filtro por eje».

Estado actual: en `api/example/catalog_schema.py`, `GoodPracticeSchema.all_filters` solo declara `FilterRef("institutions")`. El grupo de filtro por ejes ya existe y se usa en otras superficies (`DisplayGroup` con `filter_group_name="axes"`), así que basta agregarlo a la lista. El procedimiento está en el skill `manage-collections`.

## Criterios de aceptación

- [ ] La barra de filtros del listado de buenas prácticas incluye el eje
- [ ] Filtrar por eje devuelve solo las prácticas de ese eje
