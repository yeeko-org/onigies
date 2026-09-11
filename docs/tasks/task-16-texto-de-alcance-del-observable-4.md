---
type: task
id: task-16
title: Texto de alcance del observable 4.4
state: open
date: 2026-08-03
owner: ricardo
parent: "[[task-2]]"
source: ["[[2026-07-03-dudas-del-instrumento-con-el-cliente]]", "[[2026-07-28-reunion-flujo-bp-e-informacion-base]]"]
related: ["[[2026-09-04-reunion-con-ruben]]"]
---

# Texto de alcance del observable 4.4

El observable 4.4 (personas de primer contacto especializadas en violencias de género) tiene copiadas literalmente las preguntas de alcance de los observables de armonización normativa: «¿A qué poblaciones se consideró este proceso de armonización?». Es un error de copiado del instrumento original y está sembrado verbatim. Hay propuesta redactada, falta que el cliente la confirme.

Al resolverse: corregir [[cuestionario-2026-reducido]], luego `api/question/seed_data/axis_4.py`, y re-correr `load_questionnaire`.

**Ventana acordada: semana del 2026-08-03.** En la reunión del 28 de julio este hallazgo se leyó en pantalla `[36:12]` y el cliente lo confirmó en el acto («Claro, sí, está mal redactada»), pero se acordó no resolverlo por correo sino sobre la base de producción, junto con la revisión general de [[task-50]]. `[36:41]` «Mejor el lunes. El lunes para que ya se haga directo sobre la base final, o sea, porque si te la mando yo voy a tener que meterme al script y no sé qué, y se va a perder, como que es más difícil trazabilidad. Y ya si lo hacemos con la base real real pues no va a haber problema, no se va a volar».

**2026-09-07:** la versión maquetada y final del instrumento **no corrige** este texto —el 4.4 sigue preguntando por «este proceso de armonización»— ([[2026-09-07-cotejo-del-instrumento-maquetado]]). La task sigue abierta y sigue esperando lo mismo: la decisión de la CIGU, hoy en el punto A.1 del documento de correcciones.

## Acuerdos de la reunión con Rubén (2026-09-04)

Rubén leyó el punto en pantalla y **aceptó la corrección en el acto, por segunda vez** —ya lo había hecho el 28 de julio—, ahora comprometiéndose a aplicarla él mismo desde el dashboard: `[17:34]` «esta que encontraste yo la puedo corregir sin problema, la 4.1. Luego el 4.4 dice "a cuántas instancias académicas se consideró para este proceso": sí tiene el mismo problema, es un copy-paste que luego no se ajustó».

También aceptó el «¿» de apertura faltante, que es del mismo 4.4: `[19:06]` «este observable: la pregunta inicial no abre interrogación, le falta la…».

**Lo que cambia respecto de la ventana anterior:** ya no hace falta tocar `seed_data` ni re-correr `load_questionnaire` —el seed se retiró ([[adr-0015]])—; la corrección la hace Rubén en el dashboard. Lo que sigue debiendo es que la haga.

## Criterios de aceptación

- [ ] El cliente confirmó el texto
- [ ] El instrumento reducido, el seed y la base dicen lo mismo
