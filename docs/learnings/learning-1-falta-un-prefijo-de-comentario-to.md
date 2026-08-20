---
type: learning
id: learning-1
title: "Falta un prefijo de comentario TO-RICK: para que la IA deje dudas a Ricardo en el código"
state: pending
date: 2026-08-20
created: "2026-08-20T13:36:26-06:00"
scope: global
kind: new
author:
  role: coordinator
mode: requested
session: 9fe62aac-0320-41e0-8135-27bf4d63c60b
target: "[[global:task-13]]"
---

# Falta un prefijo de comentario TO-RICK: para que la IA deje dudas a Ricardo en el código

## Qué pasó

Idea de Ricardo del 20 de agosto de 2026, al revisar los commits de una sesión en piloto automático (673dd34, 1b968fa, dc72a96) en el monorepo ONIGIES. Hoy el repo tiene dos prefijos de comentario y los dos van en la misma dirección, de Ricardo hacia la IA: `TO-AI:` para las dudas e indicaciones que él deja en el código, y `AI-TASK:` para las mini-tareas anotadas ahí mismo. Falta el sentido contrario: no hay forma de que la IA deje, en el propio código, lo que topó al implementar y no puede resolver sola. Hoy eso se diluye en el chat de una sesión que ya se cerró. Ricardo lo dijo textual: era mejor ponerlo como learning general para el orchestrator/autopilot.

## Propuesta

Un prefijo `TO-RICK:` simétrico de `TO-AI:`, con el que la IA deje preguntas y dudas dirigidas a Ricardo en el lugar exacto del código donde importan. Su uso natural son las sesiones en piloto automático, así que se dialoga junto con la idea del skill autopilot y aterriza donde aterrice esa: skill propio o parte del orchestrator de [[global:task-13]]. Aún no se dialoga: es idea, no decisión.

## Outcome
