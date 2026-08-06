---
type: task
id: task-82
title: Nombre completo con tooltip en el header de instituciones
state: open
date: 2026-08-06
owner: ai
source: ["[[2026-08-06-temas-reunion-fer]]"]
related: ["[[task-43]]", "[[task-84]]"]
---

# Nombre completo con tooltip en el header de instituciones

§14 de la reunión con Fernanda, `[43:57]`–`[49:43]`. El header de una institución muestra solo las siglas. Ricardo pidió conservarlas visibles y agregar debajo el nombre completo, en tamaño más chico y con tooltip. Cree que ya existe una herramienta de `title` genérico reutilizable para esto — hay que ubicarla antes de escribir una nueva.

Archivos: `nuxt/app/components/dashboard/ies/institution/InstitutionHeader.vue` y `InstitutionCard.vue`.

Es el equivalente, para la institución, de lo que [[task-43]] hace en la tarjeta de buena práctica; mismo patrón, mismo criterio de diseño. El resto del rediseño del header —qué más va ahí y cómo se organiza— vive en [[task-83]] y [[task-84]].

## Criterios de aceptación

- [ ] El header conserva las siglas y muestra debajo el nombre completo en tamaño menor
- [ ] El nombre completo tiene tooltip
- [ ] Se reusó el helper de `title` existente si lo hay, en vez de duplicarlo
