---
type: feedback
id: fb-2
title: Rubén nunca relee las preguntas idénticas en estructura, y ahí es donde se cuelan los copy-paste
state: discarded
date: 2026-09-11
created: "2026-09-11T10:49:41-06:00"
scope: local
kind: idea
author:
  role: subagent
  agent: intake-executor
  model: opus-5
mode: auto
session: b6c8a4f0-d2da-499c-be9d-a4efa64deb57
section: Catálogos editables del instrumento desde el dashboard
target: task-101
from-repo: onigies
source: ["[[2026-09-04-reunion-con-ruben]]"]
---

# Rubén nunca relee las preguntas idénticas en estructura, y ahí es donde se cuelan los copy-paste

## Qué pasó

La reunión del 4 de septiembre destapó dos preguntas —4.1 y 4.4— copiadas de armonización normativa y nunca ajustadas. Rubén explicó por qué sobreviven a su revisión:

> Es que yo no reviso esas preguntas porque, como son idénticas en estructura —no en contenido—, siempre que reviso nada más reviso lo que es diferente. Pero por eso se fue, justamente. (`[18:08]`)

No es descuido: es una estrategia de revisión racional frente a 41 observables con plantillas casi iguales. El instrumento está construido de modo que revisar lo repetido es caro y revisar lo distinto es barato, así que lo repetido no se revisa nunca. Ricardo encontró estos dos con asistencia de IA, no leyendo.

Lo mismo explica los otros hallazgos del mismo tipo: los nueve observables con doble título, el único de 41 sin signo de apertura, las tres grafías de «sexo y género».

## Propuesta

Que el editor del cuestionario por bloques ofrezca una vista de contraste —qué dice cada observable en el mismo campo, uno debajo de otro— en vez de obligar a abrirlos de uno en uno. La detección de estas erratas hoy depende de que alguien corra un barrido programático sobre el seed; con el seed retirado (adr-0015) esa vía ya no existe.

## Outcome

Ricardo lo descartó el 2026-09-11: «esa idea no se captura como Feedback [...] no son para eso». Un nodo `feedback` mide la conducta del asistente contra lo que algún artefacto del harness pedía; lo que hay aquí es una idea de producto sobre el editor del cuestionario, que no se mide contra nada del harness.

La idea de producto —la vista de contraste campo por campo en el editor por bloques— se rechazó. En su lugar se abrió [[task-157]], el barrido crítico del cuestionario sobre el contenido de producción cuando Rubén avise que terminó sus correcciones: ataca el mismo riesgo (lo repetido no se revisa nunca) sin construir interfaz.

La observación sobre Rubén sigue siendo válida y queda citada desde [[task-157]]; lo que no procede es su forma de nodo.
