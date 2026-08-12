---
type: task
id: task-109
title: Evaluar un QuestionBase abstracto para toda la familia de preguntas
state: open
date: 2026-08-11
owner: ricardo
parent: "[[task-101]]"
source: ["[[2026-08-11-reunion-con-ruben-sobre-la-informacion-base]]"]
---

# Evaluar un QuestionBase abstracto para toda la familia de preguntas

Idea para evaluar **cuando el cuestionario por observable esté cerrado**, no antes.

Hoy la familia de preguntas está partida en dos linajes que no se hablan: las cinco clases de `cp` —AQuestion, BQuestion, ReachQuestion, PlanQuestion, SpecialQuestion— y la nueva GeneralQuestion de `gen` ([[task-107]]). Comparten forma —un texto, un orden, una FK al padre— pero cada una la declara por su cuenta.

Lo que habría que evaluar: un modelo **abstracto** común que formalice `text`, `label`, `order` y `addl_config`, y que a partir de ahí habilite **componentes de captura compartidos** entre las dos secciones, en vez de dos juegos paralelos que se parecen sin ser lo mismo.

Se abre ahora para que la idea no se pierda, pero **no se implementa**: el momento de juzgarla es cuando `cp` esté cerrado y se sepa qué comparten de verdad las dos familias. Es diálogo, no obra.

## Criterios de aceptación

- [ ] Evaluado, con `cp` cerrado, si el modelo abstracto paga su costo
- [ ] Decidido si se implementa y con qué alcance, o si se descarta
