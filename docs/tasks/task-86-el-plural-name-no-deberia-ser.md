---
type: task
id: task-86
title: El plural_name no debería ser obligatorio en la definición de main_items
state: open
date: 2026-08-06
owner: ai
parent: "[[task-3]]"
source: ["[[2026-08-06-temas-reunion-fer]]"]
---

# El plural_name no debería ser obligatorio en la definición de main_items

§14 de la reunión con Fernanda, `[43:57]`–`[49:43]`. Deuda técnica de esquema que Ricardo dictó al final: en la definición de los «main items» del dashboard, `plural_name` es obligatorio y no debería serlo — tendría que tomarse por defecto de la definición ya existente del modelo, igual que el icono y el color, que ya pueden declararse desde los esquemas.

En la llamada lo nombró como «dashboard.pu»; el archivo real es `nuxt/app/layouts/dashboard.vue`, donde se declaran `main_items`. El origen del dato está en los `CatalogSchema` del backend (`name` / `plural_name`) — ver el skill `manage-collections`. Encaja en la deuda del motor schema-driven de [[task-3]]: menos declaración duplicada entre el esquema y el menú.

## Criterios de aceptación

- [ ] Un `main_item` sin `plural_name` toma el del esquema del modelo
- [ ] Los `main_items` que hoy lo declaran siguen funcionando igual
