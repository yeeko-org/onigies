---
type: task
id: task-97
title: Resurrección de comentarios legacy en el re-run de migrate_flow_data
state: open
date: 2026-08-09
owner: ai
parent: "[[task-1]]"
source: ["[[2026-08-09-sesion-task-93-y-drift-del-harness]]"]
related: ["[[task-7]]", "[[adr-0010]]"]
---

# Resurrección de comentarios legacy en el re-run de migrate_flow_data

Mismo bug que la resurrección de adjuntos resuelta el 2026-08-09, pero en la rama de comentarios: _create_event usa get_or_create sobre las filas legacy vivas (ObservableComment, GroupComment, GeneralGroupComment), así que un comentario borrado en el sistema nuevo sería recreado por el re-run de producción comprometido en [[adr-0010]]. A diferencia de los adjuntos, aquí no hay archivo en storage que sirva de lápida, así que la solución de los adjuntos no aplica directa. Se anotan además dos pendientes menores de la misma sesión, ambos sin decidir por Ricardo: el diagnóstico test_migrate_orphan.py quedó fuera de la suite en api/.claude/ (¿séptimo test o borrar?), y la propuesta de un Playwright que cubra la cadena unit, que puede romperse en silencio.

## Veredicto sobre el séptimo test (2026-08-11)

Ricardo decidió: **es un test temporal y se borra, no se promueve**. Protege un comando de migración de una sola vez —que se corre en el deploy y después deja de tener razón de ser—, así que su vida útil termina cuando la verificación de esa migración se dé por cerrada. Vale la regla de la casa: los tests mueren con su feature.

Se queda donde está, fuera de la suite, mientras la verificación siga abierta.

## Riesgo aceptado para el deploy del 2026-08-12

Ricardo decidió correr `migrate_flow_data` completo en el re-run comprometido por [[adr-0010]] ([[2026-08-12-deploy-gen-a-produccion-migraciones-seeds]]): no se ha borrado ningún comentario en producción, así que la resurrección no tenía qué resucitar. El bug sigue vivo para cualquier re-run futuro — esta task no se cierra con ese deploy.

## El comando fue retirado (2026-08-12)

Tras el incidente de [[2026-08-12-incidente-migrate-flow-data]] (el re-run aplastó 179 estatus avanzados), `migrate_flow_data` y `verify_flow_data` se retiraron del repo: el bug de resurrección ya no puede ocurrir y el primer criterio quedó sin objeto. La task queda abierta deliberadamente para que una sesión futura decida su destino: cerrarla como sin objeto o rescatar sus pendientes propios (el séptimo test, ya decidido como temporal — su vida útil terminó con el retiro—, y la propuesta de Playwright para la cadena unit, aún sin decisión de Ricardo).

## Criterios de aceptación

- [ ] Un comentario borrado en el sistema nuevo no reaparece al re-correr migrate_flow_data
- [x] Decidido el destino del séptimo test: es temporal, se borra al cerrar la verificación de la migración
- [ ] Decisión de Ricardo sobre la propuesta de Playwright para la cadena unit (seed → catálogo → suffix)
