---
type: task
id: task-112
title: "«Está presente»: la existencia de una población pasa a tri-estado"
state: open
date: 2026-08-11
owner: ai
parent: "[[task-41]]"
source: ["[[2026-08-11-reunion-con-ruben-sobre-la-informacion-base]]"]
related: ["[[task-56]]", "[[task-106]]", "[[adr-0008]]", "[[adr-0012]]"]
---

# «Está presente»: la existencia de una población pasa a tri-estado

Sustituye la casilla de la tabla de poblaciones por un campo de tres estados, para distinguir un «no» explícito de un renglón que nadie tocó. Hoy no se puede: la existencia de una población **es** la pertenencia al M2M `Survey.sectors`, y un M2M solo sabe de presente o ausente.

La decisión y su porqué están en [[adr-0012]]; esto es su implementación.

**Modelo.** `is_present` en `PopulationQuantity`, booleano que admite nulo. La fila se persiste **en cuanto hay respuesta, sí o no**, aunque no lleve ningún conteo — lo que modifica el punto 3 de [[adr-0008]].

**`Survey.sectors` se degrada a derivado:** pasa a ser una propiedad calculada sobre las filas con `is_present` verdadero. Hay que barrer sus usos, que son tres — el serializer de generales, el composable `useGeneralSurvey` del frontend y el cálculo del observable 1.7 por su ponderación de población.

**Interfaz.** El selector muestra solo «Sí» y «No». El nulo es el estado de no haber tocado la fila y **no tiene opción visible**: no se ofrece «no responder». El encabezado de la columna pasa a **«Está presente»**, sin signos de interrogación.

Ese encabezado cierra un hilo que quedaba abierto. Rubén objetó «se atiende» en la reunión del 11 de agosto porque muchas IES dirían que no atienden a familias o proveedores, cuando la relación no es de atención sino de trabajo colaborativo; propuso cubrir poblaciones «presentes física o virtualmente». «Está presente» recoge eso. Queda anotado también en [[task-88]], que había quedado acotada a `cp` justamente con el hilo de gen sin dueño.

Se toca con [[task-106]]: la validación de campos vacíos y este tri-estado hablan de lo mismo, porque el nulo es exactamente «sin responder».

**Urgencia:** ventana del miércoles y el jueves — la sección se hace visible el jueves 13.

## Criterios de aceptación

- [ ] `PopulationQuantity.is_present` existe, con su migración
- [ ] Una fila con respuesta y sin ningún conteo se persiste y vuelve igual al recargar
- [ ] `Survey.sectors` es derivado y sus tres usos quedaron barridos
- [ ] El selector ofrece solo «Sí» y «No»; el estado sin tocar no tiene opción visible
- [ ] El encabezado de la columna dice «Está presente», sin signos de interrogación
