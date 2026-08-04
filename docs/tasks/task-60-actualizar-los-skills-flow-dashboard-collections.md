---
type: task
id: task-60
title: Actualizar los skills flow, dashboard-collections y gen-general-info tras la sesión de generales
state: closed
date: 2026-08-04
owner: ai
source: ["[[2026-08-04-sesion-seccion-informacion-base]]"]
---

# Actualizar los skills flow, dashboard-collections y gen-general-info tras la sesión de generales

La sesión del 2026-08-03/04 dejó desactualizados tres skills en puntos concretos que hoy contradicen el código: dashboard-collections afirma que EditSimple «solo recibe v-model» y no emite eventos; flow no menciona `_save_status` ni las superficies gen; gen-general-info describe el modelo pero no la superficie construida. Sesión corta de mantenimiento documental.

## Criterios de aceptación

- [x] dashboard-collections documenta que un EditSimple puede emitir item-saved y PanelCommon lo reenvía (sincronización renglón↔detalle)
- [x] flow documenta el save() completo del motor (_save_status) y que gen ya corre en vivo con sus superficies
- [x] gen-general-info refleja las banderas nuevas de Sector, GeneralGroup.order, el candado de período y dónde vive la captura (componentes de survey/)
