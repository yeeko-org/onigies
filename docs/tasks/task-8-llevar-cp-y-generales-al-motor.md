---
type: task
id: task-8
title: Llevar CP y generales al motor de flujo en el frontend
state: closed
date: 2026-08-03
owner: ai
parent: "[[task-1]]"
source: ["[[2026-06-23-progreso-frontend-del-flujo]]"]
---

# Llevar CP y generales al motor de flujo en el frontend

`FlowStatusActions`, `FlowStatusChip` y `FlowComments` son genéricos y ya sirven; falta incorporarlos a las páginas de respuesta del cuestionario principal y de generales, y a su revisión en el dashboard. Buenas prácticas es el modelo a seguir (skill `bp-validation-ux`).

**Acotada a CP (2026-08-06):** la sesión de generales del 2026-08-04 dejó `gen` corriendo entero sobre el motor (captura de la IES, revisión, envío gateado), verificado en la sesión duo ([[2026-08-06-sesion-duo-adjuntos-sobre-flow-y]]). Lo que queda de esta task es únicamente el cuestionario principal (cp), ligado a la superficie de [[task-42]].

**2026-09-07:** los rótulos de los bloques de la captura cp leen `public_name` de `cats.question_type` (composable `useQuestionTypes`), nunca hardcodeados ([[adr-0014]] §2). Instrucción de Ricardo: «hay que conectar QuestionType al dashboard y en su momento a `/respuestas` (cuando se haga esa tarea)».

## Criterios de aceptación

- [x] La IES opera CP por transiciones del motor, sin status hardcodeados (generales 2026-08-04; cp 2026-09-22, commit 0a6a214)
- [x] La revisora revisa CP desde el dashboard con chip, transiciones y comentarios (2026-09-22, commit 2166ad3)

**2026-09-22 (desde [[task-150]]):** cuando la captura cp muestre el observable 1.7 a la IES, debe llevar la nota cruzada «Las cifras de composición por sexo-género de autoridades y poblaciones que evalúa este observable se capturan en los apartados «Poblaciones» y «Autoridades» de la sección Información de base.» (así la imprime el Word, con los grupos en el orden de la base; Ricardo aceptó ese orden frente a su redacción aprobada, que llevaba «Autoridades» primero; los nombres de apartado salen de los `GeneralGroup` con `is_population`). Y propuesta pendiente de Ricardo: el campo nuevo `Observable.note` (notas del instrumento en 1.2, 1.3 y 3.1) hoy solo se ve en el Word y en el editor del dashboard; la pantalla de captura de la IES todavía no lo muestra.


## Hecho el 2026-09-22

Captura de la IES en `/respuestas` (`nuxt/app/components/dashboard/answer/capture/`) y revisión en el dashboard (colección «Ejes del cuestionario» y sección «Cuestionario principal» del survey), ambas sobre el motor y decidiendo por `role`/`content_editable`/`priority`, nunca por nombre. La nota cruzada del 1.7 se resolvió con la tarjeta del grupo `population`, que remite a Información de base con link; el 1.7 no tiene `Observable.note` en producción. `Observable.note` (1.2, 1.3, 3.1) sí se muestra bajo la pregunta inicial en la captura. Decisiones de diseño en [[adr-0017]], [[adr-0018]] y [[adr-0019]]; record [[2026-09-22-cierre-cuestionario-principal-captura-y-borrado]]. Pendiente solo el deploy ([[task-163]]).
