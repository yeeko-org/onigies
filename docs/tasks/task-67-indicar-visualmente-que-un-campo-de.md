---
type: task
id: task-67
title: Indicar visualmente que un campo de captura es numérico
state: open
date: 2026-08-06
owner: ai
parent: "[[task-41]]"
source: ["[[2026-08-06-temas-reunion-fer]]"]
---

# Indicar visualmente que un campo de captura es numérico

§7 de la reunión con Fernanda, `[13:34]`–`[14:14]`. Fernanda intentó escribir texto en un campo y no la dejó. Ricardo confirmó que el campo está definido como numérico, pero **nada lo indica visualmente**: no hay etiqueta ni los controles de incremento/decremento típicos de un `input type="number"`. La usuaria descubre la restricción al chocar con ella.

Salió en la captura de la información base (`nuxt/app/components/dashboard/survey/GeneralNumberInput.vue`), pero la decisión de cómo señalar un campo numérico conviene tomarla una sola vez y aplicarla a toda la captura, no solo a generales.

## Criterios de aceptación

- [ ] Un campo numérico se reconoce como tal antes de intentar escribir en él
- [ ] El criterio elegido se aplica de forma consistente en toda la captura, no solo en la información base
