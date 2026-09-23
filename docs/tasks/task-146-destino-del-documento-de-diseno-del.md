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

Ricardo autorizó borrar la carpeta `.claude` de nuxt completa (el documento de diseño y las capturas) en el cierre de la sesión del 22 de septiembre, con el editor validado y en producción desde el 10 ([[task-131]]). Los porqués no se extrajeron a ningún skill: el borrado se autorizó sin que se le nombrara a Ricardo este criterio abierto («los porqués sobreviven en un skill»), así que el abandono no fue a sabiendas suyo. El archivo nunca fue rastreado por git; la única fuente que queda es el log de sesión `~/.claude/projects/-home-rick-dev-unam-onigies/d5ef9c1e-a1fa-4557-975b-341682832e18/subagents/agent-a6350c73576d152a9.jsonl`, con el Write de 50 508 caracteres del 2026-09-10T23:29:44Z (las ediciones posteriores pueden faltar). Record [[2026-09-22-cierre-cuestionario-principal-captura-y-borrado]].
