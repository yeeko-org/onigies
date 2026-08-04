---
type: task
id: task-40
title: Levantar el TESTING.md del monorepo
state: closed
date: 2026-08-03
owner: ai
---

# Levantar el TESTING.md del monorepo

El repo no tiene `TESTING.md` en ningún nivel, y la regla de testing pide uno por proyecto con los niveles montados, los comandos, las credenciales de prueba y los flujos e2e cubiertos como títulos breves, referenciado desde el `CLAUDE.md`.

Insumos que ya existen: `api/flow/tests.py` (pruebas de permisos por institución y de notificaciones por cambio de turno), el resto de `pytest` del API, y los e2e de Nuxt con backend mockeado (skill `playwright-e2e`). Sesión aparte: conviene leer lo que hay antes de escribir, y de paso queda claro qué niveles están realmente montados y cuáles no.

## Criterios de aceptación

- [ ] Existe `TESTING.md` con niveles, comandos, credenciales y flujos e2e cubiertos
- [ ] `CLAUDE.md` lo referencia
