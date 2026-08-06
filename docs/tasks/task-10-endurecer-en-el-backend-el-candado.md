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

## Alcance ampliado (2026-08-06, revisión con Fernanda)

La revisión del 6 de agosto ([[2026-08-06-temas-reunion-fer]], §15 `[49:43]`–`[58:41]`) expuso el agujero desde el lado de la usuaria: pasada la fecha límite el sistema bloquea algunas acciones —enviar, cambiar de estatus— pero **permite seguir agregando contenido nuevo**. Comportamiento inconsistente: la IES no sabe si el periodo está cerrado o no, porque el sistema le contesta las dos cosas.

Tres ampliaciones al alcance original:

1. **No solo `update`.** El síntoma que apareció en vivo es el `create`: se pueden agregar buenas prácticas con el periodo cerrado. El candado tiene que cubrir `create`, `update` y `destroy`.
2. **Varios lugares, no dos viewsets.** Ricardo cree que hay más superficies donde falta el bloqueo, más allá de `GoodPracticeViewSet` y `FeatureGoodPracticeViewSet`. Hace falta una revisión general de todas las superficies de escritura que dependen del periodo, no un parche en las dos ya identificadas.
3. **Borradores post-cierre: imposibles en absoluto.** La reunión dejó abierta la pregunta de si la IES puede seguir generando borradores tras el cierre. **Respuesta de Ricardo (2026-08-06): no debería poder en absoluto.** No es una verificación pendiente ni una zona gris — es la regla, y el candado debe hacerla cumplir.

El bloqueo tiene que ser total **y claro**: el aviso en la interfaz de que el periodo cerró es [[task-74]]. La contraparte —qué sí puede hacer la revisora después de la fecha límite— está sin definir y es [[task-76]]; las tres tienen que quedar coherentes entre sí.

## Criterios de aceptación

- [ ] Una petición de actualización con el periodo cerrado responde 403
- [ ] La protección cubre tanto `GoodPracticeViewSet` como `FeatureGoodPracticeViewSet`
- [ ] La protección cubre `create`, `update` y `destroy`, no solo la actualización
- [ ] Se revisaron todas las superficies de escritura que dependen del periodo, no solo las dos ya identificadas
- [ ] Con el periodo cerrado la IES no puede crear borradores nuevos por ninguna vía
- [ ] Hay un test que lo cubre
