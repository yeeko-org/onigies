---
type: task
id: task-146
title: Destino del documento de diseño del editor de observable y de las capturas de humo bajo nuxt/.claude
state: abandoned
date: 2026-09-10
owner: ai
parent: "[[task-3]]"
source: ["[[2026-09-10-editor-por-bloques-cuestionario-abierto-y-retiro-del-seed]]"]
---

# Destino del documento de diseño del editor de observable y de las capturas de humo bajo nuxt/.claude

`diseno-editor-observable.md`, bajo la carpeta `.claude` de nuxt (589 líneas, el diseño final del editor con sus porqués, escrito por el ejecutor de `ux-designer` para el ejecutor del frontend) y `nuxt/.claude/smoke/*.png` quedaron fuera del commit del 10 de septiembre. El propio documento dice que se borra una vez construido y validado el editor, y que lo que sobreviva se mueve a un skill. Decidir qué porqués merecen vivir en `dashboard-collections` (o en un skill propio del editor de observable, al estilo de `bp-validation-ux`) y borrar el resto.

## Criterios de aceptación

- [ ] Los porqués que sobreviven están en un skill
- [ ] El documento y las capturas borrados o ignorados por git

## Cierre (2026-09-22)

Ricardo autorizó borrar la carpeta `.claude` de nuxt completa (el documento de diseño y las capturas) en el cierre de la sesión del 22 de septiembre, con el editor validado y en producción desde el 10 ([[task-131]]). Los porqués no se extrajeron a ningún skill: se abandona ese criterio a sabiendas; el documento sigue en la historia de git de la sesión que lo produjo si alguien lo necesita. Record [[2026-09-22-cierre-cuestionario-principal-captura-y-borrado]].
