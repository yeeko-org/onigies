---
type: task
id: task-55
title: Candado de periodo para la edición de los datos base del Survey
state: open
date: 2026-08-03
owner: ricardo
source: ["[[2026-07-28-reunion-flujo-bp-e-informacion-base]]"]
related: ["[[task-10]]", "[[adr-0007]]"]
---

# Candado de periodo para la edición de los datos base del Survey

En la reunión mencionó haber empezado los bloqueos de edición posterior de los datos base: `[22:10]` «ya empecé a hacer los bloqueos para que como que no se pudiera hacer la edición posterior de los datos base, eso es importante». La verificación del código muestra que **eso todavía no existe para los datos base**.

Lo que sí llegó con el despliegue del 29 de julio fue el candado de *envío de buenas prácticas*: `Period.submission_deadline` y `Period.is_bp_submission_closed` en `api/ies/models.py`, aplicados en `GoodPracticePackage.validate_flow_transition` (`api/example/models.py`) y en las acciones `discard` y `reopen` de `api/api/views/example/__init__.py`. Es otra cosa: bloquea transiciones de flujo del paquete de bp, no la edición de la información base.

**El hueco:** `SurveyViewSet` (`api/api/views/survey/__init__.py`) solo declara `IsInstitutionOwnerOrSuperuser` y acota el queryset por institución. No tiene ninguna noción de periodo, así que un `PATCH` sobre los datos base pasa siempre.

Se separa de [[task-10]] —que cubre el mismo agujero en los viewsets de buenas prácticas— porque aquí el candado **no puede reusar `submission_deadline`**: ese campo es específico del envío de bp y su fecha es distinta. Cerrar la edición de la información base requiere **otro campo de periodo** (una fecha de cierre de datos base, o un estado de periodo). Eso toca esquema: **la definición del campo es decisión de Ricardo antes de implementar nada.**

Es el respaldo técnico de [[adr-0007]]: si las IES pueden mover los datos base después de validados, cambian los denominadores de los indicadores.

## Criterios de aceptación

- [ ] Ricardo definió cómo se modela el cierre de la información base
- [ ] Una petición de actualización del Survey con la información base cerrada responde 403
- [ ] La revisora conserva la capacidad de corregir después del cierre, si así se definió
- [ ] Hay un test que lo cubre
