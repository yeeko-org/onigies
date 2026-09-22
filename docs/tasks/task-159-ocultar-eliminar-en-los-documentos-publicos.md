---
type: task
id: task-159
title: Ocultar «Eliminar» en los documentos públicos generados desde la base
state: open
date: 2026-09-22
owner: ricardo
parent: "[[task-151]]"
---

# Ocultar «Eliminar» en los documentos públicos generados desde la base

El API rechaza borrar un `PublicDocument` con generador (400 con mensaje), pero el dashboard sigue mostrando el botón «Eliminar» en su detalle, porque `EditCommon.vue` lo muestra para toda colección primaria y no tiene un gancho por registro. Opciones: (a) dejarlo así, el guardián del API basta; (b) prop genérica `hide_delete` o predicado por registro en `EditCommon`, pasado desde `PanelCommon`; (c) exponer un selector de generador en el editor para poder recrearlo. Surgió el 2026-09-22 en [[task-150]].

## Criterios de aceptación

- [ ] Decidido si el botón se oculta o se deja con el rechazo del API
