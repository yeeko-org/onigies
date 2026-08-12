---
type: task
id: task-49
title: Conteo de buenas prácticas del último año en la lista de instituciones
state: open
date: 2026-08-03
owner: ai
parent: "[[task-6]]"
source: ["[[2026-07-28-reunion-flujo-bp-e-informacion-base]]"]
---

# Conteo de buenas prácticas del último año en la lista de instituciones

`[06:02]` «como la lista de instituciones, qué bueno que me estoy dando cuenta que lo voy a poner como en el giro también, como si ya tiene buenas prácticas y cuántas y así del último año al menos».

Sirve para el seguimiento de campo de Rubí y las revisoras: saber de un vistazo qué instituciones ya enviaron algo. Estado actual: `InstitutionSchema` en `api/ies/catalog_schema.py` no expone ningún conteo. El procedimiento para tocar el esquema de catálogo está en el skill `manage-collections`.

**Hermana en el header del envío (2026-08-06):** [[task-79]] pide lo mismo con más grano —conteo por estatus, cada uno con su icono— en el header del envío de buenas prácticas. Comparten el trabajo de agregación en el serializer; conviene resolverlas juntas.

## Criterios de aceptación

- [ ] La lista de instituciones indica si la institución tiene buenas prácticas en el periodo vigente
- [ ] Muestra cuántas
