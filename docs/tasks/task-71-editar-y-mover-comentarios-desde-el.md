---
type: task
id: task-71
title: Editar y mover comentarios desde el admin de Django
state: open
date: 2026-08-06
owner: ai
source: ["[[2026-08-06-temas-reunion-fer]]"]
---

# Editar y mover comentarios desde el admin de Django

§10 de la reunión con Fernanda, `[17:20]`–`[24:33]`. Ricardo propuso en la llamada agregar desde el admin —edición directa de base de datos, «menos bonita» pero funcional— la posibilidad de editar y **mover** comentarios mal ubicados, para corregir casos como el de Fernanda, que metió un comentario general en la buena práctica equivocada en vez de a nivel de envío. Lo planteó como algo que podría agregar al día siguiente.

Es la válvula de escape administrativa, complementaria de la edición en la interfaz normal: aquella la gobierna la regla de turno, esta no. Superficie: el admin de `api/flow/admin.py`.

## Criterios de aceptación

- [ ] Desde el admin se puede editar el texto de un comentario
- [ ] Desde el admin se puede reasignar un comentario al objeto correcto (envío, buena práctica o criterio)
