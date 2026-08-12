---
type: task
id: task-83
title: Estatus del último año activo en el header de instituciones
state: open
date: 2026-08-06
owner: ai
parent: "[[task-84]]"
source: ["[[2026-08-06-temas-reunion-fer]]"]
related: ["[[task-82]]", "[[task-84]]"]
---

# Estatus del último año activo en el header de instituciones

§14 de la reunión con Fernanda, `[43:57]`–`[49:43]`. Ricardo pidió que en el header de una institución aparecieran los estatus, o los años registrados con el estatus de cada uno, y en la llamada lo dejó en «hay que pensarlo bien». **Lo definió después (2026-08-06):** el header muestra **los estatus del último año activo**.

**Qué es el último año activo:** el año cuyo `Period.results_published` sea falso; si todos están publicados, el último año. `Period` vive en `api/ies/models.py` y `results_published` ya existe, reservado para la futura página pública de resultados — ver [[adr-0009]], que decidió no absorberlo para otros usos.

Archivos: `nuxt/app/components/dashboard/ies/institution/InstitutionHeader.vue` y `InstitutionCard.vue`. La parte del rediseño que **no** quedó definida —cómo se ve el conjunto, si se parece a la tarjeta de año de la vista IES, qué pasa con los demás años— es [[task-84]].

## Criterios de aceptación

- [ ] El header de una institución muestra los estatus del último año activo
- [ ] «Último año activo» se resuelve como el año con `results_published` falso, o el último si todos están publicados
