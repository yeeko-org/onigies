---
type: task
id: task-85
title: Auto-cargar los envíos y las buenas prácticas al abrir una institución
state: open
date: 2026-08-06
owner: ai
parent: "[[task-3]]"
source: ["[[2026-08-06-temas-reunion-fer]]"]
---

# Auto-cargar los envíos y las buenas prácticas al abrir una institución

§14 de la reunión con Fernanda, `[43:57]`–`[49:43]`. Al abrir una institución, los envíos de buenas prácticas y las buenas prácticas deberían aparecer solos, sin que la revisora tenga que ir a buscarlos: «desde el get deben salir».

Toca las dos capas: que el serializer de `Institution` traiga los objetos relacionados (ver skill `manage-collections` para el contrato del catálogo y de las colecciones hijas) y que `nuxt/app/components/dashboard/ies/institution/InstitutionSheet.vue` los despliegue de entrada. El mecanismo de listas de objetos relacionados está descrito en el skill `dashboard-collections`.

## Criterios de aceptación

- [ ] Al abrir una institución se ven sus envíos de buenas prácticas sin acción adicional
- [ ] Se ven también las buenas prácticas
- [ ] No se dispara una petición por cada objeto
