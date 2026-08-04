---
type: task
id: task-44
title: Los comentarios por criterio no se bloquean cuando la práctica está del lado de la IES
state: open
date: 2026-08-03
owner: ai
parent: "[[task-6]]"
source: ["[[2026-07-28-reunion-flujo-bp-e-informacion-base]]"]
---

# Los comentarios por criterio no se bloquean cuando la práctica está del lado de la IES

Bug detectado en vivo durante la demo. Cuando el paquete se devuelve a la IES, la revisora deja de poder editar y comentar a nivel de buena práctica, pero los comentarios a nivel de criterio siguen abiertos. `[14:43]` «los comentarios no están bloqueados, pero está bueno que me dé cuenta que los comentarios no están bloqueados, para que los bloquee también; o sea, los comentarios a nivel de buena práctica sí, pero no los comentarios a nivel de cada criterio».

Evidencia en el código: en `nuxt/app/components/dashboard/example/good_practice/FeatureItem.vue` el componente `Comments` con `collection_name="feature_good_practice"` se monta dentro del bloque `v-if="isStaff"` sin ninguna referencia a la prop `editable`. Esa misma prop sí gatea el resto de los controles del componente: la casilla de la característica, el textarea de justificación y el slider de calificación.

El arreglo es propagar `editable` al bloque de comentarios, igual que a los demás controles.

## Criterios de aceptación

- [ ] Con la práctica del lado de la IES, la revisora no puede comentar a nivel de criterio
- [ ] El historial de comentarios sigue visible en solo lectura
- [ ] Los comentarios a nivel de buena práctica y de paquete siguen funcionando como hoy
