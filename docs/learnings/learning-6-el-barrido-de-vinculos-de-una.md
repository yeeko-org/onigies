---
type: learning
id: learning-6
title: El barrido de vínculos de una task cross-proyecto no miró el grafo global
state: pending
date: 2026-08-20
created: "2026-08-20T14:59:58-06:00"
scope: global
kind: deviation
author:
  role: subagent
  model: claude-opus-5[1m]
mode: requested
session: 9fe62aac-0320-41e0-8135-27bf4d63c60b
expected: skills/documenter/SKILL.md
section: El grafo cruza repos por el global, que es el hub
---

# El barrido de vínculos de una task cross-proyecto no miró el grafo global

## Qué pasó

Sesión del 20 de agosto de 2026 en el monorepo ONIGIES. Se me encargó abrir una task de alcance declaradamente cross-proyecto —revisar todas las implementaciones del motor de colecciones que Ricardo reutiliza en varios repos— y barrer el grafo en busca de nodos con los que ligarla. El barrido lo hice completo y en profundidad, pero **solo sobre `docs/` del proyecto**: recorrí tasks, decisions, records y notes de ONIGIES y no toqué `~/.claude/system/`.

El resultado fue una task ciega. En el grafo global ya existía `task-43`, «Empaquetar collections en un repo propio consumible por varios monorepos», abierta el 17 de agosto —tres días antes—, que cubre el mismo terreno con más alcance y que además ya daba por cumplida la condición del tercer proyecto del `adr-0005` de ONIGIES, con `sentencias-salud` declarándose consumidor del motor común. Nació un duplicado parcial, y ninguna de las dos citaba a la otra hasta que otro agente encontró la colisión.

La ironía del caso es que el nodo mal barrido terminó viviendo en el grafo global: primero lo abrí en el proyecto, Ricardo corrigió que iba en el global, y aun después de mudarlo no se me ocurrió barrer el grafo al que acababa de mudarlo.

## Propuesta

Que quede escrito lo que hoy no está: **antes de crear un nodo de alcance cross-proyecto o global, el barrido de vínculos incluye el grafo global, no solo el del repo donde corre la sesión**. Ricardo ya lo avaló en el momento («estamos en la misma línea»).

El skill dice que el global es el hub del grafo y da la forma `[[repo:id]]` para citar desde allá hacia un proyecto, pero no dice en ningún lado que haya que ir a mirarlo antes de escribir. Sin esa frase, el barrido por omisión se queda en el repo local, que es exactamente lo que pasó aquí.

## Outcome
