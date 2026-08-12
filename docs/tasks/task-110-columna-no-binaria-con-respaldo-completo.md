---
type: task
id: task-110
title: Columna no binaria con respaldo completo, y su pregunta previa
state: closed
date: 2026-08-11
owner: ai
parent: "[[task-41]]"
source: ["[[2026-08-11-reunion-con-ruben-sobre-la-informacion-base]]"]
related: ["[[adr-0004]]", "[[adr-0008]]"]
---

# Columna no binaria con respaldo completo, y su pregunta previa

Rubén propuso en la reunión del 11 de agosto agregar una columna «no binaria» junto a mujeres y hombres, señalando que ya hay instituciones —la UNAM entre ellas— con personas no binarias formalmente registradas. Las tres columnas existen para producir estadísticas de distribución por género.

La columna ya está pintada en el frontend, pero **el dato se pierde al guardar**: no existe en el modelo, no viaja en el payload y no entra en el total de la fila.

**Backend.** Migración que agrega `number_non_binary` a `PopulationQuantity`, entero que admite nulo, igual que los otros dos conteos.

**La pregunta previa es una sola.** Decidido el 11 de agosto tras diálogo: «¿su institución registra o mide población no binaria?» —la redacción está por pulir— vive en `Survey.measures_non_binary`, booleano que admite nulo, y se captura como GeneralQuestion de tipo booleano del grupo poblaciones ([[task-107]]).

Una, no dos, y la razón importa: **es una capacidad de medición de la institución, no una propiedad de cada tabla**. Dos preguntas independientes abrirían el estado absurdo de una institución que mide población no binaria en poblaciones y no en autoridades.

**La columna aparece en las dos tablas**, poblaciones y autoridades, habilitada por ese único flag. Rubén había dicho que en autoridades sería de facto un acto político —«nadie va a poner que tiene un rector no binario»—, pero aceptó incluirla si no cuesta tiempo extra, porque la estructura de medición no debe constreñir la posibilidad aunque en la práctica no ocurra.

**Frontend.** El conteo entra al constructor del payload en `nuxt/app/composables/useGeneralSurvey.js` y al total de la fila. De paso se corrigen dos defectos que la celda nueva trajo consigo: su rótulo accesible está copiado del de «Hombres», y las tres celdas de conteo mezclan dos formas distintas de declarar que la entrada es numérica.

**Ojo con [[adr-0004]]:** el cálculo del observable 1.7 asume composición binaria. Que exista un tercer conteo no dice cómo se puntúa — eso es [[task-111]], y sin esa definición el dato se captura pero no se mide.

## Cierre (2026-08-12, sesión orquestada)

Todo entregado en el commit `943c7ac`, verificado con smoke de navegador y e2e (`eb2ecc1`). Decisiones del cierre: rótulo de columna **«No binarie»**; la columna se **oculta** (no se deshabilita) cuando el flag no está activo; la persona titular gana tercera opción «No binaria» solo con el flag activo; la pregunta previa nació directamente como `GeneralQuestion` porque [[task-107]] se adelantó a la misma noche. Redacción final (dialogada, Rubén la revisará): «En sus registros de sexo y género, ¿su institución contempla la categoría no binaria?», con hint sobre el efecto de responder Sí. Regla adicional de Ricardo: el toggle Sí→No limpia los conteos no binarios ya capturados, en front y back. El conteo es obligatorio en filas presentes cuando el flag está activo (ratificado tras revisión). La puntuación del observable 1.7 sigue siendo [[task-111]].

## Criterios de aceptación

- [x] `PopulationQuantity` tiene `number_non_binary` y su migración
- [x] `Survey.measures_non_binary` existe y se captura como pregunta booleana del grupo poblaciones
- [x] La columna aparece en poblaciones y en autoridades, habilitada por ese único flag
- [x] El conteo se guarda y se suma al total de la fila
- [x] Cada celda de conteo tiene su propio rótulo accesible y un solo criterio de tipo de entrada
