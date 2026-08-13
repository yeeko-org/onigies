---
type: record
id: 2026-08-12-incidente-migrate-flow-data
date: 2026-08-12
---

# Incidente de datos: migrate_flow_data aplastó los estatus de flow en producción

Sesión duo (coordinador Fable + ejecutores + auditor). Ricardo detectó en el dashboard que casi todos los Envíos de Buenas Prácticas y sus prácticas aparecían en «Borrador» cuando al menos 35 habían avanzado. Diagnóstico read-only primero; cada cambio a la base pasó por su aprobación explícita, paso a paso.

## Qué pasó

El re-run de `migrate_flow_data` del deploy gen ([[2026-08-12-deploy-gen-a-produccion-migraciones-seeds]], corrido a las 21:11:03 UTC — la hora la delatan los eventos de espejado que el propio comando creó) sobrescribió `flow.Status` desde las columnas legacy (`status_sending`/`status_register`) con un UPDATE incondicional: su único filtro era la fuente, nunca el destino. Como el motor nuevo jamás escribe las columnas legacy, éstas quedaron fósiles en su valor de creación, y el re-run regresó a ese valor todo lo que había avanzado — en silencio, sin crear FlowEvents. El docstring prometía «idempotente, re-ejecutable»: cierto respecto a su fuente, destructivo respecto a su destino.

## Censo del daño (179 objetos)

Diff del dump pre-deploy (`onigies_pre_gen_deploy_20260812_202658.dump`) contra la BD viva, triangulado con `sent_at` y `FlowEvent`:

| Modelo | Filas | De → a |
|---|---|---|
| GoodPracticePackage | 36 | `bp_sent` → `bp_draft` |
| GoodPractice | 139 | `bp_completed` → `bp_draft` |
| GoodPractice (id 36) | 1 | `bp_adjusted` → `bp_completed` (la «reconciliación» del log del deploy) |
| GeneralGroupResponse | 3 | `gen_completed` → `gen_draft` |

`AxisValue` salió intacto (todo estaba aún en `cp_pre_start`) y las tablas de respuestas cp están vacías. Ningún usuario real de IES trabajó después del daño; la única actividad posterior fue de Ricardo y su cuenta de prueba (las generales 311 y 315, re-completadas, se excluyeron de la restauración). La duda de Ricardo sobre la cobertura de `FlowEvent` resultó fundada: 14 objetos avanzados no tenían ningún evento (la migración original de junio tampoco los creaba), así que la fuente primaria de la verdad fue el dump, con los eventos solo para detectar actividad post-incidente.

## Restauración y limpieza

- **Restauración quirúrgica** (aprobada paso a paso): script SQL escrito a mano por el coordinador, cada UPDATE condicionado al valor dañado, transacción con candado que aborta si los conteos finales no cuadran. Resultado: 36/139/1/3 exactos, foto final idéntica al dump. Smoke visual de Ricardo en el dashboard: en orden. Respaldo previo `onigies_pre_restore_20260813_023044.dump` (servidor + copia local).
- **Fuga colateral descubierta**: la rama de comentarios del comando espejaba los TextField privados de la revisora (`FeatureGoodPractice.comments` y afines) como eventos del timeline, legibles por la IES dueña (`FlowEventView.get` solo verifica ownership). Se borraron de producción los 11 eventos espejados (ids 1, 2, 3, 213–220) tras verificación textual contra el campo origen (10 coincidencias exactas, 1 copia obsoleta de una versión previa del mismo campo); los 18 comentarios genuinos del timeline no se tocaron.
- **Retiro del comando** (aprobado): `migrate_flow_data`, `verify_flow_data`, `deploy_flow_migration.sh` y el diagnóstico suelto `test_migrate_orphan.py` (vivía en el `.claude/` del api) salieron del repo. Verificación previa: ya no queda ninguna vía de escritura viva hacia los modelos legacy salvo los defaults de creación. Tests del API: 94 en verde antes y después.

## Auditoría de proceso (tres capas)

- **Técnica**: UPDATE incondicional de fuente muerta a destino vivo, sin guard, sin eventos, sin dry-run.
- **De proceso**: el riesgo del re-run se evaluó por precedente (la resurrección de comentarios de [[task-97]]) y no por enumeración de lo que el comando escribe; la Decisión 1 del deploy nunca mencionó `migrate_statuses`. La «1 reconciliación bp_draft → bp_completed» del log era el fingerprint del aplanamiento, leída como éxito por falta de expectativa previa.
- **Documental**: «idempotente, re-ejecutable» nació cierto en el diseño de junio, caducó en silencio con el cutover y se propagó (docstring → records → precondición de [[task-7]]) sin dueño ni condición de validez. `verify_flow_data` no podía detectarlo: importaba los mapas del propio migrador — validaba completitud, no preservación.

Lo que sí funcionó: el respaldo pre-deploy del runbook fue la razón de que el incidente fuera reparable, y el patrón seguro ya existía en casa (`repair_sent_at`: dry-run por defecto, `--apply`, solo filas sin inicializar).

## Consecuencias registradas

- Regla nueva en el skill `deploy-api` («Data-writing management commands»): inventario de escrituras leído del código, sonda de conteos pre/post con expectativa escrita de antemano, y el patrón `repair_sent_at` como estándar de los comandos re-ejecutables.
- [[task-124]] abierta: mapa completo del proceso de comentarios (los dos mecanismos, visibilidad por rol, el hueco de `FlowEventView.get`, y qué hacer ahora que el campo privado ya nunca llegará al timeline).
- La precondición de [[task-7]] («re-correr justo antes del borrado») quedó reescrita: la migración de datos está completa y congelada desde este día.
- [[task-97]] queda abierta deliberadamente para que una sesión futura decida su destino: el bug que la motivaba ya no puede ocurrir.
- [[adr-0010]] anotado: los comandos que citaba como evidencia se retiraron este día.
