---
type: task
id: task-189
title: Tests de regresión de la audiencia revisora sin is_staff
state: open
date: 2026-09-28
owner: ai
parent: "[[task-166]]"
related: ["[[2026-09-28-revisoras-sin-is-staff-en-generales]]"]
---

# Tests de regresión de la audiencia revisora sin is_staff

Acordado con Ricardo el 2026-09-28 para el día siguiente. El bug de las revisoras sin `is_staff` se escapó porque el único usuario del dashboard en los mocks e2e (`mockStaffUser`) trae `is_staff: true`. Ambos tests deben morder: revertir `GeneralGroupList` a `authStore.is_staff`, verlos fallar, restaurar.

## Criterios de aceptación

- [ ] Vitest: `flowRoleOf` con `reviewer: true, is_staff: false` da `reviewer` (y el getter `is_reviewer` del store)
- [ ] Mock e2e de revisora sin `is_staff` en `e2e/mocks/auth.ts`
- [ ] E2E: esa revisora ve `FlowStatusActions` en «Información base» con el paquete enviado, y no el formulario de la IES
- [ ] Ambos probados contra la reversión del arreglo
- [ ] `nuxt/TESTING.md` actualizado
