---
type: decision
id: adr-0016
title: El índice se expresa de 0 a 10 y dentro de cada batería de criterios todo promedia sin jerarquía
state: accepted
date: 2026-09-04
origin: meeting
deliberation: dialogued
rationale: recorded
source: ["[[2026-09-04-reunion-con-ruben]]"]
related: ["[[adr-0014]]", "[[adr-0015]]", "[[task-27]]", "[[task-28]]", "[[task-15]]"]
---

# El índice se expresa de 0 a 10 y dentro de cada batería de criterios todo promedia sin jerarquía

## Contexto y planteamiento del problema

La escala del índice del ONIGIES llevaba pendiente desde la reunión de junio de 2026 ([[task-27]]): el cálculo de agregados y la presentación pública del índice dependían de ella y nadie la había fijado. En la reunión presencial del 4 de septiembre Ricardo la sacó junto con la ponderación, `[47:23]`: «hay otros criterios que todavía no sé si ya están definidos, no me acuerdo, como lo del 0 al 10 o del 0 al 5: cuánto va a pesar cada cosita […] Siento que es una discusión metodológica importante».

La conversación resolvió la escala y, de paso, dos reglas de agregación que tampoco estaban escritas en ninguna parte.

**Nota de procedencia:** el pipeline de transcripción entregó la frase decisiva de Rubén como «entonces creo que es mejor tener una de 0 a 5», en contradicción con el resto de su propio párrafo. Ricardo, de memoria, el 2026-09-11: Rubén dijo **«de 0 a 10»**, y la declaró definitiva. La limpia lleva la corrección y su nota; la cruda conserva la salida del pipeline. Esta ADR se escribe sobre esa declaración de Ricardo, no sobre una verificación del audio.

## Criterios de decisión

- La escala no puede invitar a comparar contra la metodología anterior, que medía otra cosa.
- El método tiene que ser defendible por escrito, no por apego a un estándar externo: no lo hay.
- Las reglas de agregación no pueden exigir justificar un peso distinto para cada criterio dentro de una batería, porque no hay criterio para asignarlo.

## Opciones consideradas

**Escala 0–5.** Es la del instrumento anterior. Descartada: `[47:51]` «si lo dejas de 0 al 5 todas van a sacar puntos más bajos, eso es obvio. ¿Y qué te van a decir? "Bajé". Y lo que tenemos que responder es "no bajaste, porque no es la misma metodología, no estás midiendo lo mismo"».

**Escala 0–10.** La elegida.

**Jerarquía de pesos dentro de cada batería de criterios.** Se intentó en su momento y se abandonó. Rubén, `[53:03]`: «además no hay criterio, lo mejor siempre es promediado. De hecho así lo hicimos metodológicamente, pensando una jerarquía entre ellos: "esto vale 2"… No, no, todos valen lo mismo».

**Índices de carencia en vez de promedios.** Ricardo los puso sobre la mesa y él mismo los descartó, `[55:08]`: «esta es la metodología de "al menos": si no tienes al menos una, eso es como un índice de carencia […] Por ejemplo, CONEVAL es así. Pero yo creo que no tiene sentido hacer eso, porque complicaría hacerlo lo más simple».

## Decisión

**1. El índice se expresa en una escala de 0 a 10.** `[47:51]` «Yo soy de subirlo al 10».

**2. Dentro de una batería de criterios no hay jerarquía: el valor es el promedio simple de sus elementos**, y el número de elementos de la batería no altera nada. `[53:03]` «El valor de institucionalización con armonización es el promedio de sus elementos»; `[52:39]` «este default no importa, porque hay tablitas que tienen cinco, otras cuatro».

**3. Los pesos por tipo de pregunta viven en un default general editable por observable**, no se capturan uno por uno. Ricardo lo propuso aquí, `[51:56]`: «lo ideal es que haya un default que sea para los 41 observables, y que algunos observables —sobre todo los que tienen una lógica distinta— los puedas personalizar; que no tengas que personalizar uno por uno». La forma concreta que tomó —`QuestionType` como fuente del default, `ObservableQuestionType` para el peso propio, el catálogo editable en el dashboard— es de [[adr-0014]] y [[adr-0015]], que son posteriores a esta reunión y que esta decisión **no repite**.

**4. Los índices de carencia quedan descartados** como metodología de agregación.

## Razones

Las tres de Rubén para el 0–10, en la §«Acuerdos» de [[task-27]] con su cita completa: diferenciar la medición de la metodología anterior y poder responder al «bajé» de una IES; matizar la carga psicológica de un número bajo; y que 0–10 es el rango habitual de las métricas universitarias.

Y la razón de fondo, que es por qué esto es una decisión y no un hallazgo: **no hay canon**. Rubén consultó a una especialista en estadísticas para indicadores en organismos internacionales, de ONU Mujeres, y la respuesta fue que no existe un estándar al que apegarse. `[53:50]`: «no había realmente como un canon: todo es nada más tomar la decisión, dejarla metodológicamente sentada y argumentar un grado de razonabilidad. Entonces, en realidad es lo que siempre hago: hacer las cosas con seriedad, no definir al azar el criterio, sino hacerlo por una razón, esa razón escribirla y argumentar». Ella misma enumeró el desorden del campo, `[54:48]`: «hay índices de 0 al 5, hay índices de 0 al 3 —no sé por qué—, hay índices de 5 al 10, hay índices de 0 al 4, hay unos que son porcentajes».

## Consecuencias

- [[task-27]] cierra con esta ADR como `outcome`.
- [[task-28]] —la ecuación del índice y su agregación— pierde dos incógnitas (escala y regla dentro de batería) y conserva las demás: cómo se agrega de observable a componente, a eje y al índice global.
- Lo que **no** decide esta ADR: si institucionalización pesa distinto que transversalidad y que las preguntas específicas. Eso quedó abierto en la reunión —`[53:03]` «lo que no hemos definido es si institucionalización vale algo distinto que transversalidad y que las otras preguntas, que son específicas»— y lo fijó el acuerdo por WhatsApp del 7 de septiembre (5 / 2.5 / 2.5 sobre 10), recogido en [[adr-0014]] y [[adr-0015]]. Los pesos propios por observable siguen nulos ([[task-15]]).
- El método de cálculo, cuando se implemente, se documenta en un skill propio que cita esta ADR ([[task-28]]).
