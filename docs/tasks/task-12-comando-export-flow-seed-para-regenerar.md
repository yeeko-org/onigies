---
type: task
id: task-12
title: Comando export_flow_seed para regenerar el seed desde la base
state: open
date: 2026-08-03
owner: ai
parent: "[[task-1]]"
source: ["[[2026-07-03-auditoria-y-mejoras-del-flujo]]"]
---

# Comando export_flow_seed para regenerar el seed desde la base

Sesión S6, marcada como opcional: un comando que regenere el bloque de datos del seed leyendo la base, para poder editar cómodo en el admin y commitear el resultado. Choca de frente con la política «el seed manda» (§6-f de la auditoría), así que antes de construirlo hay que decidir si sigue teniendo sentido.

## Criterios de aceptación

- [ ] El comando existe y su salida vuelve a producir el catálogo actual, o la task se abandona con la razón escrita
