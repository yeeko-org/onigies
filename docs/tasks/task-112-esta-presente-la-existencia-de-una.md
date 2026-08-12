---
type: task
id: task-112
title: "«Está presente»: la existencia de una población pasa a tri-estado"
state: closed
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

## Cierre (2026-08-12, sesión orquestada)

Entregado en `943c7ac`, con el criterio verificatorio de [[adr-0012]] probado por sonda y por smoke: una fila marcada «No» sin conteos sobrevive al guardado y vuelve como «No». Decisiones del cierre: el M2M se renombró a **`sectors_legacy` con miras a borrarlo pronto** (Ricardo: que no haya dos fuentes de verdad; el borrado quedó en [[task-118]]) y la propiedad derivada tomó el nombre `sectors`; el M2M quedó fuera del API tras la revisión crítica. Alcance del tri-estado: las 12 filas de poblaciones incluidos los 2 extras; autoridades queda fuera (su escape es el «No aplica» de [[task-56]]). El backend dejó de borrar filas omitidas del payload (upsert puro) y la regla de limpieza anula conteos en servidor cuando `is_present=False` o `no_apply=True`, con espejo en la UI. El «tercer uso» (observable 1.7) resultó inexistente en código: barrido por inexistencia. La 0009 pobló `is_present` desde el M2M viejo.

## Criterios de aceptación

- [x] `PopulationQuantity.is_present` existe, con su migración
- [x] Una fila con respuesta y sin ningún conteo se persiste y vuelve igual al recargar
- [x] `Survey.sectors` es derivado y sus tres usos quedaron barridos
- [x] El selector ofrece solo «Sí» y «No»; el estado sin tocar no tiene opción visible
- [x] El encabezado de la columna dice «Está presente», sin signos de interrogación
