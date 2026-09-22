---
type: task
id: task-158
title: EditCommon muestra los errores de borrado como JSON crudo
state: open
date: 2026-09-22
owner: ricardo
parent: "[[task-150]]"
---

# EditCommon muestra los errores de borrado como JSON crudo

Propuesta surgida el 2026-09-22 al proteger del borrado los documentos generados ([[task-150]]): cuando el API rechaza un borrado, `EditCommon.vue` muestra «No se pudo eliminar el registro:» seguido del cuerpo JSON serializado, por ejemplo `{"detail":"Los documentos generados desde la base no se pueden eliminar."}`. Propuesta: mostrar `errors.detail` cuando exista, y el JSON solo como último recurso. Toca el marco genérico que usan todas las colecciones; por eso no se implementó sin decisión de Ricardo.

## Criterios de aceptación

- [ ] Decidido si se cambia el marco genérico
- [ ] Un rechazo de borrado con `detail` se lee en español, sin llaves ni comillas
