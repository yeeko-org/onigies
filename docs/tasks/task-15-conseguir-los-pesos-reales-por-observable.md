---
type: task
id: task-15
title: Conseguir los pesos reales por observable
state: open
date: 2026-08-03
owner: ricardo
parent: "[[task-2]]"
source: ["[[2026-07-04-seed-del-cuestionario]]"]
related: ["[[2026-09-04-reunion-con-ruben]]"]
---

# Conseguir los pesos reales por observable

Bloqueado: el cliente no ha entregado la fuente de ponderaciones. Mientras tanto los pesos quedan en `null` y aplica el fallback a `QuestionType.default_weight` (a=60, b=40), lo que significa que cualquier índice calculado hoy es provisional.

**2026-09-07:** la versión maquetada y final del instrumento **no trae ponderaciones** ([[2026-09-07-cotejo-del-instrumento-maquetado]]). Se descarta la vía más plausible de desbloqueo: el documento del cliente no es la fuente de los pesos, así que hay que pedirla aparte o cerrar la task documentando el fallback como decisión definitiva.

**2026-09-07, segunda nota:** cambió la estructura, no los valores. Los pesos ya no son columnas de `Observable` sino filas de `ObservableQuestionType` (una por observable y tipo, `weight` nullable, efectivo = propio o `QuestionType.default_weight`), editables desde el dashboard por su catálogo ([[adr-0014]]). Siguen todos en `null`. Ponderación tentativa acordada con Rubén por WhatsApp: armonización e institucionalización 5, transversalidad sectorial 2.5, orgánica 2.5, sobre 10, pendiente de simular con él ([[task-135]]).

## Acuerdos de la reunión con Rubén (2026-09-04)

Esta reunión es **anterior** al acuerdo por WhatsApp del 7 de septiembre y al deploy del 10, así que vale como procedencia de lo que después se implementó, no como trabajo nuevo.

**De dónde salió «todos los observables valen lo mismo».** No es idea de Ricardo: `[48:29]` Rubén, «lo que habíamos hablado con Isabela, que a mí me pareció bien —fue una propuesta de ellas—, es que quizás lo mejor, para no meternos en ese rollo de tener que justificar que vale 3, que vale 2, que vale tal, es que todo valiera lo mismo en términos de observables». Y `[50:54]`: «lo que me da tranquilidad es que la idea es que si cada observable vale 10, internamente…».

**De dónde salió el diseño «default general + override por observable», que es lo que [[adr-0015]] implementó seis días después.** Ricardo lo propuso aquí, `[51:56]`: «lo ideal es que haya un default que sea para los 41 observables, y que algunos observables —sobre todo los que tienen una lógica distinta— los puedas personalizar; que no tengas que personalizar uno por uno, sino que tengas un default, y si modificas ese default, es el que se comporta diferente al default general». Y `[51:19]`: «tú puedes tener un default para institucionalización y transversalización. Ese no hay ningún lugar donde se pueda editar todavía, tengo que pensar dónde». **Ya cubierto**: esa superficie existe desde el 10 de septiembre.

**El punto de partida que citaron:** `[51:19]` «antes lo que teníamos era 3 y 2»; `[51:53]` Rubén, «y había unos que valían 5 porque no había transversalización».

**Lo que la reunión dejó abierto y el acuerdo posterior cerró:** si institucionalización pesa distinto que transversalidad. `[53:03]` «lo que no hemos definido es si institucionalización vale algo distinto que transversalidad y que las otras preguntas, que son específicas». El 5 / 2.5 / 2.5 del 7 de septiembre responde eso. Los pesos propios siguen nulos.

## Criterios de aceptación

- [ ] Los pesos están sembrados desde una fuente entregada por el cliente, o se documenta que el fallback es la decisión definitiva

## Nota del 10 de septiembre de 2026

La superficie de captura ya existe: la lista de tipos del bloque «Definición del observable» en el dashboard, con el default del tipo visible y el aviso de ponderación pendiente ([[adr-0015]]). Rubén puede capturarlos él mismo; los 120 pesos propios siguen nulos.
