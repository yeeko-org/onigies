---
type: task
id: task-103
title: Decidir servidor destino y política de respaldos tras la reunión con Cómputo
state: open
date: 2026-08-11
owner: ricardo
parent: "[[task-100]]"
source: ["[[2026-08-11-reunion-con-ruben-sobre-la-informacion-base]]"]
depends-on: ["[[task-102]]"]
related: ["[[2026-09-04-reunion-con-ruben]]"]
---

# Decidir servidor destino y política de respaldos tras la reunión con Cómputo

Dos decisiones que se toman juntas y después de la reunión con Cómputo, no antes.

**El servidor.** La preferencia de Ricardo es uno nuevo, distinto del que gestionó Sandra —la máquina virtual del STIG—: aunque ambos serían de la CIGU, son proyectos distintos con entornos diferentes, y cada uno es una máquina virtual con su propio bloque de recursos, no una computadora física completa. Pero la preferencia quedó condicionada a preguntar, así que no hay ADR hasta tener la respuesta.

**Los respaldos.** Hoy son diarios sobre la base, con retención de siete días, en el servidor de Yeeko. En un servidor nuevo hay que configurarlos desde cero porque no vienen por default. La ventana de siete días ha bastado para el único escenario real de pérdida —el borrado accidental por una persona usuaria, que se reporta de inmediato y se recupera del respaldo de la madrugada anterior—, pero el periodo actual es el más vulnerable: la estructura de la base todavía cambia mientras entran datos reales.

**Duda abierta de Ricardo, sin resolver:** sincronizar automáticamente esos respaldos con su propia computadora, como salvaguarda ante la destrucción del servidor. No tiene resuelto si es apropiado que datos institucionales vivan ahí. Tiene componente institucional, no solo técnico.

## Acuerdos de la reunión con Rubén (2026-09-04)

**La duda abierta de esta task —si es apropiado que datos institucionales vivan en la máquina de Ricardo— tiene ahora evidencia de la postura de la institución**, aunque no una respuesta.

Rubén explicó por qué la CIGU usa Outlook y no Google, `[46:05]`: «porque dicen que el de Google no sé qué tiene, pero que parece como que la información se almacena en no sé qué lugar, como que es de la empresa y no de la universidad. Yo no entiendo esas cosas, pero por esa razón usamos este servicio». No es una regla que él conozca ni que sepa defender, pero sí la práctica vigente: **la UNAM ya rechazó una vez alojar datos institucionales fuera de su control**, con ese mismo argumento.

En paralelo, sobre el servidor actual, Rubén dijo `[45:53]` «Sí, bueno, confío en ti» y Ricardo respondió `[45:55]` «pero de todos modos es lo adecuado» —formalizar—. La confianza personal existe; la cobertura institucional no.

**Interpretación del asistente, no dato:** si la UNAM aplica ese criterio de forma consistente, la copia local en la máquina de Ricardo es la opción más difícil de sostener de las tres que esta task evalúa. No lo dijo nadie en la reunión.

**Revisado el 2026-09-11 tras la aclaración de Ricardo sobre STIG.** Nada de este bloque cambia: el criterio de Outlook es de la CIGU y aplica a ONIGIES igual que a cualquier proyecto suyo, y `[45:49]`–`[46:05]` sí es conversación sobre el servidor de ONIGIES. Lo que **no** vale como precedente es la migración a la máquina virtual de `[43:46]`: esa ocurrió para STIG, así que **no hay todavía un caso resuelto de servidor de la UNAM para este proyecto** del que copiar la política de respaldos. Esta task sigue esperando a [[task-102]], que no ha avanzado.

## Criterios de aceptación

- [ ] Decidido el servidor destino, con la respuesta de Cómputo en la mano
- [ ] Definida la política de respaldos del servidor nuevo: frecuencia, retención y destino
- [ ] Resuelto si la copia local en la máquina de Ricardo procede, y con qué condiciones
