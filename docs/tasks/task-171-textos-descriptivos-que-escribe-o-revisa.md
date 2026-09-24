---
type: task
id: task-171
title: Textos descriptivos que escribe o revisa Rubén
state: open
date: 2026-09-23
owner: ricardo
parent: "[[task-2]]"
source: ["[[2026-09-23-reunion-ruben]]"]
related: ["[[task-169]]"]
---

# Textos descriptivos que escribe o revisa Rubén

Dos juegos de textos del instrumento que esperan la pluma de Rubén, más el ajuste de Ricardo para que se vean. Salen de la reunión con Rubén del 23 de septiembre ([[2026-09-23-reunion-ruben]]).

## Reunión con Rubén, 2026-09-23

**Descripciones de los ejes.** Ricardo, `[13:22]`–`[13:50]`, presentando el cuestionario principal: «Luego tenemos cada uno de los ejes con sus indicadores. No tenemos descripción del eje, ¿verdad?». Rubén, `[13:52]`: «No, no tenemos, pero la puedo escribir». Ricardo, `[13:55]`–`[14:02]`: «sí hay un campo de descripción, que solo tienen lleno no violencia —el eje 4— y el de igualdad; falta una descripción para inclusión y no discriminación. […] Si puedes, está bueno, y se lo voy a agregar. La verdad no lo había visto: no me gustó tanto cómo está la descripción; la voy a poner un poquito más grande aquí arriba». Y en `[38:32]`: «Ya dijimos lo de las descripciones de los ejes: faltan dos descripciones de ejes».

En la reunión solo se nombra el de inclusión y no discriminación; el segundo, por descarte entre los cuatro ejes (igualdad y no violencia ya la tienen), es cuidados. Es deducción, no algo dicho.

**Descripciones de los tipos de pregunta.** Ricardo, `[18:32]`–`[18:33]`: «cada uno de estos tipos —hay cuatro, seis tipos de pregunta, creo— va a tener su descripción, para entender qué es armonización, institucionalización, transversalidad sectorial, transversalidad orgánica, etcétera». Y en `[38:32]`, en el catálogo de tipos de pregunta: «hay estos seis, y tienen una descripción que agregué yo. Ah, no, este es el nombre público; no sale la descripción, perdón. Checo por qué no sale; tendría que aparecer aquí. Tienen una descripción que se inventó la IA y que mejor tú revisa, para que aparezca en el ícono de info. Es algo menor».

**Estado al 23 de septiembre** (dato de la sesión, no de la reunión): los seis borradores existen en el campo `QuestionType.description`, pendientes de deploy, y la captura cp los muestra como tooltip junto al título del grupo. La sesión paralela de diseño cp dejó la misma revisión como punto 12 de [[task-169]], que se cierra por duplicado si esta task la cubre: la cubre.

Owner `ricardo` porque los textos esperan a Rubén y Ricardo es quien se los pide; lo que es código (la descripción del eje más grande y arriba) se ejecuta cuando él lo encargue.

## Criterios de aceptación

- [ ] Rubén escribió las descripciones de los ejes de inclusión y no discriminación y de cuidados
- [ ] La descripción del eje se muestra más grande y arriba en la captura cp
- [ ] Rubén revisó los seis borradores de `QuestionType.description`
- [ ] Las descripciones de tipo de pregunta aparecen en producción junto al título del grupo
