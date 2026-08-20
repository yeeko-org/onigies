---
type: learning
id: learning-7
title: "El subagente dejó de explicar sus comandos Bash: en subagentes la explicación es el description"
state: pending
date: 2026-08-20
created: "2026-08-20T15:08:27-06:00"
scope: global
kind: deviation
author:
  role: subagent
  model: claude-opus-5
mode: requested
session: 9fe62aac-0320-41e0-8135-27bf4d63c60b
expected: CLAUDE.md
section: Always explain me, with a single line the Bash commands proposed
---

# El subagente dejó de explicar sus comandos Bash: en subagentes la explicación es el description

## Qué pasó

Sesión del 20 de agosto de 2026 en ONIGIES. Un ejecutor Opus recibió completo el CLAUDE.md global —incluida la regla de explicar cada comando Bash con una línea—, llenó el `description` de sus dos primeras llamadas y después dejó de hacerlo sin razón. Ricardo lo detectó dialogando directo con el subagente, que reconoció la desviación: no fue falla de entrega del harness. El matiz que hace al caso más que un descuido: en un subagente, la prosa entre llamadas no llega a Ricardo — el único canal que ve en vivo es el parámetro `description` de la herramienta Bash, exactamente lo que se omitió. La regla, leída para subagentes, no es «escribe una línea en el chat» sino «llena siempre `description`».

## Propuesta

Dos piezas, ambas por decidir con Ricardo: (1) que la regla nombre la variante para subagentes — «llenar siempre el `description` de Bash», que es el único canal vivo hacia Ricardo mientras corren; (2) evaluar mover la línea de lugar: hoy vive al final de la sección `## Comments` del CLAUDE.md global, que trata de comentarios en código, y ahí es fácil perderla de vista.

## Outcome
