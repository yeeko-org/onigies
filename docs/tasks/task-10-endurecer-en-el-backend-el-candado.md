---
type: task
id: task-10
title: Endurecer en el backend el candado de periodo cerrado
state: open
date: 2026-08-03
owner: ai
parent: "[[task-1]]"
source: ["[[2026-07-03-auditoria-y-mejoras-del-flujo]]", "[[2026-07-28-reunion-flujo-bp-e-informacion-base]]"]
related: ["[[task-55]]"]
---

# Endurecer en el backend el candado de periodo cerrado

Follow-up que dejó abierto la sesión S4: `GoodPracticeViewSet.update` no valida periodo ni turno, a diferencia de `discard`/`reopen`, que sí. Hoy el candado de periodo vive solo en el frontend (`canEdit` exige `periodOpen`), así que una petición directa lo salta.

**Alcance ampliado (verificación del 2026-08-03).** El mismo agujero está en `FeatureGoodPracticeViewSet`, que es donde vive la justificación de la IES y la calificación de la revisora — o sea, el contenido que más importa proteger tras el cierre. Ambos viewsets están en `api/api/views/example/__init__.py` y ninguno declara `permission_classes` ni sobrescribe `update`; `GoodPracticeViewSet` lleva además `disable_protection = True`.

Lo que sí llegó con el despliegue del 29 de julio es el candado de *transiciones*: `Period.is_bp_submission_closed` se aplica en `GoodPracticePackage.validate_flow_transition` y en las acciones `discard` y `reopen`. Eso bloquea mover el estado del paquete, no editar el contenido de una práctica con un `PATCH` directo.

Los datos base del Survey tienen el mismo problema pero **no caben aquí**: requieren otro campo de periodo, porque `submission_deadline` es específico del envío de buenas prácticas. Eso es [[task-55]].

## Criterios de aceptación

- [ ] Una petición de actualización con el periodo cerrado responde 403
- [ ] La protección cubre tanto `GoodPracticeViewSet` como `FeatureGoodPracticeViewSet`
- [ ] Hay un test que lo cubre
