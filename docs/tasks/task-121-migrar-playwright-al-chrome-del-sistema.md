---
type: task
id: task-121
title: Migrar playwright al Chrome del sistema (channel chrome)
state: open
date: 2026-08-12
owner: ai
parent: "[[task-94]]"
source: ["[[2026-08-12-sesion-orquestada-a-b-captura-correcta]]"]
---

# Migrar playwright al Chrome del sistema (channel chrome)

`nuxt/playwright.config.ts` usa el Chromium empaquetado (`devices['Desktop Chrome']` sin `channel`), mientras la regla global de testing de Ricardo pide Playwright con el Chrome del sistema (`channel: 'chrome'`). Preexistente, detectado al escribir los e2e de gen. Cambio de una línea más verificar que los 37 specs siguen verdes en ese canal.

## Criterios de aceptación

- [ ] La config usa `channel: 'chrome'` y la suite completa pasa
