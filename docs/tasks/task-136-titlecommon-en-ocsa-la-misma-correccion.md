---
type: task
id: task-136
title: "TitleCommon en ocsa: la misma corrección de white-space aplicada sin commitear"
state: open
date: 2026-09-07
owner: ricardo
source: ["[[2026-09-07-rediseno-edicion-observables-pesos-y-nomenclatura]]"]
---

# TitleCommon en ocsa: la misma corrección de white-space aplicada sin commitear

El 7 de septiembre se detectó en onigies que `TitleCommon` nunca partía el título en dos líneas fuera de Chrome: Vuetify pone `white-space: nowrap` en el título y el componente lo contrarrestaba solo con `text-wrap: pretty`, que Firefox ignora. Se agregó `white-space: normal`. El bug nació en ocsa (`4fe838d`, 2024-10-01) y onigies lo heredó en el port de marzo de 2026. La misma línea se aplicó en `~/dev/ibero/ocsa/nuxt/components/dashboard/common/utils/TitleCommon.vue`, sin commitear, sobre la rama `mapa-movil` que tiene trabajo ajeno en curso. Ocsa además tiene tres headers (`ArticleHeader`, `NoteHeader`, `ProjectHeader`) que suben la fila a 70/74 px como parche.

La parte de onigies quedó hecha en la misma sesión (`nuxt/app/components/dashboard/common/utils/TitleCommon.vue`). El trabajo pendiente vive en el árbol documenter de ocsa (su task de TitleCommon, 2026-09-07); esta task se cierra aquí para no duplicar el ciclo.

## Criterios de aceptación

- [ ] El cambio en ocsa está commiteado en la rama que corresponda
- [ ] Verificado en Firefox que los títulos largos parten en dos líneas

**2026-09-07, tras el critic:** reabierta. El cambio está aplicado pero sin commitear en ocsa (rama `mapa-movil`, junto con trabajo previo de Ricardo); cierra cuando ocsa lo commitee, que es la task-104 de su árbol.
