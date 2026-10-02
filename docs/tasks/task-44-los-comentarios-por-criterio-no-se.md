---
type: task
id: task-44
title: Los comentarios por criterio no se bloquean cuando la práctica está del lado de la IES
state: open
date: 2026-08-03
owner: ai
parent: "[[task-6]]"
source: ["[[2026-07-28-reunion-flujo-bp-e-informacion-base]]"]
related: ["[[task-70]]"]
---

# Los comentarios por criterio no se bloquean cuando la práctica está del lado de la IES

Bug detectado en vivo durante la demo. Cuando el paquete se devuelve a la IES, la revisora deja de poder editar y comentar a nivel de buena práctica, pero los comentarios a nivel de criterio siguen abiertos. `[14:43]` «los comentarios no están bloqueados, pero está bueno que me dé cuenta que los comentarios no están bloqueados, para que los bloquee también; o sea, los comentarios a nivel de buena práctica sí, pero no los comentarios a nivel de cada criterio».

Evidencia en el código: en `nuxt/app/components/dashboard/example/good_practice/FeatureItem.vue` el componente `Comments` con `collection_name="feature_good_practice"` se monta dentro del bloque `v-if="isStaff"` sin ninguna referencia a la prop `editable`. Esa misma prop sí gatea el resto de los controles del componente: la casilla de la característica, el textarea de justificación y el slider de calificación.

El arreglo es propagar `editable` al bloque de comentarios, igual que a los demás controles.

## Alcance ampliado (2026-08-06, revisión con Fernanda)

La revisión del 6 de agosto ([[2026-08-06-temas-reunion-fer]], §10 `[17:20]`–`[24:33]`) mostró que el hueco no es solo el criterio de una buena práctica. Fernanda confirmó el comportamiento esperado —una vez que el envío ya no está de tu lado, no deberías poder seguir comentando— y Ricardo confirmó que la regla debe propagarse hacia abajo, no quedarse en la raíz.

**Ricardo amplió el alcance de esta task a hijos y nietos, en los tres flujos: `cp`, `gen` y `bp`.** O sea: el bloqueo por turno debe recorrer toda la jerarquía de cada grupo de flujo, no solo el par paquete→buena práctica→criterio de `bp`. El motor es el mismo en los tres (ver skill `flow`), así que la mecánica del arreglo también debería serlo: el gate de turno que hoy vive en la raíz tiene que llegar a cada nivel anidado que monte comentarios.

## Nota del 2026-10-02

Ricardo decidió que el campo `comments` de los criterios sigue la misma regla de turno por raíz que los comentarios del timeline: editable por cualquier revisora mientras el envío de bp esté en rol `reviewer`, congelado cuando regresa a la IES ([[2026-10-02-comentarios-editables-y-valvula-de-admin]], P11). El candado del criterio se construye dentro de [[task-70]]; aquí queda lo que esa task no cubre: que el bloqueo por turno recorra hijos y nietos en `cp` y `gen` para los comentarios del timeline, que hoy se gatean por el status propio del objeto y no por la raíz.

## Criterios de aceptación

- [ ] Con la práctica del lado de la IES, la revisora no puede comentar a nivel de criterio
- [ ] El historial de comentarios sigue visible en solo lectura
- [ ] Los comentarios a nivel de buena práctica y de paquete siguen funcionando como hoy
- [ ] El bloqueo por turno alcanza hijos y nietos, no solo el primer nivel
- [ ] La regla aplica igual en los tres flujos: `cp`, `gen` y `bp`
