# Prompt para Fable 5 — refactorización del seed de `flow`

Copia el bloque de abajo en una conversación nueva con **Fable 5** (modelo
`claude-fable-5`), abierta en la raíz del monorepo `onigies`.

Contexto: el archivo `api/flow/seed.py` (~280 líneas) siembra el catálogo
completo de `Status` del motor de validación. Rubén lo señaló como «poco
legible» y hay varias inconsistencias de textos, colores, iconos y de un campo
de prioridad recién agregado. Esta refactorización se aisló a propósito para
que un solo modelo la trabaje de forma holística.

---

## Prompt

> Trabaja sobre `api/flow/seed.py` (y solo lo necesario alrededor). Antes de
> proponer nada, **lee** `api/flow/seed.py`, `api/flow/models.py` (modelo
> `Status`), la función `seed_flow()` y el diseño en
> `api/ies/flux_rules/PLAN_flujo_validacion.md`. Invoca también la skill
> `flow` para no romper el contrato del motor.
>
> **Objetivo:** proponerme (para revisión, sin aplicar migraciones ni
> re-seed automáticamente) una refactorización completa del seed que sea más
> legible y que corrija las inconsistencias de abajo. Preserva **al 100 %** el
> comportamiento del motor: los campos que `seed_flow()` escribe en `Status`
> vía `update_or_create`, el parseo del set `flags`
> (`comment`/`comment_opt`/`confirm`/`edit`/`up`/`down`/`auto`/`default`/
> `public`), las transiciones (`NEXT_STATUSES`), la regla de hijos
> (`VALID_CHILD_STATUSES`) y `applicable_models` deben seguir produciendo el
> mismo catálogo, salvo los cambios que te pido explícitamente.
>
> ### 1. Estructura (legibilidad)
> Hoy cada status se define en una tupla de 7 elementos
> `(name, public_name, action_name, description, role, flags, applies)` dentro
> de `STATUSES`, y el resto de atributos vive en **dicts paralelos** keyed por
> nombre: `CONFIRM_DIALOGS`, `COMMENT_PROMPTS`, `COMMENT_PROMPT_BY_ROLE`,
> `HINTS`, `ENTRY_RULES`, `ROLE_COLORS`, `NEXT_STATUSES`,
> `VALID_CHILD_STATUSES`. Esa dispersión es lo que hace ilegible el archivo.
> Propón una estructura donde **cada status quede definido en un solo lugar**
> (por ejemplo un `@dataclass` o un dict por status con defaults), reduciendo
> los dicts paralelos, sin sacrificar claridad ni volver el archivo más
> largo. Mantén `NEXT_STATUSES`/`VALID_CHILD_STATUSES` separados si conviene
> (son relaciones, no atributos escalares), pero justifícalo.
>
> ### 2. Campo `priority` (ya existe en el modelo, hoy default 0)
> Se agregó `Status.priority = IntegerField(default=0)` para ordenar
> colecciones por **urgencia** (mayor = más urgente, se muestra primero). El
> viewset `GoodPracticePackageViewSet` ya ordena por `-status__priority`.
> Asigna valores de `priority` a cada status. Semántica desde la perspectiva
> de la **revisora** en la colección «Envíos de buenas prácticas»: lo que
> requiere su acción primero (`bp_sent`, `bp_resent`) arriba; lo terminal
> (`bp_finished`) abajo; `bp_need_changes`/`bp_draft`/`bp_discarded` en medio.
> Rankea también `cp` y `gen` con criterio análogo. **Preferencia de
> estructura:** que `priority` viva **junto al status** (p. ej. como campo con
> default en la nueva estructura del punto 1), no en otro dict paralelo.
>
> ### 3. Colores (hoy derivados solo del rol → indistinguibles)
> En `seed_flow()` el color se asigna **solo al crear** desde `ROLE_COLORS`
> (`ies`→`blue-lighten-4`, `reviewer`→`deep-purple-lighten-4`, `None`→
> `yellow-lighten-3`). Consecuencia: todos los estados del mismo rol comparten
> color y no se distinguen entre sí; en particular **`bp_need_changes`
> («Requiere ajustes») se ve igual que `bp_draft`/`bp_discarded`**, cuando
> debería resaltar como algo que exige atención (un tono ámbar/naranja de
> alerta). Propón un esquema de color que permita **override por status**
> manteniendo un default por rol, y asigna colores distinguibles al menos a
> los estados accionables. Ojo: hoy el color solo se setea en `if created`
> (para preservar ediciones del frontend); decide si eso sigue teniendo
> sentido o si el color debe re-sincronizarse desde el seed.
>
> ### 4. Iconos (hoy ausentes → todos caen a `trip_origin`)
> El seed **nunca** asigna `Status.icon`, así que `FlowStatusChip` usa el
> fallback genérico `trip_origin` para todos. Asigna un icono de Material
> Symbols (nombre en snake/guiones, set `ms`) coherente a cada status
> (p. ej. borrador, enviado, requiere-ajustes, recibida, no-acreditada,
> finalizado).
>
> ### 5. Textos de comentario engañosos (obligatorio que suena opcional)
> `COMMENT_PROMPT_BY_ROLE` da por defecto «Si gustas, agrega un mensaje…»
> **incluso a los estados con `comment_type='required'`** (los que tienen el
> flag `comment`). Ej.: `bp_need_changes` es obligatorio (el botón se
> deshabilita sin texto y el label muestra «Comentario *») pero su prompt
> dice «Si gustas…». Separa los prompts por defecto de **obligatorio** vs
> **opcional**, con redacción imperativa para los obligatorios. Para
> `bp_need_changes` usa exactamente: **«Describe las correcciones que la
> institución debe atender.»** (ya aprobado). Revisa que ningún otro estado
> obligatorio herede un prompt opcional.
>
> ### 6. Restricciones (no te pases de aquí)
> - **No fijes la nomenclatura del §2** (Recibida / Requiere ajustes / No
>   acreditada / Ajuste realizado, y sus verbos): está pendiente de un taller
>   con Rubén. Puedes **señalar** discrepancias, pero no cierres nombres.
> - **No toques** el sistema viejo en coexistencia: `ies.StatusControl`,
>   `status_sending`, `status_register` siguen vivos hasta cerrar la
>   verificación de datos (plan §8).
> - **No ejecutes** `makemigrations`/`migrate`/`seed_flow`: solo propón el
>   diff y dime al final el comando de re-seed que debo correr yo, y si tu
>   cambio de estructura requiere o no migración.
> - Respeta las convenciones de `api/CLAUDE.md` (PEP 8, 80 columnas, type
>   hints, español con acentos).
>
> **Entregable:** el `seed.py` refactorizado propuesto (por partes, para que
> yo entienda cada bloque), la tabla de `priority`/`color`/`icon` por status
> que asignaste con su justificación, y la nota de re-seed/migración.

---

## Notas de contexto (no van en el prompt, son para ti)

- Todo esto salió de la sesión de pendientes de Rubén (§2, §3c, §3d, §4, §8).
- La infraestructura de `priority` (campo + migración `0007` + orden en el
  viewset) **ya está aplicada** en esta sesión; Fable solo asigna valores.
- La refactorización implica re-seed en producción; coordínalo con el deploy
  (recordar el *gotcha* del `migrate` partido del 26-jun).