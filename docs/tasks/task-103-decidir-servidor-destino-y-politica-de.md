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
---

# Decidir servidor destino y política de respaldos tras la reunión con Cómputo

Dos decisiones que se toman juntas y después de la reunión con Cómputo, no antes.

**El servidor.** La preferencia de Ricardo es uno nuevo, distinto del que gestionó Sandra: aunque ambos serían de la CIGU, son proyectos distintos con entornos diferentes, y cada uno es una máquina virtual con su propio bloque de recursos, no una computadora física completa. Pero la preferencia quedó condicionada a preguntar, así que no hay ADR hasta tener la respuesta.

**Los respaldos.** Hoy son diarios sobre la base, con retención de siete días, en el servidor de Yeeko. En un servidor nuevo hay que configurarlos desde cero porque no vienen por default. La ventana de siete días ha bastado para el único escenario real de pérdida —el borrado accidental por una persona usuaria, que se reporta de inmediato y se recupera del respaldo de la madrugada anterior—, pero el periodo actual es el más vulnerable: la estructura de la base todavía cambia mientras entran datos reales.

**Duda abierta de Ricardo, sin resolver:** sincronizar automáticamente esos respaldos con su propia computadora, como salvaguarda ante la destrucción del servidor. No tiene resuelto si es apropiado que datos institucionales vivan ahí. Tiene componente institucional, no solo técnico.

## Criterios de aceptación

- [ ] Decidido el servidor destino, con la respuesta de Cómputo en la mano
- [ ] Definida la política de respaldos del servidor nuevo: frecuencia, retención y destino
- [ ] Resuelto si la copia local en la máquina de Ricardo procede, y con qué condiciones
