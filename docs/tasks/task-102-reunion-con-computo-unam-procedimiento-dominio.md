---
type: task
id: task-102
title: "Reunión con Cómputo UNAM: procedimiento, dominio y capacidad de disco"
state: open
date: 2026-08-11
owner: ricardo
parent: "[[task-100]]"
source: ["[[2026-08-11-reunion-con-ruben-sobre-la-informacion-base]]"]
related: ["[[2026-09-04-reunion-con-ruben]]"]
---

# Reunión con Cómputo UNAM: procedimiento, dominio y capacidad de disco

Ricardo propuso en la reunión del 11 de agosto agendar una sesión con Cómputo UNAM antes de arrancar la migración, para no descubrir el procedimiento a mitad del camino. Rubén está fuera de la oficina; probablemente la gestione la próxima semana.

Las preguntas que se llevan:

- El procedimiento de solicitud del servidor, y en qué punto está el trámite que inició Sandy.
- Qué pasa con el dominio `onigies.unam.mx` durante la transición: si sigue apuntando al servidor viejo o al nuevo, y cómo se hace el cambio sin dejar el sitio público caído.
- La capacidad de disco: cuánta hay, si crece automáticamente, qué pasa si se llena y cuánto conviene solicitar de entrada, dado el volumen esperado de preguntas y comprobantes.
- Los pasos recomendados por ellos, para no pelear contra su procedimiento.

## Acuerdos de la reunión con Rubén (2026-09-04)

> **Corrección del 2026-09-11.** Una primera lectura de esta reunión dio por ocurrida la reunión con Cómputo y por hecha la migración. **Es falso para ONIGIES.** Ricardo aclaró que la máquina virtual migrada, la reunión con DGTIC y la solicitud de Pati que se mencionan en `[43:46]`–`[44:23]` pertenecen a **STIG** —otro proyecto del mismo cliente, la CIGU, con repo propio en `~/dev/unam/stig` y completamente independiente de este—, y que él los trajo a la conversación como contexto de los pasos que vendrían para ONIGIES. La limpia lleva una nota editorial en ese tramo para que el próximo lector no repita el error.

**Para ONIGIES la reunión con Cómputo no ha ocurrido, y ni siquiera se ha pedido.** Ricardo la sacó como pendiente vivo, `[41:12]`: «¿Qué más nos falta? Creo que eso es todo, ¿no? Sí, la reunión de Cómputo UNAM». Y Rubén respondió `[41:24]`: «**Ni siquiera lo he cuestionado**». Un mes después del 11 de agosto, la gestión que esta task esperaba de él sigue sin arrancar.

Lo que la reunión sí aporta, y es de ONIGIES:

- **Una vía nueva para abrir el trámite.** Hay alguien recién llegado a la CIGU que puede abrir el ticket. Ricardo, `[45:12]`: «puedes preguntarle de una vez a este muchachito»; `[45:33]`: «Él nos puede ayudar a hacer la apertura del ticket». **Identificado el 2026-09-11:** es **Carlos Gutiérrez**, titular del área TIC de la CIGU, quien levanta los tickets en la plataforma de la DGTIC por toda la entidad —cada entidad tiene una sola cuenta—. Quien aparecía antes en este lugar, Nazul Valencia, ya no trabaja en la CIGU. Quién es quién y qué le toca a cada quien: [[interlocucion-con-la-cigu]].
- **El cuello de botella es de Rubén y él lo nombra.** `[45:21]` «Todavía me falta crear ese vínculo»; `[45:30]` «Es que apenas acaba casi de entrar». No es un obstáculo de procedimiento: es que el contacto no está hecho.
- **Mientras tanto, los datos de ONIGIES viven en el servidor de Ricardo**, y él mismo sostiene que formalizar es lo correcto aunque no haya riesgo técnico. `[45:33]` «mientras corre en mi servidor y yo hago un puente»; `[45:51]` «La información está en mi servidor»; `[45:55]` «de todos modos es lo adecuado. La van a hacer de pedo en algún momento con el tema; no pasa nada, pero no porque la información no esté segura, solo porque la pueden hacer de tos». Rubén, `[45:53]`: «Sí, bueno, confío en ti» — la confianza personal existe, la cobertura institucional no.

Las tres preguntas que esta task lleva a la reunión —procedimiento, dominio durante la transición y capacidad de disco— **siguen las tres sin tocarse**.

## Criterios de aceptación

- [ ] La reunión con Cómputo UNAM ocurrió
- [ ] Están respondidas las tres preguntas: procedimiento, dominio durante la transición y capacidad de disco
