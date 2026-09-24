---
type: task
id: task-153
title: "Ventana de respuesta de las IES: cuestionario visible pero no respondible hasta el 25 de septiembre"
state: open
date: 2026-09-11
owner: ai
parent: "[[task-2]]"
source: ["[[2026-09-04-reunion-con-ruben]]"]
related: ["[[2026-09-04-reunion-con-ruben]]", "[[adr-0015]]", "[[2026-09-23-reunion-ruben]]", "[[task-175]]"]
---

# Ventana de respuesta de las IES: cuestionario visible pero no respondible hasta el 25 de septiembre

Las IES tienen que poder **ver** el cuestionario completo antes de poder **responderlo**. La fecha comprometida de apertura es el **25 de septiembre**.

**No es el interruptor de [[adr-0015]]**, que gobierna si la estructura del cuestionario se edita desde el dashboard y cierra de ida. Esta es la compuerta de respuesta de las IES, y es otra cosa.

`[22:03]` Ricardo: «esto es lo único para cerrar ya el cuestionario y poderlo mostrar. Y lo que yo puedo hacer es programar que no se pueda responder todavía hasta el 25».

**Nota de Ricardo (2026-09-11): si se puede liberar antes del 25, mucho mejor.** Coincide con lo que él mismo planteó en la reunión, `[22:03]`: «más bien: si lo podemos abrir antes, pues que se abra. Creo que no hay ningún impedimento para abrirlo antes del 25, ¿o sí?». La objeción de Rubén fue de acompañamiento, no de fecha: `[22:30]` «tú ya un poco viste cómo es: sí se necesita mucho acompañamiento». Así que el diseño debería permitir **adelantar** la apertura sin tocar código.

**La fecha viene con ambigüedad en la propia reunión**, `[13:24]`: «Bueno, dijimos que el 10, ¿no? ¿El 10 de septiembre o qué día era que lo íbamos a abrir? El 25». Ricardo se corrige solo; el resto de la conversación confirma el 25 (`[22:03]`, `[23:04]`, `[23:20]`).

**Y el compromiso del 25 es de plataforma, no de documento**, `[23:16]`: «ese día cumplimos con llegar ya con el cuestionario montado». El documento va antes y por separado ([[task-150]]).

## Criterios de aceptación

- [x] Las IES ven el cuestionario completo sin poder capturar respuestas (2026-09-22, en local y solo IES de prueba: cp no está en `PUBLISHED_SECTIONS`; [[adr-0018]])
- [x] La fecha de apertura de respuestas es configurable y se puede adelantar sin tocar código (`Period.cp_open_at`, admin y catálogo)
- [ ] El cuestionario quedó abierto a respuestas el 25 de septiembre o antes (depende del deploy, [[task-163]], y de publicar cp en `PUBLISHED_SECTIONS`)

## Construido el 2026-09-22

La compuerta es [[adr-0018]]: `Period.cp_open_at` más el `GeneralPackage` en `gen_finished` (así aplica también [[adr-0007]], como Ricardo lo precisó: se ven las preguntas, se inhabilita toda captura). Las IES de prueba están exentas de la fecha `cp_open_at` pero no del prerrequisito `gen_finished` ([[adr-0018]] enmendada el 2026-09-23; [[task-168]] punto 10, cerrada). Falta desplegar y fijar la fecha en el admin ([[task-163]]). Record [[2026-09-22-cierre-cuestionario-principal-captura-y-borrado]].

## Reunión con Rubén, 2026-09-23

Fuente: [[2026-09-23-reunion-ruben]].

- **La fecha de apertura por periodo**, Ricardo, `[12:40]`: «una de las cosas que ya agregué es que se puede editar una fecha de apertura para cada periodo, para empezar a registrar las preguntas generales, el cuestionario principal» (es `Period.cp_open_at`).
- **Rubén vio la compuerta y la aprobó** ([[adr-0018]]). Ricardo, `[23:54]`–`[24:32]`, entrando como una IES sin base validada: «está deshabilitado, no puedo seleccionar nada, porque aquí dice "tu información base todavía no está validada; hasta entonces puedes consultar el cuestionario, pero no resolverlo"». Rubén, `[24:52]`: «Me encanta».
- **Liberar ya.** Ricardo, `[34:54]`: «El cuestionario ya podríamos liberarlo, si quieres». Rubén, `[35:17]`: «Sí, yo lo liberaría, porque el viernes ya se los puedo mostrar»; `[12:04]`: «el viernes tengo reunión y me van a preguntar». El viernes es el 25 de septiembre, la fecha comprometida. El deploy, en [[task-163]].
- **Fechas límite por sección.** La reunión (`[35:41]`–`[37:59]`) tocó fechas límite para revisar cada sección. Respuesta de Ricardo en el triage: «Eso no nos corresponde, no guardar nada, con los campos existentes tenemos, si acaso uno para "cierre de cp"». El posible campo de cierre de cp queda como decisión suya en [[task-175]], entrada (b).
