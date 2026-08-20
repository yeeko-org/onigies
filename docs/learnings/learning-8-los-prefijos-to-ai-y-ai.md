---
type: learning
id: learning-8
title: Los prefijos TO-AI y AI-TASK quedaron establecidos y no están escritos en ningún harness
state: pending
date: 2026-08-20
created: "2026-08-20T15:08:27-06:00"
scope: global
kind: new
author:
  role: fork
mode: requested
session: 9fe62aac-0320-41e0-8135-27bf4d63c60b
target: CLAUDE.md
---

# Los prefijos TO-AI y AI-TASK quedaron establecidos y no están escritos en ningún harness

## Qué pasó

El 20 de agosto de 2026 Ricardo estableció y estrenó dos convenciones de marcadores en comentarios, sobre los commits de piloto automático de ONIGIES: `TO-AI:` — dudas suyas dirigidas a la IA, dejadas en el código; la IA las levanta, se aclaran en diálogo y, detonado ese diálogo, se borran del código. `AI-TASK:` — mini-tareas anotadas directo donde aplican; la IA las barre (grep) y las resuelve. Ambas funcionaron completas en la sesión: 6 TO-AI aclarados y borrados, 3 AI-TASK resueltos. Ricardo además las registró como pattern TODO en su PyCharm global. La familia se completa con el `TO-RICK:` propuesto en [[learning-1]], y el barrido de estos marcadores es parte del skill de piloto automático propuesto en [[learning-2]] — este nodo es distinto de aquellos porque su destino es inmediato y barato: los prefijos ya operan hoy y solo falta escribirlos.

## Propuesta

Estandarizarlas en el harness global «tal vez con una línea», en palabras de Ricardo: una línea en el CLAUDE.md global que nombre los prefijos y su dinámica, aplicable en todos los repos. La redacción exacta se dialoga; el destino alternativo (dentro del skill autopilot/orchestrator) se resuelve donde [[learning-2]].

## Outcome
