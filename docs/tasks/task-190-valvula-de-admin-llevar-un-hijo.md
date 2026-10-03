---
type: task
id: task-190
title: "Válvula de admin: llevar un hijo o nieto a cualquier status de revisión mientras la raíz esté en revisión"
state: open
date: 2026-10-02
owner: ai
source: ["[[2026-10-02-comentarios-editables-y-valvula-de-admin]]"]
related: ["[[adr-0023]]", "[[adr-0002]]", "[[adr-0019]]", "[[task-58]]", "[[task-87]]", "[[task-71]]", "[[task-189]]"]
---

# Válvula de admin: llevar un hijo o nieto a cualquier status de revisión mientras la raíz esté en revisión

Lo decidido está en [[adr-0023]]; aquí va lo que hay que construir. El caso que la motiva es [[task-58]]: una revisora devuelve un grupo gen (`gen_need_changes`) sin devolver el paquete, el grupo queda en rol IES bajo una raíz en turno revisor y nadie puede deshacerlo desde la interfaz. También sirve para los casos de [[task-87]] (lote «recibida para dictamen» con errores) y como alternativa al admin de Django de [[task-71]].

## Backend

- Endpoint nuevo `POST /flow/<app>/<model>/<pk>/admin-transitions/`, separado del de transiciones; el actual no cambia ni una línea.
- Permiso: `request.user.is_admin` (ya existe en `User`: `is_superuser or is_staff`). Nunca `is_staff` directo.
- Validación: el objeto no es raíz (`resolve_flow_root(obj) is not obj`); la raíz tiene rol `reviewer` (en `cp` la raíz es `AxisValue`, el eje, no la encuesta); el destino es cualquier status que la revisión puede establecer o en el que tiene el turno —los destinos de las transiciones de rol `reviewer` en `NEXT_STATUSES` (`bp_need_changes`, `bp_for_ruling`, `bp_rejected`; `gen_need_changes`, `gen_approved`; `cp_approved`, `cp_need_changes`, `cp_partial_approved`) más los status de rol `reviewer` del grupo, que sirven para deshacer (`*_completed`, `*_adjusted`, `cp_voluntary_readjust`, `cp_partial`)—, aplicable al modelo, **menos el status actual y sus `next_statuses`**: un destino legal responde 400 «es una transición normal; usa el menú de estatus» (decidido el 2026-10-02 tras la pasada en navegador, P21: un cambio de válvula a destino legal se pintaba como transición normal porque la marca se deriva del grafo). Comentario obligatorio. Se salta el rol propio del origen (terminales incluidos); se conserva `_check_children_rule` y la propagación de `execute_transition`.
- Función hermana `execute_admin_transition` + `validate_admin_transition` en `api/flow/services.py`, que comparten con `execute_transition` los efectos (`_apply_transition`: evento, guardado, propagación, señal). El conjunto por grupo lo calcula `admin_target_names(group)` del grafo, nunca por nombre.
- El motivo del evento no se borra (403 en `DELETE`, incluso para admin) y solo lo corrige `is_admin` (P24).
- El catálogo `/flow/statuses/` lleva `admin_targets` por fila (el conjunto del grupo); el cliente resta el actual y sus `next_statuses`, y conserva un fallback que recalcula del grafo hasta que API y Netlify estén ambos desplegados.
- El `FlowEvent` se escribe como cualquier transición, con el comentario. Sin columna nueva ni migración.

## Frontend

- Getter `is_admin` en `store/auth.js`, espejo de `User.is_admin`; el componente lee ese getter, nunca `is_staff` ([[2026-09-28-revisoras-sin-is-staff-en-generales]]).
- Botón aparte junto al menú de transiciones (`FlowStatusActions` / `FlowTransitionMenu`), visible solo con `is_admin` y solo cuando el objeto no es raíz y la raíz está en rol reviewer. Lista los destinos definidos arriba (lo que la revisión establece más los status de rol reviewer para deshacer), aplicables al modelo y **fuera del grafo** (sin el actual, que ya va como chip, ni sus `next_statuses`); si no queda ninguno, el diálogo lo dice con una alerta informativa. Diseño en `.claude/scratch/2026-10-02-ux-valvula-admin-flow.md`: botón de ícono `admin_panel_settings` a la derecha del chip de status dentro de `FlowStatusActions`, bloqueado con tooltip cuando la raíz no está del lado revisor; diálogo propio con alerta de advertencia, status actual y raíz como chips, destino en radio buttons con descripción, campo obligatorio «Motivo del cambio», confirmar en color warning y sin segundo paso. El request usa `target_status`, como el endpoint de transiciones. La advertencia específica para `gen` (P25) se quitó al cierre («D3 (1)»): cp solo abre con el paquete en `gen_finished`, terminal y de nadie, y la válvula exige la raíz en turno revisor, así que nunca reabre un grupo sobre el que cp ya construyó.
- Diálogo que dice con claridad que no se recomienda, que está fuera del flujo normal, y pide el comentario. Ricardo pidió «un diálogo muy claro que diga que no se recomienda y que si está bien segura de eso»; el diseño con `ux-designer` lo resolvió sin checkbox ni segundo paso (la alerta más el motivo obligatorio), y Ricardo lo confirmó al cierre («D2. (2)»).
- El timeline (`FlowTimeline`) pinta como «Cambio administrativo» (nombre en la UI, decidido 2026-10-02) un evento cuyo `to_status` no está en los siguientes legales de su `from_status` **y que trae comentario** (el store ya tiene el grafo); la segunda condición excluye los eventos que el motor ya escribe fuera del grafo sin comentario (`assign_status_tree` por el «No» de un observable, cascada de `bp_discarded`). No se necesita bandera del backend. Transparencia total: la IES ve la marca y el motivo igual que la revisión; no se filtra por audiencia.

## Lo construido (2026-10-02)

Backend, frontend y tests hechos en la misma sesión; pasada en navegador con Playwright MCP (46 capturas en `.claude/scratch/browser-pass/`): botón, bloqueo con tooltip, diálogo, aplicar, marca en el timeline, visibilidad por audiencia. Tests `AdminOverrideTests`, `AdminTargetCatalogTests`, `AdminOverrideChildrenRuleTests`; Vitest de `getAdminTargets`, `isAdminEvent`, `getAdminRootBlock`, `is_admin`. Reglas en la skill `flow` (references/admin-override.md).

## Destinos efectivos por origen

El conjunto del grupo (lo que la revisión establece ∪ rol reviewer) menos el status actual y sus `next_statuses`, calculado de `NEXT_STATUSES` en `api/flow/seed.py`; el catálogo manda el conjunto del grupo en `admin_targets` y el cliente resta por objeto.

| Grupo · origen | Destinos de la válvula |
|---|---|
| bp · `bp_draft` | adjusted, need_changes, for_ruling, rejected |
| bp · `bp_discarded` | completed, adjusted, need_changes, for_ruling, rejected |
| bp · `bp_completed` | adjusted |
| bp · `bp_adjusted` | completed |
| bp · `bp_need_changes` | completed, for_ruling, rejected |
| bp · `bp_for_ruling` | completed, adjusted, need_changes, rejected |
| bp · `bp_rejected` | completed, adjusted, need_changes, for_ruling |
| gen · `gen_draft` | adjusted, need_changes, approved |
| gen · `gen_completed` | adjusted |
| gen · `gen_adjusted` | completed |
| gen · `gen_need_changes` | completed, approved |
| gen · `gen_approved` | completed, adjusted, need_changes |
| cp · `cp_pre_start`, `cp_not_present` | los siete: completed, adjusted, voluntary_readjust, partial, approved, need_changes, partial_approved |
| cp · `cp_filling` | adjusted, voluntary_readjust, approved, need_changes, partial_approved |
| cp · `cp_completed` | adjusted, voluntary_readjust, partial, partial_approved |
| cp · `cp_need_changes` | completed, adjusted, voluntary_readjust, partial, approved, partial_approved |
| cp · `cp_in_adjustment` | completed, voluntary_readjust, partial, approved, need_changes, partial_approved |
| cp · `cp_adjusted` | completed, voluntary_readjust, partial, partial_approved |
| cp · `cp_postponed` | adjusted, voluntary_readjust, approved, need_changes, partial_approved |
| cp · `cp_voluntary_readjust` | completed, adjusted, partial, approved, partial_approved |
| cp · `cp_partial` | completed, adjusted, voluntary_readjust, approved |
| cp · `cp_partial_approved` | adjusted, voluntary_readjust, approved, need_changes |
| cp · `cp_approved` | completed, adjusted, partial, need_changes, partial_approved |

Consecuencia que el coordinador no vio al proponer P21: los movimientos legales cuyo origen es de rol IES (`gen_need_changes→gen_adjusted`, `bp_need_changes→bp_adjusted`, `cp_filling`/`cp_postponed`/`cp_partial_approved`→`cp_completed`/`cp_partial`, `cp_in_adjustment→cp_adjusted`, `cp_approved→cp_voluntary_readjust`) quedan fuera de la válvula por legales y fuera del menú normal porque son de la IES; una admin no puede hacerlos. Son acciones de la IES (marcar completado, ajustado, reajuste voluntario) y se dejan así.

## Deploy

Lo ejecuta Claude en la sesión de deploy con la skill `deploy-api`. Esta rama lleva **dos migraciones**: `answer.0007_protect_instrument_fks` ([[task-178]], aún no en `origin/production`) y `example.0010_remove_dead_comments`, que borra `GoodPracticePackage.comments` y `GoodPractice.comments` (campos muertos; solo vive el de criterio). El deploy del nivel técnico superior (`sector-tsu`, task-192 en esa rama) añade `answer.0008` y su comando; **un solo runbook debe cubrir las tres migraciones** y correr después de fusionar ambas ramas ([[task-186]]). En el merge chocarán `api/TESTING.md` y `.claude/skills/cp-questionnaire/SKILL.md`, tocados por las dos sesiones.

1. **Orden de push: API primero, Netlify después** (deploy-api §4: API nueva con front viejo es el sentido seguro; el front nuevo contra la API vieja recibiría 404 en `events/<id>/` y `admin-transitions/`). Con ese orden el fallback cliente de `admin_targets` nunca se ejercita ([[task-197]]).
2. Antes del push: emulación local del build de Netlify (deploy-api §Frontend build); el último `pnpm run build` fue antes de los últimos cambios de `FlowAdminOverride`, `store/flow.js`, `FlowTimeline`, `FlowComments`, `GoodPracticePackageEditSimple` y `vitest.config.ts`.
3. En el servidor, con el código viejo y antes de `migrate`, dos lecturas de solo lectura:
   - Conteo de las columnas por borrar: `SELECT COUNT(*) FROM example_goodpracticepackage WHERE comments IS NOT NULL AND comments <> '';` y lo mismo sobre `example_goodpractice`. **Esperado: paquete 1 (pk 64, UAPRUEBA, institución de prueba, texto «MÁS») y práctica 0, según la base local al 2026-09-28; en producción no se contó.** Los nombres de tabla son los default de Django (`app_label_modelo`, sin `db_table` en `example/models.py`). Otro número detiene la línea y se consulta a Ricardo: el `pg_dump` del runbook sería la única copia.
   - Conteo de eventos que la marca «Cambio administrativo» pintaría sobre historia vieja: FlowEvents con `from_status` y `to_status`, comentario no vacío y `to_status` fuera de `next_statuses` del origen (consulta por ORM, como la del crítico en local: 0 al 2026-09-28). Si hay, la IES los vería marcados y nadie salvo admin podría corregir su texto; decidir con Ricardo antes de seguir.
   - `SELECT name FROM django_migrations WHERE app IN ('answer','example') ORDER BY name;` no debe listar aún `0007`, `0008` ni `0010`.
4. `migrate` (sin app: las tres), `makemigrations --check --dry-run` → «No changes detected», `supervisorctl restart apionigies`, smoke: `/api/catalogs/all/` y un `GET /api/good_practice/` autenticado en 200, y `information_schema.columns` sin `comments` en las dos tablas.
5. Push a `production` para Netlify; verificar por build id.

Riesgo bajo, nombrado: raíces cuyo status se puso sin FlowEvent (migración, `.update()`, el restore del 2026-08-12) no tienen evento de cruce de lado, así que sus comentarios viejos siguen editables como antes.

**Ricardo decidió desplegar cuando las revisoras terminen su jornada**: el 2026-10-02 devolvieron 24 prácticas y estaban trabajando en bp.

## Tests

- Backend: el endpoint normal sigue rechazando un destino fuera del grafo para todos; el de admin lo acepta solo con `is_admin`, comentario y raíz en revisión; rechaza raíces y raíces en rol IES; conserva la regla de hijos.
- [[task-189]] gana un mock admin (`is_staff: true`) distinto del de revisora sin staff; la revisora no ve el botón, el admin sí.

## Criterios de aceptación

- [ ] Un admin lleva un grupo gen en `gen_need_changes` a `gen_approved` con el paquete en `gen_sent`, con comentario, desde la UI (en navegador solo se abrió y canceló el diálogo en gen; sin test backend en gen: los tests usan bp y cp)
- [x] Un admin lleva una buena práctica en `bp_for_ruling` a `bp_need_changes` con el paquete en `bp_sent`
- [x] Con la raíz en rol IES, en terminal, o sobre la raíz misma, el endpoint responde 400 y el botón no aparece
- [x] Una revisora sin `is_staff` no ve el botón y el endpoint le responde 403
- [x] El evento aparece en el timeline distinguido como cambio administrativo, con su comentario
- [x] Un destino legal desde el status actual responde 400 y no aparece en el diálogo
- [x] La regla de hijos y la propagación siguen aplicando
- [x] El endpoint de transiciones normales no cambió
- [ ] Emulación del build de Netlify corrida tras los últimos cambios del frontend (hecha 2026-10-02 tras D1/D3; si el frontend vuelve a cambiar, repetir)
- [ ] Desplegado en producción con las migraciones verificadas (conteos previos y eventos fuera del grafo), API antes que Netlify, fuera de la jornada de las revisoras

## Pendientes de UI para admin (fuera de esta task)

Ricardo eligió «D4. 1»: el admin ve «Guardar» siempre en `GoodPracticeEditSimple` (`v-if="editable || isAdmin"`). Quedan sin resolver, como diseño de UI y no como decisión: (a) los criterios cambian de layout por audiencia (la revisora ve ícono en vez de checkbox y la justificación en solo lectura), así que el admin solo edita contenido de criterios por API salvo que se construya un layout híbrido; (b) los adjuntos siguen siendo solo de la IES, admin incluido, en backend (`attachment_views.py`) y UI; (c) la superficie de revisora no tiene botón de «agregar práctica». Se abren tasks cuando Ricardo pida alguna.
