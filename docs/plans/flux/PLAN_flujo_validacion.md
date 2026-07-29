# Plan — Motor de flujo de validación (sesión backend)

Estado: **especificación v2 aprobada, pendiente de ejecutar en sesión nueva.**
Fuente de verdad del flujo: `analysis.json` (extraído del board de Miró) +
las correcciones y decisiones de este documento.

Alcance: **solo backend** — modelos del motor de reglas, timeline genérico,
adjuntos genéricos, seed, migración de datos y admin. El motor de ejecución
(servicios/endpoints que validan transiciones y propagan) y el frontend son
sesiones posteriores.

---

## 0. Decisiones tomadas (v2)

- **Migración gradual con modelo paralelo.** Se crea `flow.Status` con su
  nombre definitivo desde el día uno; coexiste con `ies.StatusControl` hasta
  verificar los datos. **No hay rename ni `SeparateDatabaseAndState`** — el
  §8 del plan v1 se elimina: el modelo viejo simplemente se borra al final.
- **Sin `FlowModel`.** La aplicabilidad status×modelo usa
  `M2M(ContentType)`; la jerarquía padre-hijo y el grupo de cada modelo
  viven en un registry de código (`flow/registry.py`), porque el vínculo
  `AxisValue ↔ ObservableResponse` no tiene FK y requiere código de todos
  modos. `Collection` (ps_schema) **no** se reutiliza: solo 2 de los 6
  modelos están registrados como colecciones y ps_schema debe permanecer
  desacoplado del proyecto.
- **Sin `StatusTransition` ni `ParentChildRule`.** Verificado contra las 37
  transiciones del board: `transition.role == from_status.role` en el 100%
  de los casos. Ambos modelos colapsan en dos M2M autorreferentes de
  `Status` (`next_statuses`, `valid_child_statuses`).
- **`role` nullable reemplaza a `is_terminal`.** El color del rectángulo en
  Miró significa "de quién es el turno" (quién ejecuta las transiciones de
  salida). Los terminales (amarillos) no tienen salidas: `role=None`.
- **Ids con prefijo uniforme** `bp_` / `cp_` / `gen_` en TODOS los status.
  Ya no se conserva ningún id de producción (el script de migración mapea).
  El "naming reconciliado" del plan v1 queda obsoleto.
- **PK del nuevo `Status` sigue siendo `name`** (CharField) — consistente
  con `Collection` y `Period`; el frontend compara strings legibles.
- **Campos que NO pasan al modelo nuevo:** `can_send` (solo lo escribía el
  seed viejo), `priority` (solo el admin), `is_final` (sustituido por
  `role=None`), `recalc` (duplicado de `propagates_up`: en el board
  `recalc='up'` ⟺ `upward_propagation` y `'down'` no se usa), `miro_id`
  (el board fue insumo de diseño; los cambios futuros van por admin).
- **`auto_on_first_save` se conserva** (ex `computed_on_first_save`). NO
  duplica a `propagates_up`: "Solicitar reajuste voluntario" propaga hacia
  arriba pero es acción manual. Uno dice *cuándo se asigna* (al primer
  guardado), el otro *qué pasa al asignarse* (sube al padre).
- **`is_public` nuevo** (rescatado del comentario en el modelo viejo):
  controla qué registros se muestran en la página pública según su status.
- **Timeline:** el modelo se llama `FlowEvent` (no `StatusEvent`: también
  registra comentarios puros). Pierde el FK `transition` (ya no existe el
  modelo).
- **D (se mantiene de v1)** — no se guarda el `role` con que se actuó; se
  deriva de `user.is_reviewer`.
- `GROUP_CHOICES` nuevos, alineados con los prefijos:
  `[("bp", "Buenas prácticas"), ("cp", "Cuestionario principal"), ("gen", "Preguntas generales")]`.
- `ROLE_CHOICES`: `[("reviewer", "Revisora"), ("ies", "Institución")]`,
  null/blank permitido (None = terminal).

### Regla de lectura del board (sin cambios)

- Texto entre paréntesis `( … )` → `description`.
- Texto entre corchetes `[ … ]` → flag (`requires_comment`,
  `auto_on_first_save`).
- **Corrección de dirección en `dependencies[]`:** `from_id` es el status
  del **hijo**, `to_id` el del **padre**. Es decir: el padre puede estar en
  `to_id` cuando todos sus hijos están en alguno de los `from_id`.

---

## 1. Jerarquía padre-hijo (registry de código)

```
Cuestionario (cp):  AxisValue (A) → ObservableResponse (O) → GroupResponse (G)
Buenas prácticas (bp):  GoodPracticePackage (P) → GoodPractice (G)
Generales (gen):  GeneralGroupResponse (sin jerarquía)
```

- `GoodPractice.package` y `GroupResponse.observable_response` son FK
  directos.
- **`AxisValue ↔ ObservableResponse` NO tiene FK.** El padre de un
  `ObservableResponse` es el `AxisValue` del mismo `survey` con
  `axis = observable.component.axis`.
- `ComponentValue` **no participa** del flujo. Anotar en `api/CLAUDE.md`.

`flow/registry.py` declara, por modelo participante: su `group`, y cómo
resolver padre e hijos (atributo directo o callable para el caso
AxisValue↔Observable). Es la única fuente de verdad de la topología — no se
duplica en BD porque es estructural, no configuración.

---

## 2. App `flow` — modelos (`api/flow/models.py`)

### 2.1 `Status`

```python
GROUP_CHOICES = [
    ("bp", "Buenas prácticas"),
    ("cp", "Cuestionario principal"),
    ("gen", "Preguntas generales"),
]
ROLE_CHOICES = [
    ("reviewer", "Revisora"),
    ("ies", "Institución"),
]

class Status(models.Model):
    name = CharField(max_length=120, primary_key=True)   # bp_draft, cp_filling…
    group = CharField(max_length=10, choices=GROUP_CHOICES)
    public_name = CharField(max_length=255)
    description = TextField(blank=True, null=True)
    color = CharField(max_length=30, blank=True, null=True)   # vuetify color
    icon = CharField(max_length=40, blank=True, null=True)    # material icon
    order = IntegerField(default=4)
    is_default = BooleanField(default=False)
    is_public = BooleanField(
        default=False,
        help_text="Los registros en este status se muestran en la página pública")
    # None = status terminal (nadie lo mueve); si tiene valor, indica de
    # quién es el turno: quién puede ejecutar las transiciones de salida.
    role = CharField(max_length=10, choices=ROLE_CHOICES, blank=True, null=True)
    requires_comment = BooleanField(default=False)
    propagates_up = BooleanField(default=False)
    auto_on_first_save = BooleanField(default=False)

    applicable_models = M2M(ContentType, blank=True,
                            related_name='applicable_statuses')
    next_statuses = M2M('self', symmetrical=False, blank=True,
                        related_name='previous_statuses')
    # Para mover el PADRE a este status, TODOS sus hijos deben estar en
    # alguno de estos. Auto-loops permitidos (Aprobado ← Aprobado).
    valid_child_statuses = M2M('self', symmetrical=False, blank=True,
                               related_name='valid_for_parent_statuses')

    class Meta:
        constraints = [UniqueConstraint(
            fields=['group'], condition=Q(is_default=True),
            name='unique_default_per_group')]
        ordering = ["group", "order"]
```

Notas:

- El motor valida una transición con: `target ∈ origen.next_statuses` ∧
  `user` cumple `origen.role` ∧ `target.applicable_models` contiene el
  modelo del objeto ∧ regla de hijos de `target.valid_child_statuses`.
- Un default por grupo, garantizado por el `UniqueConstraint` condicional.

### 2.2 `FlowEvent` (timeline: cambios de status + comentarios)

```python
class FlowEvent(models.Model):
    content_type = FK(ContentType); object_id = PositiveIntegerField()
    target       = GenericForeignKey('content_type', 'object_id')
    from_status  = FK(Status, null=True, related_name='+')  # null al crear
    to_status    = FK(Status, null=True, related_name='+')  # null = comentario puro
    user         = FK(User)
    comment      = TextField(blank=True, null=True)
    created_at   = DateTimeField(auto_now_add=True)
```

Reemplaza a `ObservableComment`, `GroupComment`, `GeneralGroupComment` y al
`TextField comments` de `GoodPracticePackage` / `GoodPractice` /
`FeatureGoodPractice`.

### 2.3 `Attachment` (adjuntos genéricos)

```python
class Attachment(models.Model):
    content_type = FK(ContentType); object_id = PositiveIntegerField()
    target       = GenericForeignKey('content_type', 'object_id')
    file         = FileField(upload_to=resolve_upload_path)
    event        = FK(FlowEvent, null=True, blank=True)
    uploaded_by  = FK(User, null=True)
    created_at   = DateTimeField(auto_now_add=True)
```

Reemplaza `GroupAttachment`, `GeneralGroupAttachment`, `Evidence`.
`resolve_upload_path` (en `api/flow/upload_paths.py`) reconstruye la ruta
según el tipo de `target`, reusando la lógica de
`set_upload_attachment_path` y `set_upload_general_attachment_path`.

---

## 3. Catálogo de status (seed)

`is_public=True` solo en `bp_for_ruling`, `cp_approved`, `gen_approved`
(ajustable en admin). Sin valor en "role" = terminal.

### 3.1 Buenas prácticas (`bp`) — P = GoodPracticePackage, G = GoodPractice

| id | public_name | description | role | flags | aplica |
|---|---|---|---|---|---|
| `bp_draft` | Borrador | En captura; la IES puede editar libremente. | ies | default | P, G |
| `bp_completed` | Completada | La IES la marcó como completa; se revisará cuando se envíe el paquete. | reviewer | — | G |
| `bp_sent` | Enviado | Paquete enviado; las prácticas están en revisión. | reviewer | — | P |
| `bp_need_changes` | Requiere ajustes | La revisión solicitó correcciones a la IES. | ies | requires_comment | P, G |
| `bp_adjusted` | Ajuste completo | Correcciones incorporadas; en espera de nueva revisión. | reviewer | — | G |
| `bp_resent` | Enviado con ajustes | Paquete reenviado tras incorporar las correcciones. | reviewer | — | P |
| `bp_for_ruling` | Recibida para dictamen | Cumplió los criterios; pasa a la etapa de dictamen. | — | is_public | G |
| `bp_rejected` | No pasó los filtros | Recibida, pero no cumplió los criterios mínimos de la convocatoria. | — | requires_comment | G |
| `bp_finished` | Finalizado | Revisión del paquete concluida; sin acciones pendientes. | — | — | P |

> `requires_comment` en `bp_need_changes` no está en el board pero sí en su
> equivalente de `cp`; se asume omisión del board (decidido: se agrega).

**Transiciones bp** (`next_statuses`):

```
bp_draft        → bp_completed, bp_sent
bp_completed    → bp_need_changes, bp_for_ruling, bp_rejected
bp_adjusted     → bp_need_changes, bp_for_ruling, bp_rejected
bp_need_changes → bp_adjusted, bp_resent
bp_sent         → bp_finished
bp_resent       → bp_finished
```

**Reglas padre-hijo bp** (`valid_child_statuses`, padre ← hijos en):

```
bp_sent     ← bp_completed
bp_resent   ← bp_adjusted, bp_completed
bp_finished ← bp_for_ruling, bp_rejected
```

### 3.2 Cuestionario principal (`cp`) — A = AxisValue, O = ObservableResponse, G = GroupResponse

| id | public_name | description | role | flags | aplica |
|---|---|---|---|---|---|
| `cp_pre_start` | Por iniciar | Aún no se captura ninguna respuesta. | ies | default | A, O, G |
| `cp_filling` | En llenado | Captura en curso por la IES. | ies | auto_on_first_save, propagates_up | A, O, G |
| `cp_completed` | Completado | Terminado por la IES; en espera de revisión. | reviewer | — | O, G |
| `cp_sent` | Enviado | Eje enviado para revisión. | reviewer | — | A |
| `cp_in_review` | En revisión | La revisión del eje está en curso. | reviewer | — | A |
| `cp_need_changes` | Requiere ajustes | La revisión solicitó correcciones a la IES. | ies | requires_comment | A, O, G |
| `cp_in_adjustment` | En ajustes | Captura de correcciones en curso. | ies | auto_on_first_save, propagates_up | A, O, G |
| `cp_adjusted` | Ajuste completo | Correcciones incorporadas; en espera de nueva revisión. | reviewer | — | O, G |
| `cp_resent` | Enviado con ajustes | Eje reenviado tras incorporar las correcciones. | reviewer | — | A |
| `cp_postponed` | Pospuesta | La IES decidió responder esto más adelante. | ies | — | O, G |
| `cp_voluntary_readjust` | Reajuste voluntario solicitado | La IES pidió reabrir una respuesta ya aprobada. | reviewer | requires_comment, propagates_up | A, O, G |
| `cp_partial` | Parcialmente respondido | Hay respuestas listas para corroborar mientras el resto sigue en captura. | reviewer | requires_comment | O, G |
| `cp_partial_approved` | Parcialmente aprobado | La parte entregada fue validada; el resto sigue pendiente. | ies | — | O, G |
| `cp_approved` | Aprobado | Respuesta validada por la revisión. | ies | is_public | A, O, G |

> `cp_approved` con role `ies` no es errata: su única salida (solicitar
> reajuste voluntario) la ejecuta la IES. El board es consistente en esto.

**Transiciones cp:**

```
cp_pre_start         → cp_filling
cp_filling           → cp_completed, cp_sent, cp_postponed, cp_partial
cp_completed         → cp_approved, cp_need_changes
cp_sent              → cp_in_review
cp_in_review         → cp_approved, cp_need_changes
cp_adjusted          → cp_approved, cp_need_changes
cp_resent            → cp_in_review
cp_postponed         → cp_completed, cp_partial
cp_approved          → cp_voluntary_readjust
cp_voluntary_readjust → cp_need_changes
cp_need_changes      → cp_in_adjustment
cp_in_adjustment     → cp_adjusted, cp_resent, cp_postponed
cp_partial           → cp_need_changes, cp_partial_approved
cp_partial_approved  → cp_completed, cp_partial
```

**Reglas padre-hijo cp** (dirección ya corregida; incluye auto-loops):

```
cp_approved         ← cp_approved
cp_completed        ← cp_completed
cp_adjusted         ← cp_adjusted, cp_completed, cp_approved
cp_sent             ← cp_completed, cp_postponed, cp_partial
cp_resent           ← cp_completed, cp_adjusted, cp_approved, cp_postponed, cp_partial
cp_need_changes     ← cp_need_changes, cp_approved, cp_postponed
cp_partial          ← cp_completed, cp_postponed
cp_partial_approved ← cp_partial_approved
```

### 3.3 Generales (`gen`) — GeneralGroupResponse (un solo nivel)

Diseñado en esta versión (no existe en Miró). Sin propagación ni reglas
padre-hijo. `gen_adjusted` permite a la revisora distinguir primera entrega
de reentrega. `gen_approved` es reabrible por la revisora (válvula de
escape) en lugar de terminal puro.

| id | public_name | description | role | flags |
|---|---|---|---|---|
| `gen_pre_start` | Por iniciar | Aún no se captura ninguna respuesta. | ies | default |
| `gen_filling` | En llenado | Captura en curso por la IES. | ies | auto_on_first_save |
| `gen_completed` | Completado | La IES terminó; en espera de revisión. | reviewer | — |
| `gen_need_changes` | Requiere ajustes | La revisión encontró puntos por corregir. | ies | requires_comment |
| `gen_adjusted` | Ajuste completo | Correcciones incorporadas; en espera de nueva revisión. | reviewer | — |
| `gen_approved` | Aprobado | Respuestas validadas por la revisión. | reviewer | is_public |

**Transiciones gen:**

```
gen_pre_start    → gen_filling
gen_filling      → gen_completed
gen_completed    → gen_approved, gen_need_changes
gen_need_changes → gen_adjusted
gen_adjusted     → gen_approved, gen_need_changes
gen_approved     → gen_need_changes        (reapertura)
```

---

## 4. Seed (`api/flow/seed.py`)

Idempotente por PK (`name`); los M2M se reconstruyen con `clear()` + `add()`.
No reemplaza a `InitStatus` (que sigue alimentando al `StatusControl` viejo
durante la coexistencia); se llama por separado desde `initial_data` o un
management command. Siembra:

1. Los `Status` de las tablas §3 (con flags, `is_public`, colores/iconos
   heredables de los equivalentes viejos donde existan).
2. `applicable_models` (ContentTypes de los 6 modelos).
3. `next_statuses` y `valid_child_statuses` según §3.

---

## 5. Modelos existentes — fase de coexistencia

A los 6 modelos se les **agrega** (sin tocar lo viejo):

```python
status = FK('flow.Status', null=True, blank=True, on_delete=PROTECT,
            related_name='+')
```

- `api/answer/models.py`: `ObservableResponse`, `GroupResponse` + campo
  `status` + `GenericRelation(FlowEvent)` y `GenericRelation(Attachment)`.
- `api/survey/models.py`: `AxisValue`, `GeneralGroupResponse` ídem.
- `api/example/models.py`: `GoodPracticePackage`, `GoodPractice` ídem.
- `api/ies/models.py`: `Institution.save()` setea **ambos** campos durante
  la coexistencia: los viejos (`status_register_id='pre_start'`,
  `status_sending_id='draft'`) y los nuevos (`status_id='cp_pre_start'` /
  `'bp_draft'`).
- `api/core/settings/__init__.py`: registrar `flow` en `INSTALLED_APPS`.
- `api/CLAUDE.md`: nota de que `ComponentValue` no es parada de validación.

Los modelos viejos de comentarios/adjuntos y los campos `status_register` /
`status_sending` **no se tocan** hasta la fase de borrado (§8).

---

## 6. Script de migración de datos (`api/flow/management/commands/migrate_flow_data.py`)

Management command idempotente (re-ejecutable). Dos partes:

**a) Status** — mapeo `(modelo, id viejo) → id nuevo`:

| modelo | viejo | nuevo |
|---|---|---|
| GoodPractice | `draft` | `bp_draft` |
| GoodPractice | `ready_to_send` | `bp_completed` |
| GoodPracticePackage | `draft` | `bp_draft` |
| GoodPracticePackage | `ready_to_send` | `bp_draft` (listo pero no enviado) |
| GoodPracticePackage | `created` | `bp_sent` |
| A/O/G (register) | `pre_start` | `cp_pre_start` |
| A/O/G (register) | `filling` | `cp_filling` |
| A/O/G (register) | `sent` | `cp_sent` |
| A/O/G (register) | `need_changes` | `cp_need_changes` |
| A/O/G (register) | `approved` | `cp_approved` |
| A/O/G (register) | `requires_new_checking` | `cp_in_review` |
| GeneralGroupResponse | `pre_start`… | `gen_pre_start`… (mismo patrón) |

Producción solo tiene buenas prácticas (`draft` / `ready_to_send`), pero el
script cubre todos los modelos para entornos locales. Status viejos de
`sending` sin uso (`in_review`, `needs_adjustments`, `ready_to_resend`,
`need_new_checking`, `accepted`, `discarded`) se reportan si aparecen en
datos, sin migrarse — decisión manual.

**b) Comentarios y adjuntos** — copia (no mueve) a los genéricos:

- `ObservableComment`, `GroupComment`, `GeneralGroupComment` → `FlowEvent`
  (comentario puro: `to_status=None`).
- `comments` (TextField) de `GoodPracticePackage` / `GoodPractice` /
  `FeatureGoodPractice` → `FlowEvent` con `user` = un staff designado.
- `GroupAttachment`, `GeneralGroupAttachment`, `Evidence` → `Attachment`
  (mismo path de archivo, sin recopiar el archivo físico).

Al final imprime conteos viejo vs nuevo para verificación.

---

## 7. Admin (`api/flow/admin.py`)

- `StatusAdmin`: `list_display` con `group`, `name`, `public_name`, `role`,
  flags; `list_editable` para `order`, `color`, `icon`, `is_public`;
  `list_filter` por `group` y `role`; `filter_horizontal` para los 3 M2M
  (`applicable_models`, `next_statuses`, `valid_child_statuses`).
- `FlowEventAdmin`: solo lectura (es bitácora) — `list_display` con target,
  from/to, user, fecha; `list_filter` por `to_status`; sin add/change.
- `AttachmentAdmin`: lectura + delete; link al evento.
- El admin del `StatusControl` viejo se conserva hasta la fase de borrado.

---

## 8. Fase de borrado (solo tras verificar §6 en producción)

1. Quitar `status_register` / `status_sending` de los 6 modelos.
2. Borrar `ObservableComment`, `GroupComment`, `GroupAttachment`,
   `GeneralGroupComment`, `GeneralGroupAttachment`, `Evidence`, el `Comment`
   abstracto y los helpers de upload path viejos.
3. Quitar `comments` (TextField) de los 3 modelos de `example`; quitar el
   `print("is_create:", ...)` de `GoodPractice.save()`.
4. Borrar `ies.StatusControl`, su admin, `InitStatus` y sus
   `GROUP_CHOICES`/`ROLE_CHOICES`; simplificar `Institution.save()` (solo
   campos nuevos).
5. Actualizar `api/api/views/example/__init__.py` — el filtro
   `status_sending__is_final=False` pasa a `status__role__isnull=False`.

---

## 9. Migraciones (las corre Ricardo)

1. `flow` inicial: `Status`, `FlowEvent`, `Attachment`.
2. Campo `status` + `GenericRelation`s en los 6 modelos (una migración por
   app: `answer`, `survey`, `example`).
3. (Sin migración de esquema) correr el seed y `migrate_flow_data`.
4. **Checkpoint de verificación** — admin / conteos / API en paralelo.
5. Migraciones de borrado (§8), una por app.

> Nunca ejecutar `makemigrations`/`migrate` desde el asistente.

---

## 10. Secuencia de commits sugerida

1. App `flow`: modelos + registry de jerarquía + seed + admin.
2. Campo `status` nuevo + `GenericRelation`s + `Institution.save()` dual.
3. Script `migrate_flow_data` + ejecución local + verificación.
4. (Tras verificar en producción) fase de borrado §8 + nota en `CLAUDE.md`.

---

## 11. Deuda frontend (documentar, no arreglar en esta sesión)

- Ids de status renombrados: `draft` → `bp_draft`, `ready_to_send` →
  `bp_completed`, `created` → `bp_sent`, `pre_start` → `cp_pre_start`, etc.
  Todo lo que compare strings de status (p. ej. `GoodPracticeList`) debe
  actualizarse al mapa nuevo.
- Campo `status_sending` / `status_register` → `status` en los payloads
  cuando los serializers se actualicen (la coexistencia permite exponer
  ambos temporalmente).
- `role`: los valores pasan de `validator` → `reviewer`; la comparación
  `role === 'ies'` sigue siendo válida.
- El catálogo de status que consume el frontend cambiará de endpoint/shape
  (vendrá de `flow.Status`, con `next_statuses` para pintar acciones
  disponibles).
- Las acciones actuales `reopen` / `send` / `discard` del frontend de BP no
  existen como tales en el flujo nuevo — rediseñar contra `next_statuses`.
- Comentarios y adjuntos pasan a endpoints genéricos (`FlowEvent` /
  `Attachment`) — los componentes de comentarios/evidencias cambian de API.

## Pendientes abiertos (no bloquean)

- Suerte de `discarded` ("No deseo responder" / descarte voluntario del
  paquete): no está en el board. Se decide en la sesión de frontend; si se
  necesita, es agregar un status + transiciones en admin.
- Motor de ejecución (servicios que validan transición, propagación
  `propagates_up`, regla de hijos, `requires_comment`, permisos por
  `role`): sesión posterior a los modelos.
- Colores/iconos definitivos de los status nuevos (heredar de los viejos
  donde aplique; afinar en admin).
