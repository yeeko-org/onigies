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
- Validación: el objeto no es raíz (`resolve_flow_root(obj) is not obj`); la raíz tiene rol `reviewer` (en `cp` la raíz es `AxisValue`, el eje, no la encuesta); el destino es cualquier status que la revisión puede establecer o en el que tiene el turno —los destinos de las transiciones de rol `reviewer` en `NEXT_STATUSES` (`bp_need_changes`, `bp_for_ruling`, `bp_rejected`; `gen_need_changes`, `gen_approved`; `cp_approved`, `cp_need_changes`, `cp_partial_approved`) más los status de rol `reviewer` del grupo, que sirven para deshacer (`*_completed`, `*_adjusted`, `cp_voluntary_readjust`, `cp_partial`)—, aplicable al modelo; comentario obligatorio. Se salta el rol propio del origen y `next_statuses` (terminales incluidos); se conserva `_check_children_rule` y la propagación de `execute_transition`.
- Hay que ver si `execute_transition` admite un modo que salte las comprobaciones 1 y 3 de `validate_transition` o si conviene una función hermana; `assign_status_tree` no sirve porque no propaga ni valida hijos.
- El `FlowEvent` se escribe como cualquier transición, con el comentario. Sin columna nueva ni migración.

## Frontend

- Getter `is_admin` en `store/auth.js`, espejo de `User.is_admin`; el componente lee ese getter, nunca `is_staff` ([[2026-09-28-revisoras-sin-is-staff-en-generales]]).
- Botón aparte junto al menú de transiciones (`FlowStatusActions` / `FlowTransitionMenu`), visible solo con `is_admin` y solo cuando el objeto no es raíz y la raíz está en rol reviewer. Lista los destinos definidos arriba (lo que la revisión establece más los status de rol reviewer para deshacer), aplicables al modelo, no solo los de `next_statuses`; el actual se muestra deshabilitado. Diseño en `.claude/scratch/2026-10-02-ux-valvula-admin-flow.md`: botón de ícono `admin_panel_settings` a la derecha del chip de status dentro de `FlowStatusActions`, bloqueado con tooltip cuando la raíz no está del lado revisor; diálogo propio con alerta de advertencia, status actual y raíz como chips, destino en radio buttons con descripción, campo obligatorio «Motivo del cambio», confirmar en color warning y sin segundo paso. El request usa `target_status`, como el endpoint de transiciones.
- Diálogo de confirmación que dice con claridad que no se recomienda, que está fuera del flujo normal, y pide confirmación explícita y el comentario. Ricardo: «un diálogo muy claro que diga que no se recomienda y que si está bien segura de eso». El diseño se hace con `ux-designer`.
- El timeline (`FlowTimeline`) pinta como «Cambio administrativo» (nombre en la UI, decidido 2026-10-02) un evento cuyo `to_status` no está en los siguientes legales de su `from_status` **y que trae comentario** (el store ya tiene el grafo); la segunda condición excluye los eventos que el motor ya escribe fuera del grafo sin comentario (`assign_status_tree` por el «No» de un observable, cascada de `bp_discarded`). No se necesita bandera del backend. Transparencia total: la IES ve la marca y el motivo igual que la revisión; no se filtra por audiencia.

## Tests

- Backend: el endpoint normal sigue rechazando un destino fuera del grafo para todos; el de admin lo acepta solo con `is_admin`, comentario y raíz en revisión; rechaza raíces y raíces en rol IES; conserva la regla de hijos.
- [[task-189]] gana un mock admin (`is_staff: true`) distinto del de revisora sin staff; la revisora no ve el botón, el admin sí.

## Criterios de aceptación

- [ ] Un admin lleva un grupo gen en `gen_need_changes` a `gen_approved` con el paquete en `gen_sent`, con comentario, desde la UI
- [ ] Un admin lleva una buena práctica en `bp_for_ruling` a `bp_need_changes` con el paquete en `bp_sent`
- [ ] Con la raíz en rol IES, en terminal, o sobre la raíz misma, el endpoint responde 400 y el botón no aparece
- [ ] Una revisora sin `is_staff` no ve el botón y el endpoint le responde 403
- [ ] El evento aparece en el timeline distinguido como cambio administrativo, con su comentario
- [ ] La regla de hijos y la propagación siguen aplicando
- [ ] El endpoint de transiciones normales no cambió
