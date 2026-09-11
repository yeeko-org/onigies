---
type: task
id: task-146
title: Destino del documento de diseño del editor de observable y de las capturas de humo bajo nuxt/.claude
state: open
date: 2026-09-10
owner: ai
parent: "[[task-3]]"
source: ["[[2026-09-10-editor-por-bloques-cuestionario-abierto-y-retiro-del-seed]]"]
---

# Destino del documento de diseño del editor de observable y de las capturas de humo bajo nuxt/.claude

`nuxt/.claude/diseno-editor-observable.md` (589 líneas, el diseño final del editor con sus porqués, escrito por el ejecutor de `ux-designer` para el ejecutor del frontend) y `nuxt/.claude/smoke/*.png` quedaron fuera del commit del 10 de septiembre. El propio documento dice que se borra una vez construido y validado el editor, y que lo que sobreviva se mueve a un skill. Decidir qué porqués merecen vivir en `dashboard-collections` (o en un skill propio del editor de observable, al estilo de `bp-validation-ux`) y borrar el resto.

## Criterios de aceptación

- [ ] Los porqués que sobreviven están en un skill
- [ ] El documento y las capturas borrados o ignorados por git
