---
type: task
id: task-39
title: Migrar la documentación de onigies al esquema documenter
state: closed
date: 2026-08-03
owner: ai
---

# Migrar la documentación de onigies al esquema documenter

Migración del `docs/` heredado (planes, históricos, actas, instrumento) al esquema de cinco tipos del skill `documenter`, con triage de pendientes. Contexto y detalle en la bitácora hija. El plan global del rediseño es [[global:task-2]]; onigies no estaba en sus cuatro repos, se sumó como quinto.

## Criterios de aceptación

- [ ] Los documentos existentes están clasificados en los cinco tipos, sin carpetas viejas
- [ ] Los pendientes dispersos son tasks con dueño y criterios
- [ ] El validador corre en verde y el hook está instalado
