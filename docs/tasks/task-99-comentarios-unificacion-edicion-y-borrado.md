---
type: task
id: task-99
title: "Comentarios: unificación, edición y borrado"
state: open
date: 2026-08-11
owner: ai
source: ["[[2026-08-11-auditoria-del-arbol-de-trabajo-y-reorganizacion]]"]
---

# Comentarios: unificación, edición y borrado

Raíz nueva para las tres tareas de comentarios que colgaban sueltas: [[task-69]] (unificar todos los lugares donde aparecen), [[task-70]] (editar y borrar los propios mientras el envío siga de tu lado) y [[task-71]] (editar y mover comentarios desde el admin de Django). Las tres salieron de la revisión con Fernanda del 6 de agosto y comparten superficie: el componente de comentarios del dashboard y el timeline de eventos de flujo.

No incluye [[task-97]]: aunque es de comentarios, es deuda de migración de datos y cuelga de [[task-1]].

## Criterios de aceptación

- [ ] Las tres hijas están cerradas o abandonadas
- [ ] Un comentario se ve, se edita y se borra con las mismas reglas en todas las superficies
