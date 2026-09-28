---
type: task
id: task-188
title: Decidir si buenas prácticas y los valores de eje merecen el mismo PROTECT hacia el instrumento
state: open
date: 2026-09-28
owner: ricardo
related: ["[[task-178]]"]
---

# Decidir si buenas prácticas y los valores de eje merecen el mismo PROTECT hacia el instrumento

Hallazgo del crítico de la sesión del 2026-09-28, fuera de lo decidido en [[task-178]] (que se enmarcó en el cuestionario principal). Siguen en `on_delete=CASCADE` hacia el instrumento tres FKs de datos que las IES o el cálculo producen: `GoodPractice.axis` y `GoodPractice.component` en `api/example/models.py` (buenas prácticas capturadas por las IES; borrar un eje o componente las arrastra), y `AxisValue.axis` y `ComponentValue.component` en `api/survey/models.py` (los valores calculados por encuesta). La exposición real es limitada: el DELETE del dashboard devuelve 400 antes de borrar si hay dependientes, y Axis/Component no tienen `NoDeleteMixin` pero sí pasan por ese reporte; queda `confirm-delete` por API directa y el ORM. Con los `PROTECT` de hoy, borrar un eje ya falla por los `ObservableResponse` de sus observables, así que en la práctica el eje está protegido por cascada; el caso descubierto es un eje o componente sin observables pero con buenas prácticas.

## Criterios de aceptación

- [ ] Ricardo decide si `GoodPractice.axis/.component` pasan a PROTECT
- [ ] Ricardo decide si `AxisValue.axis` y `ComponentValue.component` pasan a PROTECT o se quedan en CASCADE por ser valores recalculables
- [ ] Si algo cambia: migración sin efecto en SQL y test junto a `InstrumentProtectionTests`
