---
type: task
id: task-54
title: Revisar «Solicitar ajustes» disponible en un estado indebido
state: open
date: 2026-08-03
owner: ricardo
parent: "[[task-6]]"
source: ["[[2026-07-28-reunion-flujo-bp-e-informacion-base]]"]
---

# Revisar «Solicitar ajustes» disponible en un estado indebido

Detectado en vivo y dejado pasar en la reunión; Ricardo quiere revisarlo con detalle antes de decidir si se arregla o se acepta como está.

**Dónde ubicarlo en el acta.** El intercambio relevante es `[18:12]` – `[19:33]` de [[2026-07-28-reunion-flujo-bp-e-informacion-base]], al final del recorrido completo del paquete. Cita textual, `[18:33]`:

> «terminar la calificación de todas, y entonces cuando lo guardo tengo que... o lo recibo o lo marco como no acreditado. Pero bueno, en este caso lo voy a marcar como recibo peritamen y esto se tiene que cerrar solito. Y ahora sí como finalizar, **aunque esto de solicitar ajustes, mira, por ejemplo aquí me permite, eso está mal, no sé si está mal... o sea, no está estrictamente bien y creo que va a ser muy complicado moverlo**, pero el punto es que ya puedo ponerle finalizar. Ya se finalizó, ya está finalizado, ya nadie puede... o sea, como ya nadie puede cambiar estos...»

Contexto aledaño para reconstruir el estado en que ocurre:

- `[11:46]` es donde se introduce «solicitar ajustes» antes de calificar: «Yo aquí le puedo poner solicitar ajustes, incluso antes de calificarlo».
- El cierre de `[11:46]` explica por qué el paquete no puede finalizarse si una práctica requiere ajustes: «no puedo finalizar el paquete completo si hay una que requiere ajustes»; `[14:00]` continúa con la devolución del paquete entero.
- `[19:33]` cierra el recorrido con el paquete finalizado: «ya cumplió todo el flujo de ida y venida».

Lo que hay que determinar: en qué estado exacto aparece la transición «Solicitar ajustes» cuando ya no debería, si es un `next_statuses` demasiado permisivo en `api/flow/seed.py` o una regla de turno que no se está aplicando, y si corregirlo rompe combinaciones legítimas — que es lo que él temía con «va a ser muy complicado moverlo».

## Criterios de aceptación

- [ ] Está identificado el estado exacto y la transición que lo permite
- [ ] Ricardo decidió si se corrige o se acepta, y la razón quedó escrita
