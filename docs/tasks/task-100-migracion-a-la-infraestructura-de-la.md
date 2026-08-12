---
type: task
id: task-100
title: Migración a la infraestructura de la UNAM
state: open
date: 2026-08-11
owner: ricardo
source: ["[[2026-08-11-reunion-con-ruben-sobre-la-informacion-base]]"]
---

# Migración a la infraestructura de la UNAM

Raíz nueva para lo que hasta hoy solo vivía en el roadmap del skill `deployment`, que se declara a sí mismo un esqueleto. La reunión del 11 de agosto le puso contenido.

Estado que hereda: el servidor actual es de 2018 —ocho años— y está obsoleto, con acceso de Ricardo; el trámite del nuevo lo inició Sandy y Nazul podría ayudar a avanzarlo; mientras tanto la plataforma vive en un servidor de Yeeko, con respaldo diario de la base retenido siete días. Ricardo evalúa el riesgo real: no el colapso de la base —está en AWS y es estable— sino el borrado accidental por una persona usuaria, el único caso en que la ventana de siete días ha servido de verdad. Rubén subrayó que el periodo más vulnerable es el actual, con la estructura de la base todavía cambiando y datos reales entrando en paralelo.

**Por qué no hay ADR todavía.** La preferencia de Ricardo es que sea un servidor nuevo y no el mismo que gestionó Sandra —serían proyectos distintos con entornos distintos, aunque ambos de la CIGU—, pero condicionada: «pero preguntamos». La decisión se toma con la respuesta de Cómputo en la mano.

Hijas: [[task-95]], [[task-25]], más la reunión con Cómputo y la decisión que la sigue.

## Criterios de aceptación

- [ ] El API corre en infraestructura de la UNAM y no en el servidor de Yeeko
- [ ] El dominio onigies.unam.mx sirve el sistema nuevo sin el puente temporal a Netlify
- [ ] Hay una política de respaldos escrita y funcionando en el servidor destino
