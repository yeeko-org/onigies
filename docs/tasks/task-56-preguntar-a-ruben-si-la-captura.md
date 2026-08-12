---
type: task
id: task-56
title: Preguntar a Rubén si la captura de poblaciones requiere el estado «sin dato» (no_apply)
state: open
date: 2026-08-04
owner: ricardo
parent: "[[task-41]]"
---

# Preguntar a Rubén si la captura de poblaciones requiere el estado «sin dato» (no_apply)

Surgió al diseñar la tabla única de poblaciones (existe / hombres / mujeres). El modelo PopulationQuantity tiene no_apply, pero Ricardo está casi seguro de que es redundante con la columna «existe». Importa porque para el observable 1.7 «cero», «sin dato» y «no existe» son tres cosas distintas en los denominadores. La captura de hoy se construye SIN considerar no_apply.

Segunda pregunta, agregada al afinar el grupo de autoridades: ¿existe alguna IES donde falte alguno de los 3 cuerpos de autoridad (máximo cuerpo colegiado, titulares de instancias académicas, titulares de instancias administrativas)? La tabla de autoridades se construyó con las 3 filas fijas y sin escape; si la excepción existe en la realidad, el mecanismo acordado es un checkbox discreto «No aplica» por fila persistido en el `no_apply` que el modelo ya trae (opt-out para excepción rara, a diferencia del opt-in «existe» de poblaciones) — entra después con costo mínimo, sin migración.

## Autoridades: resuelto por decisión de Ricardo (2026-08-11)

La segunda pregunta ya no espera a nadie. En la reunión del 11 de agosto, `[35:12]`–`[39:00]` ([[2026-08-11-reunion-con-ruben-sobre-la-informacion-base]]), se exploró el terreno: la persona titular existe siempre, «de cajón»; del máximo cuerpo colegiado en instituciones privadas Rubén no estaba seguro; los titulares de instancias académicas existen porque toda instancia académica tiene responsable, y de las administrativas no lo tenía claro.

**Decisión unilateral de Ricardo, no acuerdo con Rubén, y sin nada pendiente de confirmar:** se asume que cualquiera de las tres puede faltar y se pone la opción **«No aplica» en cada una de las tres filas**. No se va a preguntar a Rubén si el cuerpo colegiado existe en las privadas; el opt-out cubre el caso sin necesidad de saberlo.

Es el mecanismo que esta task ya describía —casilla discreta por fila sobre el `no_apply` que el modelo ya trae, sin migración—, así que lo que cambia es solo que deja de ser condicional.

Un supuesto que hay que construir antes: Ricardo se lo explicó a Rubén como «para que se pueda marcar y así pasar la validación, que hoy no permite guardar con campos vacíos». **Esa validación no existe en el código.** Sin ella, «No aplica» no desbloquea nada porque nada estaba bloqueado — es [[task-106]].

**La primera pregunta sigue abierta.** El «sin dato» en poblaciones no se respondió en esos términos; reapareció por otra puerta como el selector de tres estados de la propia captura, que Rubén y Ricardo pospusieron explícitamente y que se está resolviendo en diálogo.

## Avance (2026-08-12, sesión orquestada)

El AC del «No aplica» de autoridades quedó implementado vía [[task-106]] en `943c7ac`: checkbox por fila al final, después del Total (posición decidida por el coordinador con delegación de Ricardo), persistido en `no_apply`, que limpia y deshabilita los conteos de la fila y la exime en la validación — que ahora sí existe y sí bloquea. El primer nivel del «sin dato» de poblaciones quedó cubierto por el tri-estado de [[task-112]]; el segundo nivel («no» vs «no sé») sigue como lo dejó [[adr-0012]]: no resuelto y aceptado. En el cierre de la sesión Ricardo descartó explícitamente agregar `no_data` a [[task-117]] por ahora — si madura, será decisión metodológica aparte.

## Criterios de aceptación

- [ ] Rubén respondió si «existe pero sin dato» debe ser capturable en poblaciones, distinto de no marcar el sector
- [x] Resuelto si algún cuerpo de autoridad puede no existir: se asume que sí, sin preguntar
- [x] Las tres filas de autoridades tienen la opción «No aplica», persistida en `no_apply`
- [ ] Con la respuesta de poblaciones: se agenda el uso de `no_apply` donde aplique, o se evalúa retirar el campo del modelo
