---
type: task
id: task-123
title: Implementación completa de is_public en adjuntos
state: open
date: 2026-08-13
owner: ai
related: ["[[adr-0013]]"]
---

# Implementación completa de is_public en adjuntos

El backend ya funciona: `Attachment.is_public` (default `False`) y el endpoint de descarga con `AllowAny` que responde 302 también a anónimos cuando el flag es verdadero. Falta la capa de producto, pensada para la futura plataforma pública: UI de edición del flag en el dashboard, y decidir qué ContentTypes o tipos de archivo pueden marcarse públicos (decisión de Ricardo). No urgente, opcional: nada en el sistema actual depende de esto.

## Criterios de aceptación

- [ ] Decidido con Ricardo qué ContentTypes/tipos de archivo admiten is_public
- [ ] UI para editar el flag en las superficies que se decidan
- [ ] Tests del flujo público end-to-end
