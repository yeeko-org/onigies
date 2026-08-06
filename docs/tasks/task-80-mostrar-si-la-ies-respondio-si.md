---
type: task
id: task-80
title: Mostrar si la IES respondió sí o no a reportar buenas prácticas
state: open
date: 2026-08-06
owner: ai
parent: "[[task-6]]"
source: ["[[2026-08-06-temas-reunion-fer]]"]
---

# Mostrar si la IES respondió sí o no a reportar buenas prácticas

§12 de la reunión con Fernanda, `[29:43]`–`[34:37]`. La IES responde primero si tiene o quiere reportar buenas prácticas, y esa respuesta **no se ve en ningún lado**: ni en el header del envío ni en el detalle del paquete. Ricardo lo dijo así en la llamada: no tiene sentido que el dato que gobierna toda la sección sea el único invisible. Sin él, un envío vacío es indistinguible de un envío no empezado.

El dato existe: `GoodPracticePackage.has_good_practices` en `api/example/models.py`. Falta exponerlo y presentarlo en `nuxt/app/components/dashboard/example/good_practice_package/GoodPracticePackageHeader.vue` y `GoodPracticePackageEditSimple.vue`.

## Criterios de aceptación

- [ ] El header del envío indica si la IES respondió que sí o que no
- [ ] El detalle del paquete muestra la misma respuesta
- [ ] Un «no» se distingue de un envío sin responder
