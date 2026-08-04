---
type: task
id: task-59
title: Reparar los sent_at nulos de los envíos en producción
state: closed
date: 2026-08-04
owner: ai
source: ["[[2026-08-04-sesion-seccion-informacion-base]]"]
---

# Reparar los sent_at nulos de los envíos en producción

El motor guardaba con `update_fields=['status']` y el hook que asigna `sent_at` nunca llegaba a la base (arreglado el 2026-08-04: el motor persiste con `save()` completo). En producción, los paquetes bp enviados antes del fix tienen `sent_at` nulo. La fecha es recuperable con fidelidad: el `FlowEvent` de envío se escribía en la misma transacción, así que `min(created_at)` de los eventos con `to_status` en (`bp_sent`,`bp_resent`) es la fecha exacta y respeta el no-pisar-al-reenviar. Los paquetes que llegaron a su status por `migrate_flow_data` no tienen evento; ver si el flujo viejo (`status_sending`/`StatusControl`) conserva fecha. En local: 62 paquetes bp, 3 con sent_at, 1 reparable por evento, 1 enviado sin evento — la mayoría nunca se envió y no necesita nada. La consulta de dimensionamiento quedó en el reporte del ejecutor backend de la sesión.

## Criterios de aceptación

- [x] Se dimensionó en producción cuántos paquetes bp/gen enviados tienen sent_at nulo, separando con y sin FlowEvent
- [x] Los reparables recibieron el created_at del primer FlowEvent de envío (comando o RunPython idempotente)
- [x] Los no reparables (migrados del flujo viejo, sin evento) quedaron decididos: fecha del flujo viejo o null deliberado

Cierre 2026-08-04: 36 paquetes bp reparados con el comando `repair_sent_at` (dry-run y verificación de idempotencia en producción); gen no tenía envíos. El único sin evento (id=64, migrado del flujo viejo como `bp_finished` con `status_sending=discarded`) era un paquete de prueba: Ricardo decidió null deliberado, sin investigar el mapeo. El flujo viejo no conserva fecha alguna (StatusControl es catálogo puro).
