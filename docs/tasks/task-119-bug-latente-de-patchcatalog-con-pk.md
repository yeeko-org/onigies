---
type: task
id: task-119
title: Bug latente de patchCatalog con PK de texto
state: open
date: 2026-08-12
owner: ai
parent: "[[task-3]]"
source: ["[[2026-08-12-sesion-orquestada-a-b-captura-correcta]]"]
related: ["[[task-108]]"]
---

# Bug latente de patchCatalog con PK de texto

Hallazgo del alta de los catálogos de [[task-108]]: `patchCatalog` en `nuxt/app/store/index.js` localiza el elemento con `findIndex(el => el.id === response.data.id)`. Para `GeneralGroup`, cuya PK es un slug (`forma_gobierno`) y no un `id`, ambos lados son `undefined`, así que el `findIndex` siempre «acierta» en el índice 0 y **mutaría el grupo equivocado** en `store.cats`.

Hoy no se dispara: los `EditSimple` de los catálogos nuevos guardan por `saveElement → saveCatalog`, que sí respeta `pk`. Se dispararía si alguien activa el modo reordenar de `PanelsResult` sobre la colección `general_group` (`PanelCommon.saveOrder`). Es genérico del store, no de la colección: cualquier catálogo futuro con PK de texto lo hereda.

## Criterios de aceptación

- [ ] `patchCatalog` localiza por la PK real de la colección, no por `id` a secas
- [ ] El modo reordenar sobre `general_group` no corrompe el store
