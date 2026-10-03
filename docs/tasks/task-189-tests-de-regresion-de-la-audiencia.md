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

## Avance del 2026-10-02

Los Vitest de store ya existen: `nuxt/tests/unit/flow_store.test.js` cubre `is_admin` (superuser, staff, revisora sin staff, IES), `isAdminEvent`, `getAdminTargets`, `canEditComment`/`eventSide` y `getAdminRootBlock`, con el helper de Pinia en `tests/unit/helpers/` y el alias de `pinia` en `vitest.config.ts`. Sigue pendiente el e2e: mock de revisora sin `is_staff` y un `mockAdminUser` (`is_staff: true`) para el diálogo de la válvula ([[task-190]]): el admin ve el botón, abre el diálogo, «Aplicar» deshabilitado sin motivo, aplica y ve la marca; la revisora sin staff no lo ve; con el paquete en borrador el botón está bloqueado. El worktree no tiene `.env.test` ni los `.pem` de localhost, así que se corre desde el checkout principal.

## Criterios de aceptación

- [ ] Vitest: `flowRoleOf` con `reviewer: true, is_staff: false` da `reviewer` (y el getter `is_reviewer` del store); `is_admin` ya cubierto
- [ ] E2E del diálogo de la válvula con `mockAdminUser`, y la revisora sin staff no ve el botón
- [ ] Mock e2e de revisora sin `is_staff` en `e2e/mocks/auth.ts`
- [ ] E2E: esa revisora ve `FlowStatusActions` en «Información base» con el paquete enviado, y no el formulario de la IES
- [ ] Ambos probados contra la reversión del arreglo
- [ ] `nuxt/TESTING.md` actualizado
