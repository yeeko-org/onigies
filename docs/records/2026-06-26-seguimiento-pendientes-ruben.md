---
type: record
id: 2026-06-26-seguimiento-pendientes-ruben
title: Seguimiento de los acuerdos de la reunión con Rubén
date: 2026-06-26
---

# Seguimiento de pendientes — reunión Rubén (26 jun 2026)

Estado de avance de los acuerdos de la reunión. Fuente completa (sin editar):
[[2026-06-26-pendientes-reunion-ruben-raw]].

**Leyenda:**
`[x]` hecho · `[ ]` pendiente ·
🟠 **Fable** (refactor de `seed.py`, ver
[[2026-07-03-prompt-a-fable-refactor-del-seed]]) ·
🟣 **Rubén** (decisión/definición conjunta) ·
🔵 sesión aparte.

---

## Sesión del 3 de julio — §1 + §3

Alcance acordado: bugs de comportamiento (§1, sin el renombrado §2) y retoques
de UX (§3).

### §1 — Bugs y comportamiento
- [x] **Reenvío de paquete (crítico).** `sendTransition` resuelve
  `bp_sent`/`bp_resent` según el estado; label y disparo derivan de ahí.
  `GoodPracticeList.vue`.
- [x] **Botón de envío ausente.** Era el CTA «Enviar evaluación» de la
  revisora: `flowActions.transitions` (ref anidado) no se desenvolvía en el
  template. Desestructurado. `GoodPracticePackageEditSimple.vue`.
- [x] **Estatus viejo persistente.** `StatusChip` viejo → `FlowStatusChip` en
  `/respuestas`. `pages/respuestas/index.vue`.
- [x] **Comentario editable del lado IES fuera de turno.**
  - [x] Front: `canComment` por turno oculta la caja. `FlowComments.vue`.
  - [x] Back: guard simétrico 403. `flow/views.py`.

### §3 — UX y visualización
- [x] **Justificación en formato legible.** Texto plano `text-body-1`,
  respeta saltos. `FeatureItem.vue`.
- [x] **Textarea con alto automático.** `auto-grow` + `max-rows="20"` en los
  4 textareas de captura IES (`FeatureItem`, `NewGoodPractice`,
  `GoodPracticeEditSimple` ×2).
- [x] **Ocultar puntuaciones a la IES.** Confirmado ya protegido en UI +
  payload; verificado, sin cambios.
- [x] **Ordenar por estatus (más urgentes primero).**
  - [x] Infra: campo `priority` en `flow.Status` + migración `0007` aplicada +
    orden por defecto `-status__priority` en `GoodPracticePackageViewSet`.
  - [x] 🟠 Valores de `priority` y estructura del seed → Fable.
- [x] 🟠 **Color de «requiere ajustes».** Hoy el color se deriva del rol, así
  que `bp_need_changes` no se distingue. → Fable.
- [x] 🟠 **Asterisco de comentario obligatorio engañoso.** Prompt «si gustas»
  en estados obligatorios. → Fable.

### Entregable de la sesión
- [x] **Prompt para Fable 5** con las observaciones del seed (colores,
  iconos, prompts obligatorios, valores de `priority`, estructura).
  [[2026-07-03-prompt-a-fable-refactor-del-seed]].

---

## Pendiente de hacer juntos

### §2 — Nomenclatura de estados
- [x] 🟣 **Renombrar estados/verbos** según la tabla acordada (Recibida /
  Requiere ajustes / No acreditada / Ajuste realizado). Depende del taller §8.
- [x] 🟠 **Icono para «recibida»** (y revisar iconos en general). → Fable.

### §4 — Funcionalidad nueva
- [ ] 🔵 **Vigencia de la práctica.** «¿Sigue vigente?», rango 2022 → presente.
- [x] 🔵 **Notificaciones por correo.** Al cambiar el estatus de los
  agrupadores (padres), correo genérico «tienes comentarios».
- [ ] 🔵 **Exportación a Excel de puntuaciones.** Una columna por criterio con
  el número, más institución, año y descripción.

### §5 — Infraestructura
- [ ] 🔵 **`media` → `files` (crítico).** Evitar la colisión con el ONIGIES
  legado en producción.
  - [x] Código: `MEDIA_URL=/files/` + `MEDIA_ROOT=.../files`; ruta `serve`
    explícita en `core/urls.py` (sirve con `DEBUG=False`); URLs de archivo
    absolutas en `example` y `flow` — el navegador pide directo a
    `apionigies.yeeko.org/files/...`, nginx queda fuera del camino.
  - [x] Servidor: carpeta `media/` → `files/` movida y API recargado
    (2026-07-29); la copia vieja quedó en `api/_backups/files_stale_jul04`.

### §6 — Cuestionario
- [ ] 🔵 Integrar el **cuestionario actualizado** de Rubén.
- [ ] 🔵 **Quitar el número de versión** en la visualización (conservar orden
  interno).
- [ ] 🔵 **Numeración visible solo a nivel de observable.**
- [ ] **Mostrar a Rubén** el despliegue de preguntas iniciales y específicas
  (compromiso para la próxima reunión).

---

## Diferido y decisiones de Rubén

### §7 — Diferido
- [ ] 🔵 Asignación de revisoras a BP (se retoma con la revisión de
  observables).
- [ ] 🔵 Directorio/visualización de buenas prácticas aceptadas.

### §8 — Decisiones que requieren a Rubén
- [ ] 🟣 **Taller de configuración de estados** (comentario/confirmación/mensaje
  por estado). Insumo directo para §2 y para Fable.
- [ ] 🟣 Escala del índice: **0–10 vs. 0–5**.
- [ ] 🟣 Ecuación del índice de avance y agregación.
- [ ] 🟣 Condiciones base (~10 de 40 variables).
- [ ] 🟣 ¿Comentario obligatorio al marcar «atendido» por la IES?