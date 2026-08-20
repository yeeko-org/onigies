---
type: task
id: task-61
title: Montar Vitest en nuxt y cubrir la lógica pura de secciones
state: open
date: 2026-08-04
owner: ai
source: ["[[task-53]]"]
---

# Montar Vitest en nuxt y cubrir la lógica pura de secciones

Al escribir los tests de [[task-53]] quedó sin cubrir la lógica pura de `nuxt/app/utils/sections.js` porque Vitest no está montado en el repo (no hay dependencia ni config; los únicos tests de nuxt son los e2e de Playwright). El e2e existente de tabs corre con una IES `is_test: true`, así que **nadie verifica el caso de la IES real** — que solo vea las secciones publicadas y que un deep-link a una sección interna caiga en la primera publicada — que es justo la regla que se despliega. Ricardo aprobó dejar esto como tarea: montar Vitest es una dependencia nueva y merece su propia sesión corta. Alternativa descartada por ahora: un cuarto e2e con fixture de IES real (sin dependencias, pero cobertura más cara de mantener para lógica pura).

## Raíz del bloque de testing (2026-08-11)

Además de su propio alcance, esta task encabeza el mini-bloque de testing del monorepo. Su hija es [[task-94]], los tests de regresión del stack de adjuntos sobre flow: Ricardo confirmó que sí se hacen, así que deja de ser una propuesta suelta.

Las dos se agrupan porque comparten la misma dependencia y el mismo destino documental — la parte de frontend de [[task-94]] espera precisamente a que Vitest exista, y las dos actualizan el `TESTING.md` que las cubre.

## Estado (19-ago-2026)

Sus cuatro criterios están cumplidos y comiteados, y su otra hija [[task-121]] quedó cerrada. **No se cierra porque [[task-94]] sigue abierta**, y esa espera a que Ricardo acote la lista de tests propuesta — cerrar el padre en `--recursive` la arrastraría de refilón. Queda abierta solo como raíz del bloque de testing: en cuanto task-94 se resuelva (o se reasigne a otro padre), esta se cierra sin más trabajo.

## Criterios de aceptación

- [x] Vitest configurado en nuxt/ (dependencia aprobada por Ricardo en la sesión de task-53)
- [x] Test unitario de utils/sections.js: sectionOfTab (axis-{id} → cp, valores inválidos → null) y visibleSections/isSectionVisible para IES real y de prueba
- [x] Cubierto el caso de la IES real: solo ve bp y un ?tab=base cae en la primera sección publicada
- [x] TESTING.md de nuxt actualizado con el nivel unitario
