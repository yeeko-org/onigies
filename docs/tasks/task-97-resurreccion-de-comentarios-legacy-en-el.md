---
type: task
id: task-97
title: Resurrección de comentarios legacy en el re-run de migrate_flow_data
state: open
date: 2026-08-09
owner: ai
source: ["[[2026-08-09-sesion-task-93-y-drift-del-harness]]"]
related: ["[[task-7]]", "[[adr-0010]]"]
---

# Resurrección de comentarios legacy en el re-run de migrate_flow_data

Mismo bug que la resurrección de adjuntos resuelta el 2026-08-09, pero en la rama de comentarios: _create_event usa get_or_create sobre las filas legacy vivas (ObservableComment, GroupComment, GeneralGroupComment), así que un comentario borrado en el sistema nuevo sería recreado por el re-run de producción comprometido en [[adr-0010]]. A diferencia de los adjuntos, aquí no hay archivo en storage que sirva de lápida, así que la solución de los adjuntos no aplica directa. Se anotan además dos pendientes menores de la misma sesión, ambos sin decidir por Ricardo: el diagnóstico test_migrate_orphan.py quedó fuera de la suite en api/.claude/ (¿séptimo test o borrar?), y la propuesta de un Playwright que cubra la cadena unit, que puede romperse en silencio.

## Criterios de aceptación

- [ ] Un comentario borrado en el sistema nuevo no reaparece al re-correr migrate_flow_data
- [ ] Decisión de Ricardo sobre el séptimo test (api/.claude/test_migrate_orphan.py: promover a flow/tests/ o borrar)
- [ ] Decisión de Ricardo sobre la propuesta de Playwright para la cadena unit (seed → catálogo → suffix)
