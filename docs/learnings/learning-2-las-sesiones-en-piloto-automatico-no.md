---
type: learning
id: learning-2
title: Las sesiones en piloto automático no están gobernadas por ningún skill
state: pending
date: 2026-08-20
created: "2026-08-20T13:37:04-06:00"
scope: global
kind: new
author:
  role: coordinator
mode: requested
session: 9fe62aac-0320-41e0-8135-27bf4d63c60b
target: "[[global:task-13]]"
---

# Las sesiones en piloto automático no están gobernadas por ningún skill

## Qué pasó

Idea de Ricardo del 20 de agosto de 2026, al revisar los commits de una sesión en piloto automático (673dd34, 1b968fa, dc72a96) en el monorepo ONIGIES. Una sesión en piloto automático —la que corre sin Ricardo mirando— no tiene hoy nada que la gobierne: ni al ejecutarla ni al revisarla después. El costo se ve en la revisión, que es cuando Ricardo tiene que reconstruir a mano qué hizo la sesión y qué dejó anotado en el código.

## Propuesta

Un skill `autopilot`, específico y **no auto-invocable**, que cubra los dos momentos. Al ejecutar: dejar comentarios explicativos pensados para que Ricardo los lea después, y usar los prefijos de comentario del repo —`TO-AI:`, `AI-TASK:` y el `TO-RICK:` propuesto en [[learning-1]]—. Al revisar: abrir la revisión con un barrido de `grep` sobre `AI-TASK` y `TO-AI` para que nada anotado en el código se quede sin levantar. Alternativa a decidir en el diálogo, y es la razón de que el destino sea [[global:task-13]]: si es skill propio o se integra al `orchestrator`, que está en construcción y nació en la sesión orquestada del 12 de agosto. Aún no se dialoga: es idea, no decisión.

## Outcome
