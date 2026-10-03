---
type: task
id: task-194
title: El hint de «Completada» sigue diciendo «en espera de que se envíe el paquete» cuando ya se envió
state: open
date: 2026-10-02
owner: ricardo
source: ["[[2026-10-02-comentarios-editables-y-valvula-de-admin]]"]
related: ["[[task-190]]"]
---

# El hint de «Completada» sigue diciendo «en espera de que se envíe el paquete» cuando ya se envió

Visto en la pasada en navegador del 2026-10-02: con el paquete de buenas prácticas ya en revisión, el hint del status `bp_completed` sigue leyendo «en espera de que se envíe el paquete para revisarla». Es texto de la seed de `flow`, bajo el candado de `seeded_at` (los textos se editan en el admin, no se re-siembran), así que corregirlo es de Rubén o de Ricardo en el admin; si se quiere un hint distinto según el estado del paquete, eso sí es cambio de código.

## Criterios de aceptación

- [ ] Decidido si basta reescribir el hint en el admin o si el hint depende del estado de la raíz
- [ ] Texto corregido en producción
