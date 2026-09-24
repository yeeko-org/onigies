---
type: task
id: task-28
title: Ecuación del índice de avance y su agregación
state: open
date: 2026-08-03
owner: ricardo
parent: "[[task-5]]"
source: ["[[2026-06-26-seguimiento-pendientes-ruben]]"]
related: ["[[2026-09-04-reunion-con-ruben]]", "[[adr-0016]]", "[[2026-09-23-reunion-ruben]]"]
---

# Ecuación del índice de avance y su agregación

Cómo se calcula el avance de una IES y cómo se agrega de observable a componente, eje e índice global. Sin esto no se puede construir el cálculo del índice ni la visualización pública.

## Acuerdos de la reunión con Rubén (2026-09-04)

Dos reglas de agregación dichas por Rubén, y una metodología que Ricardo descartó. Ninguna estaba escrita.

**Dentro de una batería de criterios no hay jerarquía: todo se promedia.** `[53:03]` «no hay criterio, lo mejor siempre es promediado. De hecho así lo hicimos metodológicamente, pensando una jerarquía entre ellos: "esto vale 2"… No, no, todos valen lo mismo. El valor de institucionalización con armonización es el promedio de sus elementos». Ricardo lo respaldó por mantenibilidad, `[52:58]`: «yo no haría que esos valieran diferente, porque sería demasiado difícil de mantener».

**El número de criterios por batería no altera el default.** `[52:39]` Rubén: «este default no importa, porque hay tablitas que tienen cinco, otras cuatro».

**Los índices de carencia se descartan.** Ricardo, `[55:08]`: «esta es la metodología de "al menos": si no tienes al menos una, eso es como un índice de carencia. No solo existen los promedios, sino también los índices de carencia […] Por ejemplo, CONEVAL es así. Pero yo creo que no tiene sentido hacer eso, porque complicaría hacerlo lo más simple».

**Y el marco para decidir lo que falte**, de una consultora de ONU Mujeres a la que Rubén consultó, `[53:50]`: «no había realmente como un canon: todo es nada más tomar la decisión, dejarla metodológicamente sentada y argumentar un grado de razonabilidad».

**Fijado en [[adr-0016]] (2026-09-11).** Dos de las incógnitas de esta task ya no lo son: **el índice se expresa de 0 a 10** —fijado por Ricardo, de memoria, el 2026-09-11; declarada definitiva— y **dentro de una batería de criterios todo promedia sin jerarquía**, con el número de elementos de la batería siendo indiferente. Los índices de carencia quedaron descartados. Lo que sigue abierto es la agregación hacia arriba: de observable a componente, a eje y al índice global.

**Dónde vive el método cuando se implemente.** Ricardo propuso un skill como casa del cálculo de indicadores; la recomendación del asistente fue ADR hoy y skill al implementar, y así quedó. El skill no se escribe ahora: se escribe cuando exista el cálculo, y cita a [[adr-0016]] en vez de repetirla.

## Criterios de aceptación

- [ ] La ecuación y las reglas de agregación de observable a componente, eje e índice global están definidas por escrito
- [ ] Al implementar el cálculo se escribe el skill de cálculo de indicadores, citando [[adr-0016]] en vez de repetirla

## Reunión con Rubén, 2026-09-23

Fuente: [[2026-09-23-reunion-ruben]]. Dos preguntas nuevas para la ecuación, ninguna resuelta; el detalle con todas las citas está en [[task-173]], puntos (c) y (e).

- **¿Pesa el sí/no inicial?** Rubén, `[52:01]`–`[52:29]`: «Cuando tú le pones el ponderador de institucionalización, ¿solo va a jalar el cuadrito, o jala la pregunta de sí o no del comienzo? […] lo que quiero saber es si para ese ponderador, que por lo general va a ser de 5, utiliza la batería de acá abajito […] o si también toma en cuenta la pregunta de sí o no inicial». Ricardo, `[52:52]`: «Ahorita no lo toma; bueno, no he hecho ese cálculo, porque no están definidas estas cosas, pero no lo toma. No sé si tendríamos que, solo por contestar que sí, regalarles un punto; yo creo que no, pero no lo sé». Rubén, `[53:20]`: «Como que hay que revisarlo». El caso límite, Ricardo, `[53:22]`–`[53:36]`: «¿qué pasa si alguien pone que sí y en todas estas pone que no?»; Rubén, `[53:38]`: «sí puede pasar».
- **El reparto dentro de cada 5 y el peso de la sectorial**, `[1:06:23]`–`[1:19:55]`. Cada pregunta de la batería vale el 5 entre el número de preguntas (Ricardo, `[1:06:51]`: «Aquí hay 6 preguntas; entonces cada una vale 0.8»). Ricardo propone que la sectorial valga menos (`[1:08:03]`: «tal vez distribuiría 6, 3, 1, o 4, 4, 2») o multiplicarla por la proporción de sectores en que aplica (`[1:13:40]`). Rubén defiende que valga lo mismo (`[1:10:32]`: «Por eso, que valga lo mismo») y pide «una fórmula general, y las excepciones», probada con casos (`[1:16:52]`) y fácil de sostener en el informe metodológico (`[1:08:53]`, `[1:17:33]`). Quedó en «pensémoslo. Sí, y no urge» (Ricardo, `[1:19:50]`).
