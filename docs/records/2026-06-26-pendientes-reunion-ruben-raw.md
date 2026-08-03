---
type: record
id: 2026-06-26-pendientes-reunion-ruben-raw
title: Pendientes crudos de la reunión con Rubén
date: 2026-06-26
---

# Pendientes — reunión con Rubén (26 de junio de 2026)

Documento de trabajo derivado de la transcripción
[[2026-06-26-transcripcion-reunion-ruben]]. Concentra los acuerdos
sobre buenas prácticas (BP), la lógica de estados (Flow) y los siguientes
pasos. Marco con `[crítico]`, `[medio]` y `[bajo]` la prioridad estimada.

---

## 1. Bugs y correcciones de comportamiento

- **[crítico] Reenvío de paquete no funciona.** El botón dice «enviar a
  revisión» cuando debería decir «reenviar a revisión» y el flujo tendría que
  disparar el reenvío (proceso tipo *resend*). Es el único bug que Ricardo
  calificó como crítico; el resto son menores. `[00:24:03]`, `[00:45:24]`
- **Botón de envío ausente.** En la vista del paquete debería existir un botón
  «parecido a guardar, pero para enviar» que no aparece. `[00:12:59]`
- **Estatus viejo persistente.** En buenas prácticas aparece «enviado para
  revisar», que es el estatus anterior (`StatusControl`). Falta terminar el
  barrido a la nueva app `flow.Status`. `[00:18:26]`
- **Comentario editable del lado IES.** Cuando la IES ya no puede editar (el
  turno está del lado de la revisora), no debería poder agregar comentarios.
  Verificar. `[00:16:30]`

---

## 2. Nomenclatura de estados (buenas prácticas)

Acuerdo sobre los nombres finales. Recordar la distinción **verbo de acción**
(lo que hace la revisora/IES) vs. **estado resultante** (en el que queda la
BP); son dos redacciones distintas a propósito. `[00:28:40]`

| Acción (botón) | Estado resultante | Notas |
|---|---|---|
| Marcar como recibida | Recibida | Se quita «para dictamen». La plataforma no llega al nivel de dictamen (eso se hace «casero»). `[00:03:57]`, `[00:04:23]` |
| Solicitar ajustes | Requiere ajustes | Exige mensaje obligatorio para la institución. `[00:10:03]` |
| Marcar como no acreditada | No acreditada | No hay estado «aprobada». `[00:04:05]` |
| Marcar como atendido (lado IES) | Ajuste realizado | Sustituye a «marcar como ajuste completo», que quedaba raro. `[00:23:31]` |

**Pendiente de aplicar:**
- Renombrar los estados/verbos según la tabla.
- Falta **icono** para el estado «recibida» (y revisar iconos en general).
  `[00:04:31]`

**Contexto metodológico (para textos y ayuda):** todas las BP que cumplan la
definición se **admiten** e ingresan al directorio de buenas prácticas; el
comité experto define aparte, por eje, la «destacada» (mención honorífica).
La plataforma solo llega hasta «recibida». `[00:01:39]`, `[00:03:10]`

---

## 3. UX y visualización

- **[medio] Justificación en formato legible.** Hoy se muestra «en azulito» y
  se ve raro sin textos largos. Rediseñar a un formato más legible.
  `[00:06:43]`
- **[medio] Textarea de ajustes con alto automático.** Poner `height: auto`
  para que no quede incómodo con textos largos. `[00:19:01]`
- **Color de «requiere ajustes».** No se distingue; cambiar el color.
  `[00:16:00]`
- **Asterisco de comentario obligatorio.** El asterisco muestra «si gustas»
  pero el comentario es obligatorio (el botón no se activa sin él). El texto
  contradice la regla; corregir la redacción. `[00:14:36]`
- **Ordenar por estatus (más urgentes primero).** Pendiente de reajustar
  porque cambió por completo la lógica de estados. `[00:15:00]`
- **Ocultar puntuaciones a la IES.** Confirmado: las escalas que puntúa la
  revisora (p. ej. «cumple poco») **no** las ve la institución. Mantener.
  `[00:17:11]`

---

## 4. Funcionalidad nueva

- **[medio] Vigencia de la práctica.** Agregar opción «¿mi práctica sigue
  vigente?» con rango del año 2022 a «sigue presente». Las instituciones lo
  piden con insistencia. `[00:05:07]`, `[00:05:58]`
- **Notificaciones por correo.** Agregar al motor de flujos: cuando cambien
  los estatus de los **agrupadores (padres)**, enviar un correo **genérico**
  del tipo «has recibido comentarios, entra aquí para revisarlos». Sin
  detallar la observación. `[00:33:07]`, `[00:34:01]`
- **[medio] Exportación a Excel de puntuaciones.** Una columna por criterio
  con el **número** (no la etiqueta), más institución, año y descripción. Sirve
  para que Rubén jerarquice y entregue a las expertas (que no tendrán cuenta)
  las ~10 mejores prácticas. `[00:51:31]`, `[00:52:41]` — visualización
  (valores en el header) queda para después.
- **Edición de reglas desde el dashboard.** Volver editables en vivo las
  definiciones de los 32 estados (nombre, verbo, descripción, reglas de
  confirmación/comentario y relaciones padre-hijo). Hoy viven en un archivo de
  ~280 líneas poco legible. `[00:50:27]`

---

## 5. Infraestructura

- **[crítico] Conflicto de `media` con el ONIGIES anterior.** El `media` de la
  v2 choca con el `media` del sistema legado que convive en producción
  (`onigies.unam.mx`). Investigar cambiar la ruta de `media` a **`files`** para
  la versión 2 y evitar la colisión de archivos/probatorios. `[00:07:12]`,
  `[00:08:23]`

---

## 6. Cuestionario (preguntas iniciales y específicas)

- Rubén envía el **cuestionario actualizado** (cambios de sintaxis/claridad,
  la estructura es la misma) para trabajar sobre una versión real. `[00:35:19]`,
  `[00:42:50]`
- **Quitar el número de versión** en la visualización (sí conservar orden 1, 2,
  3 internamente). `[00:35:33]`
- La **numeración visible** solo a nivel de **observable**; las demás preguntas
  son de muchos tipos y numerarlas sería confuso. `[00:36:20]`
- Ricardo mostrará cómo se despliegan las preguntas iniciales y específicas en
  la próxima reunión; el motor ya está construido. `[00:34:43]`

---

## 7. Diferido (no ahora)

- **Asignación de revisoras a BP.** No estará en base de datos por ahora; cada
  quien lleva su lista aparte. Se retoma junto con la revisión de observables.
  `[00:30:33]`
- **Directorio/visualización de buenas prácticas aceptadas** (listados con
  cuatro apartados, la destacada al principio). Más adelante. `[00:48:24]`

---

## 8. Decisiones pendientes (requieren definición conjunta / de Rubén)

- **Taller de configuración de estados.** Recorrer cada uno de los 32 estados
  y definir: ¿requiere comentario?, ¿requiere confirmación?, ¿cuál es el
  mensaje de confirmación? El reenvío, por ejemplo, no tenía validación de
  confirmación. `[00:25:26]`, `[00:27:05]`
- **Escala del índice: 0–10 vs. 0–5.** Rubén se inclina por 0–10 (marcar
  diferencia con la metodología anterior, no comparable); Ricardo prefiere
  0–5. Sin consenso aún. `[00:37:41]`
- **Ecuación del índice de avance y agregación.** Falta decidir cómo se agrupa
  la información (¿agregación por componente?). Rubén consultará a más personas.
  `[00:36:37]`
- **Condiciones base.** Rubén preseleccionó ~10 de 40 variables (con al menos
  una por eje) bajo el nombre «medición de condiciones iniciales para la
  igualdad»; lo confirmará con Norma, Leti e Isabela. `[00:39:26]`
- **¿Comentario obligatorio al marcar «atendido» por la IES?** Hoy es opcional;
  se puede volver obligatorio. Por definir. `[00:21:01]`

---

## 9. Calendario

- No hay reunión el martes (partido de México). Próxima posible: **lunes** a
  las 16:00 (o miércoles). `[00:34:25]`, `[00:53:42]`
- **Rubén entrega:** cuestionario actualizado (por WhatsApp).
- **Ricardo entrega la próxima vez:** despliegue de preguntas iniciales y
  específicas. `[00:34:43]`