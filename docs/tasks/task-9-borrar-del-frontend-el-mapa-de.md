---
type: task
id: task-9
title: Borrar del frontend el mapa de status viejo
state: open
date: 2026-08-03
owner: ai
parent: "[[task-1]]"
source: ["[[2026-06-23-progreso-frontend-del-flujo]]", "[[2026-06-19-recomendaciones-del-dashboard]]"]
---

# Borrar del frontend el mapa de status viejo

`composables/filters.js` y `fetch.js` siguen refiriendo `status_sending`/`status_register` para los paneles de filtros, y `status_filters` está hardcodeado en el front (recomendación 9 de la auditoría del dashboard). `HeaderCommon` bifurca entre el motor nuevo y los `status_groups` viejos: mientras coexistan hay dos modelos mentales de estado. El backend debe entregar la metadata de status y el front consumirla.

## Criterios de aceptación

- [ ] `status_filters` ya no vive hardcodeado en el frontend
- [ ] `HeaderCommon` tiene un solo camino de estado
