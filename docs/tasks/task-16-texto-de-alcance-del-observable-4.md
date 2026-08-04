---
type: task
id: task-16
title: Texto de alcance del observable 4.4
state: open
date: 2026-08-03
owner: ricardo
parent: "[[task-2]]"
source: ["[[2026-07-03-dudas-del-instrumento-con-el-cliente]]", "[[2026-07-28-reunion-flujo-bp-e-informacion-base]]"]
---

# Texto de alcance del observable 4.4

El observable 4.4 (personas de primer contacto especializadas en violencias de género) tiene copiadas literalmente las preguntas de alcance de los observables de armonización normativa: «¿A qué poblaciones se consideró este proceso de armonización?». Es un error de copiado del instrumento original y está sembrado verbatim. Hay propuesta redactada, falta que el cliente la confirme.

Al resolverse: corregir [[cuestionario-2026-reducido]], luego `api/question/seed_data/axis_4.py`, y re-correr `load_questionnaire`.

**Ventana acordada: semana del 2026-08-03.** En la reunión del 28 de julio este hallazgo se leyó en pantalla `[36:12]` y el cliente lo confirmó en el acto («Claro, sí, está mal redactada»), pero se acordó no resolverlo por correo sino sobre la base de producción, junto con la revisión general de [[task-50]]. `[36:41]` «Mejor el lunes. El lunes para que ya se haga directo sobre la base final, o sea, porque si te la mando yo voy a tener que meterme al script y no sé qué, y se va a perder, como que es más difícil trazabilidad. Y ya si lo hacemos con la base real real pues no va a haber problema, no se va a volar».

## Criterios de aceptación

- [ ] El cliente confirmó el texto
- [ ] El instrumento reducido, el seed y la base dicen lo mismo
