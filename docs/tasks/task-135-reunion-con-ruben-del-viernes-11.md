---
type: task
id: task-135
title: "Reunión con Rubén del viernes 11 de septiembre: reach obligatorio, simulación de puntajes, el 1.12 y la ponderación tentativa"
state: closed
date: 2026-09-07
owner: ricardo
parent: "[[task-5]]"
source: ["[[2026-09-07-rediseno-edicion-observables-pesos-y-nomenclatura]]"]
related: ["[[2026-09-04-reunion-con-ruben]]"]
---

# Reunión con Rubén del viernes 11 de septiembre: reach obligatorio, simulación de puntajes, el 1.12 y la ponderación tentativa

Puntos a llevar:

- ¿Transversalidad sectorial es obligatoria? La tienen 35 de 41 observables; los seis sin ella son 1.1, 1.12, 1.14, 1.15, 4.1 y 4.7. Hoy `required` es falso.
- El observable 1.12 (planes de estudio) tiene fila de transversalidad orgánica porque el tipo es requerido, pero no tiene esa pregunta: ¿es excepción legítima (y «requerido» admite excepciones) o falta la pregunta en el instrumento?
- Ponderación tentativa acordada por WhatsApp el 7 de septiembre: armonización e institucionalización 5, sectorial 2.5, orgánica 2.5, sobre 10; Rubén quiere simular con Ricardo qué puntaje saca una IES con una u otra forma de calcular antes de fijarla. Los pesos siguen nulos ([[task-15]]).
- Rubén entra de lleno a ONIGIES después del miércoles 9.

## Acuerdos de la reunión con Rubén (2026-09-04)

**Esta reunión es la que agendó la del 11 de septiembre.** `[37:07]` Rubén: «¿nos podríamos reunir, si quieres, jueves o viernes de la próxima semana, o miércoles? El martes y miércoles vamos a estar a full con lo de la clausura del diplomado»; `[37:27]` «el jueves ya voy a estar libre».

**Y le puso el tema de ponderación que esta task lleva.** Ricardo, `[53:32]`: «Eso no tenemos que resolverlo ahorita, pero lo ideal es que destinemos un día para conversar eso». La simulación de puntajes que Rubén pidió por WhatsApp el 7 de septiembre es el desarrollo de ese acuerdo, no algo distinto.

**Qué esperaba Rubén tener listo para esa reunión:** la corrección del cuestionario. `[38:32]` «es posible que el jueves que nos veamos, si no alcanzo, no tenga listo eso; pero podemos ver lo que tú avanzaste, y yo le daría prioridad a más tardar el viernes o el lunes, para que ya esté listo el sondeo».

## Criterios de aceptación

- [ ] Respuesta de Rubén sobre reach obligatorio registrada y, si aplica, `required` actualizado en el seed
- [ ] Decisión sobre el 1.12 registrada
- [ ] Simulación de puntajes acordada o agendada

## Antes de la reunión (10 de septiembre de 2026)

Cambia lo que se lleva: la ponderación tentativa 5 / 2.5 / 2.5 ya está en la base como default de los tipos, y planes, especial y población tienen default nulo ([[adr-0015]]); el default se hereda solo en observables con exactamente el trío, así que el 1.12 y los seis sin sectorial piden peso propio y se ven con aviso. La BQuestion faltante del 1.12 y cualquier sectorial nueva las agrega Rubén mismo desde el dashboard cuando se despliegue ([[task-139]]); ya no se editan en el seed. Si Rubén decide que sectorial es obligatoria, `required` de `reach` se cambia en `initial_data.py` y en la base a mano (el seed de tipos solo crea).

## Cierre (2026-09-22)

La reunión del 11 de septiembre no ocurrió (Ricardo, 2026-09-22). Los tres puntos pasan íntegros a [[task-165]], la agenda para la reunión del 23 de septiembre a las 11, junto con lo nuevo del análisis de «no aplica» ([[adr-0017]]). Los criterios quedan sin marcar a propósito: no se cumplieron aquí.
