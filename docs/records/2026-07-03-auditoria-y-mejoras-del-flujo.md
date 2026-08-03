---
type: record
id: 2026-07-03-auditoria-y-mejoras-del-flujo
title: Auditoría y mejoras del flujo de validación — seed, seguridad y frontend
date: 2026-07-03
---

# Plan — Mejoras al flujo de validación (revisión exhaustiva 2026-07)

Estado: **propuesta, pendiente de decisiones de Ricardo** (ver §6).
Origen: sesión de revisión de `api/flow/seed.py` + auditorías backend y
frontend (subagentes Opus 4.8). Complementa (no reemplaza) a
[[2026-06-05-diseno-del-motor-de-flujo]].

---

## 1. Rediseño de contenidos del seed (colores, íconos, priority)

Hallazgo previo: el modelo `Status` ya tiene `priority` e `icon`
(`flow/models.py`), pero el seed **nunca los escribe**; `color` solo se
asigna al crear. Decisión ligada: política "el seed manda" (§6-f).

Semántica de color constante entre grupos: azul = captura, cian =
completado-esperando-envío, morados = en revisión, naranja/ámbar =
correcciones, teal = corregido, verde = aprobado, rojo = rechazo,
café = pausa/abandono, gris azulado = cerrado neutro.

Priority (0–100, mayor = más urgente): 90s = correcciones pendientes,
70s–80s = turno de la revisión, 50s–60s = trabajo IES en curso,
30s–40s = latente, ≤20 = cerrado.

### bp

| status | color | icon | priority |
|---|---|---|---|
| bp_need_changes | orange | new_releases | 90 |
| bp_adjusted | teal | published_with_changes | 80 |
| bp_resent | indigo | forward_to_inbox | 78 |
| bp_sent | deep-purple | send | 75 |
| bp_completed | cyan | task_alt | 60 |
| bp_draft | blue | edit_note | 50 |
| bp_for_ruling | green | verified | 30 |
| bp_rejected | red | cancel | 20 |
| bp_discarded | brown | do_not_disturb_on | 15 |
| bp_finished | blue-grey | sports_score | 10 |

### cp

| status | color | icon | priority |
|---|---|---|---|
| cp_need_changes | orange | new_releases | 90 |
| cp_voluntary_readjust | pink | lock_open | 85 |
| cp_adjusted | teal | published_with_changes | 80 |
| cp_resent | indigo | forward_to_inbox | 78 |
| cp_sent | deep-purple | send | 75 |
| cp_in_review | purple | fact_check | 72 |
| cp_in_adjustment | amber | construction | 70 |
| cp_partial | lime-darken-2 | rule | 65 |
| cp_completed | cyan | task_alt | 60 |
| cp_partial_approved | light-green | incomplete_circle | 55 |
| cp_filling | blue | edit_note | 50 |
| cp_postponed | brown-lighten-1 | snooze | 40 |
| cp_pre_start | blue-grey-lighten-1 | hourglass_empty | 35 |
| cp_approved | green | done_all | 10 |

### gen (espejo de bp)

| status | color | icon | priority |
|---|---|---|---|
| gen_need_changes | orange | new_releases | 90 |
| gen_adjusted | teal | published_with_changes | 80 |
| gen_resent | indigo | forward_to_inbox | 78 |
| gen_sent | deep-purple | send | 75 |
| gen_completed | cyan | task_alt | 60 |
| gen_draft | blue | edit_note | 50 |
| gen_approved | green | done_all | 15 |
| gen_finished | blue-grey | sports_score | 10 |

Nota de estilo pendiente (§6-a): sólidos vs pasteles `lighten-3/4`.

## 2. Textos

1. `bp_for_ruling`: "Recibida" → **"Recibida para dictamen"**; action
   "Recibir" → "Recibir para dictamen".
2. Unificar `*_adjusted`: **"Ajustes atendidos"** (neutro en género) con
   action "Marcar ajustes como atendidos" en bp/cp/gen.
3. `bp_discarded` "Descartado": choque de género (paquete m / práctica f).
   Opciones: dejarlo, "Participación descartada", "Sin participación".
   Decisión §6-b.
4. `cp_partial` action: "Enviar parcial a corroborar" → "Enviar avance
   parcial".
5. Descriptions: "en manos de la revisión" → "están en revisión" (3
   ocurrencias).
6. **HINTS faltantes (19):** todo cp (14), `bp_draft`,
   `gen_completed/adjusted/resent/approved`. Regla: el hint se dirige a
   quien tiene el turno (`role`); terminales en tono neutro. Redactar en
   la sesión de edición.

## 3. Comentarios (comment_type / prompts)

Bug confirmado: `bp_rejected` tiene comentario obligatorio pero
`role=None` → `COMMENT_PROMPT_BY_ROLE.get(None)` devuelve `None` y la
caja queda sin rótulo.

Separar defaults obligatorio vs opcional + overrides imperativos:

| status | prompt |
|---|---|
| bp/cp/gen_need_changes | «Describe las correcciones que la institución debe atender.» (aprobado) |
| bp_rejected | «Explica a la institución por qué la práctica no fue acreditada.» |
| cp_voluntary_readjust | «Explica qué necesitas corregir y por qué pides reabrir la respuesta.» |
| cp_partial | «Describe qué respuestas están listas para corroborar y qué falta.» |
| opcionales | default por rol actual («Si gustas, agrega un mensaje para…») |

Flags a emparejar (decisión §6-c):

- `bp_resent`, `gen_sent`, `gen_resent`, `cp_sent`: agregar `confirm`
  (+ `comment_opt` en los envíos).
- `cp_adjusted`, `gen_adjusted`: agregar `comment_opt` («describe los
  ajustes que realizaste», como bp_adjusted).
- `bp_rejected`: agregar `confirm` (terminal e irreversible).
- Suave: `comment_opt` en aprobaciones (`cp_approved`, `gen_approved`,
  `bp_for_ruling`).

Frontend relacionado (hallazgo F6): el fallback de prompt cuando falta
en catálogo es siempre "Comentario", sin distinguir required/optional —
diferenciar fallbacks en `FlowTransitionDialogs.vue`.

## 4. Grafo: transiciones y reglas de hijos

1. **Dead-end `bp_resent` (confirmado a nivel grafo):**
   `VALID_CHILD_STATUSES["bp_resent"] = [bp_adjusted, bp_completed]` no
   admite `bp_for_ruling`/`bp_rejected`. Ronda mixta (unas prácticas
   dictaminadas, otras devueltas) → tras ajustar, el paquete no puede
   reenviarse. Fix: agregar ambos a la lista.
2. **Dead-end `bp_discarded` (auditor B6):** la lista no incluye
   `bp_completed`; si la IES completó alguna práctica y luego quiere
   descartar, el motor lo rechaza. Fix: agregar `bp_completed`.
3. **Sin válvula de escape en bp y gen:** `bp_finished`, `bp_rejected`,
   `bp_for_ruling`, `gen_approved`, `gen_finished` son terminales
   absolutos (cp tiene `cp_voluntary_readjust`). El plan v2 contemplaba
   `gen_approved → gen_need_changes` y se perdió. Decisión §6-d.
4. **Orden no obvio en `cp_voluntary_readjust`:** propaga up; para mover
   el eje a `cp_need_changes` hay que mover primero al hijo. Fix posible:
   agregar `cp_voluntary_readjust` a
   `VALID_CHILD_STATUSES["cp_need_changes"]`, o documentar el orden.
5. Menor: listas mixtas P/GP en `NEXT_STATUSES` son válidas (el motor
   filtra por `applicable_models`) pero confunden al leer — anotar en la
   reestructura.

## 5. Auditorías (hallazgos no-seed)

### Backend — ALTA (seguridad)

- **B1. Sin ownership en `/flow/.../transitions/`** (`flow/views.py`):
  cualquier IES autenticada puede transicionar objetos de otra
  institución. Existe `IsInstitutionOwnerOrSuperuser` sin aplicar.
- **B2. Ídem en `discard`/`reopen`** (`GoodPracticePackageViewSet`):
  queryset sin filtrar + sin permiso de objeto.
- **B3. Ídem en comentarios** (`FlowEventView.post`).
- **B4. `assign_auto_status` es código muerto:** nadie lo llama; las
  raíces (paquetes, ejes, GeneralPackage…) nacen con `status=NULL` y el
  motor rechaza toda transición sobre ellas. Cablear en el primer
  guardado (vista/serializer o signal) o `default` en los FK.

### Backend — MEDIA

- **B5. TOCTOU:** `execute_transition` sin `select_for_update` — doble
  submit puede aplicar dos transiciones. Re-obtener con lock.
- **B7. Nadie puede comentar en terminales** (`role=None` nunca iguala
  el rol del usuario). ¿Intencional? Si no, permitir a revisoras.
- **B8. `migrate_flow_data` roto para gen:** mapea a `gen_pre_start`/
  `gen_filling` que ya no existen (IntegrityError) y `GeneralPackage`
  no está en el mapa (queda NULL, se encadena con B4).

### Backend — BAJA

- B9: sin test que sincronice `get_available_transitions` cliente/servidor.
- B10: `print` de debug en `example/models.py` (ya previsto en §8 del
  plan original).
- B11: regla de hijos solo directa (cubierta transitivamente hoy).
- B12: propagación con save por nodo (N+1 aceptable, árboles chicos).

### Frontend

- **F1 (media).** `GoodPracticeList.vue:49` hardcodea
  `bp_sent`/`bp_resent` para el CTA de envío — viola "el motor manda".
- **F2 (media).** `discard`/`reopen` con confirmación hardcodeada fuera
  del catálogo (`confirm_title`/`confirm_text` no se heredan); `reopen`
  sin snackbar.
- **F3 (media).** Status del paquete puede quedar stale tras propagación
  al transicionar una práctica (no hay `onTransitioned` que refresque la
  raíz).
- **F7 (media).** `canEditContent` no considera cierre de periodo:
  `periodOpen` no aplica a `canEdit`/`packageEditable`/`canAddMore`.
  Verificar si el backend lo bloquea.
- **F12 (media).** `v-html` sobre texto capturado por la IES en
  `GoodPracticeCard.vue:134,141` — XSS almacenado. Cambiar a
  interpolación.
- Bajas: F4 doble-disparo sin guardia en `onSelect`; F5 spinner del
  split-button no refleja el POST de transición; F6 fallback de prompt
  (ver §3); F8 `order` ignorado por el frontend; F9 `ensureStatuses()`
  sin await (flash inicial); F10 ítems de menú no pre-deshabilitados
  cuando fallarán entry_rules; F11 acciones sin snackbar de éxito.

## 6. Decisiones tomadas (2026-07-03)

- a) Colores **sólidos** (no pasteles).
- b) `bp_discarded` → **"Descartada"** (femenino, natural con práctica).
- c) Flags emparejados: **todos los propuestos**, incluidos los envíos
  con confirm+comment_opt y comment_opt en aprobaciones. Extra no
  pedido pero coherente: `cp_resent` también (era el único envío sin
  confirmación) — vetable.
- d) Válvulas de escape: **NINGUNA** — ni bp (pocas prácticas) ni gen
  (vetado 2026-07-03: los generales alimentan el arranque de cp;
  reabrirlos después invalidaría lo que depende de ellos).
  `gen_approved`/`gen_finished` quedan como terminales absolutos.
  Solo cp conserva su válvula (`cp_voluntary_readjust`).
- e) Estructura del seed: **opción A** (StatusDef dataclass, estilo
  catalog_schema; grafo en dicts separados; `_validate()` anti-typos).
  Opción C (`export_flow_seed`) queda como S6 opcional.
- f) **El seed manda**: sobreescribe siempre color/icon/priority; el
  admin es solo para experimentar.
- g) Comentarios en terminales: se mantienen **cerrados**; el caso
  "Ya todo correcto" se cubre con `comment_opt` en la transición de
  aprobación (el mensaje viaja con el evento de aprobar).
- h) Seguridad B1–B5: subagente Opus 4.8 en la misma sesión.
- Hints: textos aprobados; el **rediseño visual** del hint en el
  frontend va a sesión aparte (S8).

## 7. Estado de ejecución y sesiones

| # | Alcance | Estado / Modelo |
|---|---|---|
| S1 | `seed.py` reescrito (estructura A + contenidos §1–§4) + fix `migrate_flow_data` (B8 + reconcile GeneralPackage) + confirmación de descarte desde catálogo en `GoodPracticeList` | **Hecho** (2026-07-03, Fable 5) |
| S2 | Seguridad B1–B5: ownership en flow/views y example, cablear `assign_auto_status`, lock | **Hecho** (2026-07-03, subagente Opus 4.8; 14 tests en `flow/tests.py`). Pendiente de revisión de Ricardo. Nota: el ViewSet de paquetes pasó de `IsAuthenticatedOrReadOnly` a `IsAuthenticated` — el GET anónimo ahora responde 401 (verificar que ninguna página pública lo consuma). La promoción a `cp_filling` (`assign_auto_status`) queda lista pero la vista de captura cp que debe llamarla aún no existe. |
| S4 | Frontend: F1 (hardcodeo bp_sent/bp_resent), F2 restante (discard/reopen vía motor o documentar), F3 (raíz stale tras propagación), F7 (`canEditContent` + periodo cerrado), F12 (v-html XSS en GoodPracticeCard) + bajas F4–F6, F9, F11 | **Hecho** (2026-07-03, Opus 4.8). Ver detalle abajo. |
| S5 | Notificaciones por cambio de turno. **Alcance final acotado** (decisiones 2026-07-03): solo se notifica a la **IES** (usuarios activos), nunca a revisoras, y solo sobre **objetos raíz** (`GoodPracticePackage`, `GeneralPackage`, `AxisValue`), cuando el turno vuelve a la IES (`to.role='ies'` y cambió) o se llega a un status final (`to.role=None`). En la práctica dispara: `bp_need_changes`, `bp_finished`, `cp_need_changes`, `cp_approved`, `gen_need_changes`, `gen_finished`. Señal `transition_executed` emitida por `execute_transition` (solo transición manual, no propagación); receptor `flow/notifications.py` que envía con `transaction.on_commit` (un fallo SMTP no revierte la transición) vía `send_simple_email` + plantilla `email/flow_notification.html` (asunto por status, comentario de la revisión en el cuerpo, enlace a `/respuestas/{año}`). Regla derivable: no hizo falta config en el seed ni mapa; la audiencia sale de `to.role or 'ies'` y el gate de "solo raíz" de `get_parent(obj) is None`. | **Hecho** (2026-07-03, Opus 4.8; 9 tests en `flow/tests.py`). Pendiente de revisión de Ricardo. |
| S6 (opc) | `export_flow_seed`: comando que regenera el bloque de datos del seed desde la BD (edición cómoda en admin → commit) | Opcional — Sonnet 5 |
| S7 (opc) | Test de sincronía motor/cliente (B9) + usar `priority` para ordenar colecciones en dashboard (hoy el frontend ignora `order`/`priority`) | Opcional — Sonnet 5 |
| S8 | Rediseño visual del hint y del diálogo de comentario en el frontend (presentación, no lógica: cómo se ve el hint bajo el chip y la caja de comentarios) | **Hecho** (2026-07-03, Fable 5) + F10 y B10 de paso. Ver detalle abajo. |

Nota S3: absorbida en S1 (mapeo gen `pre_start`/`filling` → `gen_draft`;
`GeneralPackage` NULL → `gen_draft` en un reconcile nuevo).

### Detalle de ejecución S4 (2026-07-03, Opus 4.8)

- **F12 (XSS)** `GoodPracticeCard.vue`: los dos `v-html` (descripción /
  resultados) pasan a interpolación `{{ }}` con `.pre-line`
  (`white-space: pre-line`) para conservar saltos.
- **F1** `GoodPracticeList.vue`: se elimina el `.find(name === bp_sent |
  bp_resent)`. `sendTransitions` = transiciones disponibles con
  `role === 'reviewer'` (las que ceden turno a la revisora), renderizadas
  como menú (`FlowTransitionMenu`). Decisión de Ricardo: menú con todas las
  transiciones; se reconcilió filtrando por rol porque mostrar
  `bp_discarded` crudo lo rutearía por el endpoint genérico (`transitions/`)
  en vez del custom `discard/`, dejando `has_good_practices` inconsistente.
  El descarte sigue exclusivamente en la UI Sí/No + endpoint `discard`.
- **F7** `GoodPracticeList.vue`: `canEdit` ahora exige `periodOpen`, que se
  propaga a `packageEditable`/`canAddMore`/`editingEditable`.
  **Follow-up backend (fuera de S4):** `GoodPracticeViewSet.update` NO valida
  periodo ni turno (a diferencia de `discard`/`reopen`, que sí). El candado
  de periodo vive hoy solo en el frontend; endurecer el backend queda
  pendiente (adyacente a S2/B1-B4).
- **F3** en ambas superficies: `GoodPracticeEditSimple` emite `transitioned`
  (desde `onTransitioned` del kernel). IES (`GoodPracticeList`) →
  `loadPractices`; revisora (`GoodPracticePackageEditSimple`) →
  `refetchPackage` (recarga el paquete y re-apunta la práctica abierta por
  id). `GoodPracticeEditDialog` reenvía el evento.
- **F4** `useFlowActions.onSelect`: guardia `if (sending.value) return null`.
- **F5** `GoodPracticeEditSimple`: split-button `:loading="loading ||
  sending"`.
- **F6** `FlowTransitionDialogs`: el fallback del prompt distingue
  `required` («Comentario (obligatorio)») de opcional.
- **F9** `middleware/dashboard.js`: `await ensureStatuses()` (middleware
  `async`) para evitar el flash de chips sin estilo.
- **F2/F11** `GoodPracticeList`: snackbars de éxito en `discard`/`reopen`.
- No abordadas (bajas fuera del alcance elegido): **F8** (`order`/`priority`
  ignorados por el frontend — vive en S7 opc) y **F10** (ítems de menú no
  pre-deshabilitados cuando fallarán `entry_rules`).
- Colateral: se corrigió un `Es` suelto en `flow/models.py:74`
  (`BooleanField(Es`), artefacto de un diff previo que rompía el import del
  backend; detectado por diagnósticos del IDE.

### Detalle de ejecución S8 + F10 + B10 (2026-07-03, Fable 5)

Dirección visual elegida por Ricardo sobre mockup comparativo (artifact):
hint **H3** (sensible al turno), historial **D1** (colapsado), caja de
comentario neutra con badge, alert de confirmación con color del destino.

- **Hint H3 + `hint_wait`:** nuevo campo `Status.hint_wait` (migración
  `flow/0008`) — variante del hint para el rol que NO tiene el turno;
  `hint` queda para quien sí lo tiene (terminales solo usan `hint`).
  Sembrados 27 `hint_wait` en `seed.py` (bp 7, cp 14, gen 6).
  `FlowStatusActions.vue`: tres modos — `mine` (callout ámbar, eyebrow
  "Te toca"), `theirs` (gris, "En espera de la revisión/institución",
  muestra `hint_wait || hint`), `terminal` (texto tenue sin caja).
- **Diálogo D1:** `ConfirmActionDialog` — caja de comentario en tonal
  gris (antes primary rojizo), badge Obligatorio/Opcional, y el slot
  `comment-history` movido DESPUÉS de la caja (la acción arriba);
  `FlowTransitionDialogs` — historial en `v-expansion-panels` colapsado
  con contador; alert de `confirm_text` en tonal con `color`/`icon` del
  status destino (antes warning fijo); fallback del prompt simplificado
  a «Escribe tu comentario.» (el badge ya distingue oblig./opcional).
- **F10:** `useFlowActions.transitions` adjunta `blocked` (entry_rules +
  regla de hijos) a cada transición; `FlowTransitionMenu` pre-deshabilita
  el ítem, ícono `lock` y los motivos como subtítulo. `onSelect`
  re-valida como red de seguridad.
- **B10:** eliminado el `print` de debug en `example/models.py`.
- Colateral: `bp_sent` declaraba `entry_rules=["package_ready"]` pero la
  regla ya no existe en `flowRules.js` (S4 la retiró); se quitó del seed
  — la compuerta real es `valid_child_statuses` (bp_completed).
- Pendiente: verificación visual de Ricardo en la app y re-sembrar
  (`seed_flow`) al desplegar.
