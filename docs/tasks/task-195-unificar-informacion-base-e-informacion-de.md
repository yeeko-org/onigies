---
type: task
id: task-195
title: Unificar «Información base» e «Información de base» en la UI
state: open
date: 2026-10-02
owner: ricardo
source: ["[[2026-10-02-comentarios-editables-y-valvula-de-admin]]"]
---

# Unificar «Información base» e «Información de base» en la UI

La pestaña y los enlaces dicen «Información base» (`GeneralGroupList.vue`, `CpAxisCapture.vue`, `CpGroupCard.vue`); los tooltips y docstrings de `ObservableHeader`, `ObservableEditSimple` y `GeneralGroupEditSimple` dicen «Información de base», igual que la skill `gen-general-info` y el CLAUDE.md del monorepo. La advertencia nueva del diálogo de admin usó «Información base» por seguir la pestaña. Hay que elegir una forma (es wording de UI: Ricardo o Rubén) y aplicarla en todas las superficies y en la skill.

## Criterios de aceptación

- [ ] Una sola forma en componentes, skills y CLAUDE.md
- [ ] Decidida por Ricardo
