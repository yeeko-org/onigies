---
type: task
id: task-63
title: Filtro por defecto «todas» en la lista de invitaciones
state: open
date: 2026-08-06
owner: ai
parent: "[[task-3]]"
source: ["[[2026-08-06-temas-reunion-fer]]"]
---

# Filtro por defecto «todas» en la lista de invitaciones

§3 de la reunión con Fernanda, `[03:43]`–`[10:04]`. Al revisar los usuarios de una institución (ejemplo con «SEP»), la lista de invitaciones abre filtrada en «pendientes» y las cuentas ya vinculadas quedan escondidas; Ricardo indicó en la llamada que el default debería ser «todas».

Ubicación exacta: `nuxt/app/components/dashboard/common/InvitationList.vue`, `const filter = ref('pending')`; las opciones del filtro (`pending`, `linked`, `all`) están declaradas unas líneas arriba en el mismo archivo. Es un cambio de una línea, pero conviene revisar de paso que el contador que acompaña al filtro siga leyéndose bien con el default nuevo.

## Criterios de aceptación

- [ ] La lista de invitaciones de una institución abre mostrando todas
- [ ] Los filtros «pendientes» y «vinculadas» siguen disponibles
