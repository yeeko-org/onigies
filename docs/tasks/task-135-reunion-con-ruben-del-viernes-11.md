---
type: task
id: task-135
title: "Reunión con Rubén del viernes 11 de septiembre: reach obligatorio, simulación de puntajes, el 1.12 y la ponderación tentativa"
state: open
date: 2026-09-07
owner: ricardo
parent: "[[task-5]]"
source: ["[[2026-09-07-rediseno-edicion-observables-pesos-y-nomenclatura]]"]
---

# Reunión con Rubén del viernes 11 de septiembre: reach obligatorio, simulación de puntajes, el 1.12 y la ponderación tentativa

Puntos a llevar:

- ¿Transversalidad sectorial es obligatoria? La tienen 35 de 41 observables; los seis sin ella son 1.1, 1.12, 1.14, 1.15, 4.1 y 4.7. Hoy `required` es falso.
- El observable 1.12 (planes de estudio) tiene fila de transversalidad orgánica porque el tipo es requerido, pero no tiene esa pregunta: ¿es excepción legítima (y «requerido» admite excepciones) o falta la pregunta en el instrumento?
- Ponderación tentativa acordada por WhatsApp el 7 de septiembre: armonización e institucionalización 5, sectorial 2.5, orgánica 2.5, sobre 10; Rubén quiere simular con Ricardo qué puntaje saca una IES con una u otra forma de calcular antes de fijarla. Los pesos siguen nulos ([[task-15]]).
- Rubén entra de lleno a ONIGIES después del miércoles 9.

## Criterios de aceptación

- [ ] Respuesta de Rubén sobre reach obligatorio registrada y, si aplica, `required` actualizado en el seed
- [ ] Decisión sobre el 1.12 registrada
- [ ] Simulación de puntajes acordada o agendada

## Antes de la reunión (10 de septiembre de 2026)

Cambia lo que se lleva: la ponderación tentativa 5 / 2.5 / 2.5 ya está en la base como default de los tipos, y planes, especial y población tienen default nulo ([[adr-0015]]); el default se hereda solo en observables con exactamente el trío, así que el 1.12 y los seis sin sectorial piden peso propio y se ven con aviso. La BQuestion faltante del 1.12 y cualquier sectorial nueva las agrega Rubén mismo desde el dashboard cuando se despliegue ([[task-139]]); ya no se editan en el seed. Si Rubén decide que sectorial es obligatoria, `required` de `reach` se cambia en `initial_data.py` y en la base a mano (el seed de tipos solo crea).
