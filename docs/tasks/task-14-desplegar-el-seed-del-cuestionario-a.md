---
type: task
id: task-14
title: Desplegar el seed del cuestionario a producción
state: closed
date: 2026-08-03
owner: ricardo
parent: "[[task-2]]"
source: ["[[2026-07-29-commits-tematicos-y-deploy-flow]]", "[[2026-07-04-seed-del-cuestionario]]"]
---

# Desplegar el seed del cuestionario a producción

El código y el esquema del seed ya llegaron a producción con el fast-forward que resolvió el incidente del 500, pero `load_questionnaire` nunca se ha corrido allá. La ventana de despliegue depende de que el cliente resuelva los textos abiertos: sembrar antes obliga a re-sembrar después.

**2026-08-12**: el seed volvió a correr en producción con el modelo nuevo de preguntas base ([[2026-08-12-deploy-gen-a-produccion-migraciones-seeds]]): 41 observables actualizados, 5 grupos generales y 7 GeneralQuestions. El criterio pendiente sigue igual: los textos definitivos dependen de Rubén, y con «textos solo al crear» sus futuras correcciones se aplican vía catálogo, no por re-seed.

**2026-09-07**: llegó la versión maquetada y final del instrumento, y el cotejo ([[2026-09-07-cotejo-del-instrumento-maquetado]]) confirmó que es textualmente equivalente al original ya sembrado. Lo que estaba sembrado en producción *era* el instrumento definitivo; el segundo criterio se cumple sin re-seed. Lo que sigue abierto del instrumento son decisiones de redacción de la CIGU, que ya no bajan por esta task sino por [[task-16]], [[task-17]] y [[task-50]].

## Criterios de aceptación

- [x] `load_questionnaire` corrió en producción
- [x] Los ejes, componentes y observables visibles corresponden al instrumento definitivo (2026-09-07)
