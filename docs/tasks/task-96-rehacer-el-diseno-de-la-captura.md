---
type: task
id: task-96
title: Rehacer el diseño de la captura numérica y los panels de Generales
state: open
date: 2026-08-09
owner: ai
parent: "[[task-41]]"
source: ["[[2026-08-09-sesion-task-93-y-drift-del-harness]]"]
related: ["[[task-67]]"]
---

# Rehacer el diseño de la captura numérica y los panels de Generales

La primera implementación del rediseño ([[task-67]] y decisiones de [[task-93]]) quedó funcional pero visualmente mala a juicio de Ricardo; se conserva sin revertir y se rehace aquí. Estado que hereda esta task: alias VCountInput en vuetify.ts (defaults: entero, min 0, sin spinners, outlined; inputmode va por uso porque los defaults de Vuetify solo proxean props declaradas); GeneralNumberQuestion.vue (ex GeneralNumberInput) con pregunta a la izquierda e input a la derecha; celdas de GeneralAuthorities y GeneralPopulations con el alias directo y aria-label por celda; panels de Generales sin accordion, con franja unificada gris (grey-darken-3 / fondo grey-lighten-5, orden de Ricardo tras descartar un color por grupo) y FlowComments movido del título a la fila superior derecha del cuerpo junto a FlowStatusActions (solo revisión). Pendientes concretos: el input declara width="200" pero renderiza gigante y desigual — diagnosticar; el suffix de unidad (instancias/planes, seed en api/question/seed_data/catalogs.py) es invisible en campo vacío sin foco y Ricardo esperaba un label visible; el ícono se probó con 123 (descartado por Ricardo) y quedó cambiado a tag (#), vivo en los defaults de VCountInput y pendiente de su veredicto visual — la señal del campo numérico sigue sin resolverse; las celdas de poblaciones conservan 110px; task-67 aún nombra GeneralNumberInput en su prosa.

## Criterios de aceptación

- [ ] Diagnosticado por qué width="200" no se respeta en render (inputs desiguales y enormes)
- [ ] La unidad es visible sin foco ni valor (el suffix de Vuetify solo pinta con foco o valor; revisitar label visible)
- [ ] Elegida y aprobada por Ricardo la señal visual del campo numérico (123 ya se probó y se descartó; tag (#) está aplicado y sin veredicto)
- [ ] Diseño de panels y captura aprobado visualmente por Ricardo
