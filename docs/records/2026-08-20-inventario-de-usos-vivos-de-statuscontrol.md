---
type: record
id: 2026-08-20-inventario-de-usos-vivos-de-statuscontrol
date: 2026-08-20
parent: "[[task-7]]"
---

# Inventario de usos vivos de `ies.StatusControl` antes del borrado

Informe de investigación de solo lectura levantado el 2026-08-20 para responder una pregunta concreta de Ricardo: si el motor `flow` está en producción desde el 2026-06-26 y la compuerta de verificación de datos se cerró el 2026-08-12, ¿por qué `ies.StatusControl` sigue en pie — algo lo usa de verdad? El inventario existe para que la sesión que ejecute [[task-7]] no vuelva a derivarlo: ahí están los paths con líneas, la clasificación de cada uso y el orden en que hay que desmontarlo.

Advertencia de método: se leyó el árbol de trabajo, no el HEAD. Al momento del barrido había cambios sin commitear en `api/ies/models.py`, `nuxt/app/composables/cats.js`, `nuxt/app/store/index.js`, `StatusDetail.vue`, `PanelsResult.vue` y `EditCommon.vue`. Salvo un cambio de dato (`STATUS_GROUP_PARAMS["register"]["order"]` de `4` a `3`, en `api/ies/models.py:325`), el diff era cosmético: quitaba comentarios explicativos añadidos el día anterior.

## La etiqueta que hacía falta: «UI viva sin efecto»

Las tres categorías obvias —andamiaje de coexistencia, código muerto, código que sostiene una función viva— no alcanzaban para clasificar lo que más confunde en este caso. Hizo falta una cuarta, que se acuña aquí y se usa en todo el inventario:

> **UI viva sin efecto**: código que sí se ejecuta y sí se pinta en pantalla hoy, pero cuyo resultado no cambia nada en el sistema. El filtro se manda y el backend lo descarta; la opción de orden se ofrece y el validador de ordenamiento la rechaza; el campo se escribe por PATCH y esa columna ya no gobierna ningún flujo.

No es código muerto —se ejecuta, se ve, se puede clicar— ni es load-bearing —borrarlo no rompe ninguna función real—. Es exactamente la categoría que explica por qué `StatusControl` *parecía* usado: la superficie visible sobrevivió al motor que la sostenía.

Las otras tres etiquetas se usan con el sentido habitual: **andamiaje de coexistencia** es lo que solo existe para sostener los datos legacy hasta el borrado; **muerto** es lo inalcanzable o no referenciado; **load-bearing** es aquello cuya remoción rompe una función viva hoy.

## Backend

### Definiciones de campo que sostienen datos en la base (andamiaje de coexistencia)

Seis FK a `StatusControl` en modelos concretos, más una en un abstracto:

| path:línea | campo | modelo |
|---|---|---|
| `api/answer/models.py:23-24` | `status_register` | `ObservableResponse` |
| `api/answer/models.py:62-63` | `status_register` | `GroupResponse` |
| `api/survey/models.py:78-79` | `status_register` | `AxisValue` |
| `api/survey/models.py:244-245` | `status_register` | `GeneralGroupResponse` |
| `api/example/models.py:53-54` | `status_sending` | `GoodPracticePackage` |
| `api/example/models.py:114-116` | `status_sending` (`default='draft'`) | `GoodPractice` |
| `api/survey/models.py:11-13` | `status_register` | `Comment` (abstracto: lo heredan `ObservableComment`, `GroupComment`, `GeneralGroupComment`) |

Cada uno de los seis convive con su `status = FK('flow.Status')` hermano y lleva el comentario de coexistencia citando el §5 del diseño del motor (por ejemplo `api/survey/models.py:80-81`). El modelo mismo está en `api/ies/models.py:344-379`: PK de texto, `group` con `GROUP_CHOICES`, `role` con `ROLE_CHOICES`, `can_send`, `is_final`, `priority`, `order`, `color`, `icon`.

Tres de esas columnas son `NOT NULL` —`ObservableResponse.status_register`, `GroupResponse.status_register` y `GeneralGroupResponse.status_register`—, dato que manda en el orden de los pasos del borrado.

### Caminos de código que sí se ejecutan hoy

- **`Institution.save()`** — `api/ies/models.py:56-57` (`av.status_register_id = 'pre_start'`), `:71` (`package.status_sending_id = 'draft'`) y `:86` (`'status_register_id': 'pre_start'` en el `defaults` de `general_group_responses`). Escribe las columnas legacy en cada creación de survey, axis_value y paquete. Es **la única vía de escritura viva** que queda hacia `StatusControl` en todo el sistema.
- **`InitStatus`** — `api/ies/initial_data.py:4-86`, disparado desde `api/ies/apps.py:13-19` solo cuando `'migrate_initial_data' in sys.argv`. Siembra quince status (`draft`, `pre_start`, `approved`…). Es andamiaje: sin él, los defaults de `Institution.save()` reventarían por FK inexistente. Lo llaman también los tests, en `api/survey/tests.py:12,31`.
- **`status_groups_data()`** — `api/ies/models.py:330-341`, consumido en `api/api/views/catalogs/all.py:20`. Ver la sección propia más abajo.
- **`StatusControlSerializer` y el volcado completo del catálogo** — `api/api/views/catalogs/serializers.py:5-8` y `api/api/views/catalogs/all.py:18-19`: `/catalogs/all/` entrega la tabla `status_control` entera, y lo hace sin autenticación (`permission_classes = (AllowAny,)`). Es lo que alimenta el `status` del store del frontend y, por ahí, los `StatusDetail` del dashboard.
- **`_derive_field_meta`** — `api/ps_schema/registry.py:143-153`, con la línea `"status_groups": [f["name"] for f in fields if f.get("related_model") == "StatusControl"]`. Corre en cada `get_collections_data()` (`api/ps_schema/registry.py:244-257`). Es el punto exacto donde el mundo viejo se cuela al contrato del dashboard nuevo.
- **Serializers de `example`** — `api/api/views/example/serializers.py` usa `fields = '__all__'` en sus siete clases (líneas 32, 38, 51, 64, 84, 97 y 108), de modo que `status_sending` viaja en el payload de `good_practice` y `good_practice_package` y además es escribible por PATCH.
- **Admin** — `api/ies/admin.py:57-63`, `@admin.register(StatusControl)`. El §7 del diseño del motor lo declara conservado hasta la fase de borrado.

### Ninguna colección lo declara: se deriva sola

`grep -rn status api/*/catalog_schema.py` no devuelve nada. Ningún `CatalogSchema` ni `CollectionSchema` menciona status: los `status_groups` se derivan automáticamente del `_meta` del modelo en `_derive_field_meta`. Consecuencia práctica: al borrar el modelo, la lista queda vacía en toda colección sin que haya que tocar ninguna declaración de esquema.

## El dato duro: solo dos colecciones exponen `status_groups`

De todas las colecciones registradas —`api/example/catalog_schema.py:46,58,70`; `api/survey/catalog_schema.py:16,28`; más las de `ies/`, `indicator/` y `question/`—, **solo dos tienen FK a `StatusControl`** y por tanto reciben `status_groups: ["status_sending"]`:

- `good_practice_package` (`GoodPracticePackage`)
- `good_practice` (`GoodPractice`)

Ninguna otra. `Survey`, `GeneralPackage`, `Institution`, `Period` y todos los catálogos salen con `status_groups: []`. Y los cuatro modelos que llevan `status_register` —`ObservableResponse`, `GroupResponse`, `AxisValue`, `GeneralGroupResponse`— **no están registrados como colecciones**, así que su columna legacy no llega al dashboard por ninguna vía. Toda la superficie visible de `StatusControl` en el dashboard vivía, entonces, en dos colecciones de buenas prácticas.

## Frontend: la cadena completa

El recorrido del dato, de la respuesta HTTP al componente:

1. `nuxt/app/store/index.js:70` — `this.status = calculate_status(data.status_control)` agrupa el catálogo crudo por `group` (`nuxt/app/composables/filters.js:14-24`).
2. `nuxt/app/store/index.js:278-288` — el getter `status_dict` arma `{grupo: {nombre: status}}`, con guarda `if (!state.cats?.status_control) return {}`.
3. `nuxt/app/composables/cats.js:13-16` — indexa `data.status_groups` por `sg.collection`, que es el nombre del campo (`status_sending`), y produce `status_filters`.
4. `nuxt/app/composables/cats.js:87-95` — por cada entrada de `coll.status_groups` empuja un filtro a `collection_filters` y una opción de orden `${status.collection}__order`.
5. `nuxt/app/store/index.js:290-292` — el getter `status_filters` expone lo anterior al resto de los componentes.

Los consumidores, con su clasificación:

| path:línea | qué hace | clasificación |
|---|---|---|
| `nuxt/app/components/dashboard/common/generic/EditCommonFields.vue:76-86` | Renderiza un `StatusDetail` por cada `status_group` de la colección; `@change-status` llama a `saveStatus` (`:29-47`), que hace PATCH real del campo `status_sending` | Escribe en la base de verdad, pero lo que escribe ya no gobierna el flujo: **UI viva sin efecto** |
| `nuxt/app/components/dashboard/status/StatusDetail.vue` (completo) | `v-select` de status por grupo; lee `mainStore.status` y `statusGroupLabel` | UI viva sin efecto |
| `nuxt/app/components/dashboard/common/select/FiltersList.vue:37-46` | Pinta el `StatusDetail` de la barra de filtros cuando `filter_box.collection` | UI viva sin efecto: `BaseGenericViewSet.filterset_fields = []` (`api/api/views/common_views.py:95`) y `PackageFilter.fields = {}` (`api/api/views/example/__init__.py:62`) hacen que el parámetro `status_sending` se descarte en el backend |
| `nuxt/app/components/dashboard/common/main/PanelsResult.vue:103-107` | En `addItem()` precarga el default del campo desde `status_filters[field.name].default_value` | Andamiaje de coexistencia; además `good_practice*` tiene `hide_create: True` (`api/example/catalog_schema.py:53,66`) y `PanelsResult.vue:202` oculta el botón, así que en la práctica casi nunca corre |
| `nuxt/app/components/dashboard/common/generic/EditCommon.vue:14,15,84-90` | `updateStatus()` arma el snackbar «Status de Envío actualizado a "X"» leyendo `status_dict` | UI viva sin efecto |
| `nuxt/app/composables/cats.js:89-95` | Ofrece ordenar la lista por `status_sending__order` | Muerto en efecto: `OrderingAutoFilter` (`api/api/views/common_views.py:67-89`) solo valida `{campo}__order` cuando `issubclass(field.related_model, Status)`, y `StatusControl` no lo es, así que el orden se ignora |
| `nuxt/app/components/dashboard/common/MassiveEdit.vue:117-127` | `StatusDetail` en edición masiva | Mismo estatus que `FiltersList` |
| `nuxt/app/components/dashboard/status/StatusChip.vue:36,52,68` | Chip armado desde `status_dict` y `status_filters` | Solo se invoca desde `GenericSelect.vue:235,276`, cuya condición nunca se cumple |
| `nuxt/app/components/dashboard/common/select/GenericSelect.vue:221,231,277` | Deshabilita y decora según `item.raw.status_validation` | **Muerto**: ningún payload lleva `status_validation`, porque no existe en ningún modelo concreto |
| `nuxt/app/components/dashboard/status/StatusToggle.vue:34-37` | Lee `status_dict` | **Muerto**: el componente no se importa en ningún lado |
| `nuxt/app/components/dashboard/status/StatusDetail.vue:52,73` | Controla `readonly` con `status_selected.open_editor` | Roto por diseño: `open_editor` no existe en `StatusControl` (`api/ies/models.py:367` lo tiene comentado), siempre es `undefined`, y el select queda readonly para todo no-staff |

Todo lo demás del dashboard ya corre sobre `flow`: `FlowStatusChip` y `FlowStatusActions` en `HeaderCommon.vue:149`, `GoodPracticeList.vue:330`, `GoodPracticeCard.vue:112`, `SurveyHeader.vue:48`, `GeneralGroupList.vue:209`, `GeneralGroupPanel.vue:181` y `pages/respuestas/index.vue:97,131,161`.

No queda ningún id de status viejo hardcodeado en `nuxt/app/`: el grep de `ready_to_send`, `pre_start`, `need_changes` y `'draft'` no devuelve nada fuera de `status_control` mismo. Eso lo cerró [[task-9]]. La única prueba unitaria del frontend (`nuxt/tests/unit/sections.test.js`) no toca status.

## El `status_groups` del 2026-08-19 es mundo `StatusControl`

El commit `673dd34` del 2026-08-19 («Tasks 9, 22, 23 y 119: status_groups desde el backend…») es el único que introduce `status_groups_data` y `status_filters`. Como el payload es reciente y el modelo es viejo, valía la pena preguntarse si esa capa era independiente del catálogo legacy. No lo es, por tres eslabones:

1. Se construye iterando `GROUP_CHOICES` (`api/ies/models.py:330-341`), que es literalmente el `choices` del campo `StatusControl.group` (`api/ies/models.py:347`).
2. Su clave `collection` es `f"status_{key}"`, es decir, el nombre de la columna legacy (`status_sending`, `status_register`).
3. El frontend lo casa contra `coll.status_groups`, que `_derive_field_meta` calcula filtrando por `related_model == "StatusControl"` (`api/ps_schema/registry.py:151-152`).

Lo que hizo [[task-9]] no fue crear una capa nueva sino **mudar al backend un mapa que estaba duplicado y hardcodeado** en `nuxt/app/composables/filters.js`. Lo decía el propio comentario que ese commit dejó en `api/ies/models.py`. Conclusión operativa: `status_groups_data`, `STATUS_GROUP_PARAMS` y `status_filters` mueren con el modelo, no lo sobreviven.

## Restos ya podridos: borrables hoy, sin migraciones

Estos usos no son coexistencia sino residuo. Ninguno toca la base, así que se pueden retirar en cualquier momento y por separado del §8:

- `api/utils/mix_models.py` completo — `CatalogType.status_validation` (`:29-30`) y `CatalogGroup`. Ningún modelo hereda de esas abstractas: el grep sobre todo `api/` solo devuelve las definiciones.
- `api/api/permissions.py:84-95`, `IsEditorOrCreateOrRead`. Muerto por partida doble: la clase no está referenciada en ningún viewset ni en `settings.PS_SCHEMA`, y usa `obj.status_validation.open_editor`, atributo que **no existe** en `StatusControl`. Si alguien la enchufara, reventaría con `AttributeError`.
- `api/api/views/common_views.py:16-21`, `AdvancedConditionalFieldsViewMixin.field_permissions`, que lista `status_register`, `status_sending` y `status_validation` como excluidos para anónimos. El mixin no lo hereda nadie.
- `api/example/models.py:156-157`, el `status_validation` comentado de `FeatureGoodPractice`.
- `api/ies/models.py:326`, la clave `"validation"` de `STATUS_GROUP_PARAMS`, con `default_value: "proposed"` — un nombre de status que `InitStatus` **no siembra** (las filas del grupo `validation` están comentadas en `api/ies/initial_data.py:44-48`). Emite una entrada de payload `status_validation` que ningún modelo concreto tiene.
- En el frontend: `nuxt/app/components/dashboard/status/StatusToggle.vue` entero y la rama `status_validation` de `GenericSelect.vue`.

## El §8.5 del diseño del motor es letra muerta

El §8 del diseño (`docs/records/2026-06-05-diseno-del-motor-de-flujo.md:410-424`) manda en su punto 5: «Actualizar `api/api/views/example/__init__.py` — el filtro `status_sending__is_final=False` pasa a `status__role__isnull=False`».

**Ese filtro ya no existe.** `grep -rn is_final api/`, excluyendo migraciones, devuelve exactamente tres coincidencias: `api/ies/initial_data.py:7` (un comentario), `api/ies/initial_data.py:61,75` (la asignación del seed) y `api/ies/models.py:368` (la definición del campo). En `api/api/views/example/__init__.py` no hay rastro: desapareció en algún refactor previo sin que nadie lo anotara. El punto 5 del §8 —y el criterio de aceptación de [[task-7]] que lo repite— quedaron sin objeto.

## Qué depende hoy, de verdad, de `StatusControl`

Cero funcionalidad de flujo. El motor `flow` gobierna `bp`, `cp` y `gen` enteros; `StatusControl` no participa en ninguna transición, permiso, propagación ni notificación. Lo que sostiene es solo esto:

1. **Integridad referencial**: seis columnas apuntando a la tabla. Cuatro de ellas —los `status_register` de `ObservableResponse`, `GroupResponse`, `AxisValue` y `GeneralGroupResponse`— son datos en reposo puros: ninguna se lee en ningún camino de código.
2. **Los defaults de creación de `Institution.save()`**, que existen solo para no violar el `NOT NULL` de las columnas que el §8 borra.
3. **Una superficie de UI en dos colecciones del dashboard**, la que se retiró el mismo 2026-08-20 (ver más abajo).

La lectura del inventario es que no es que algo lo necesite: es que **nadie ejecutó el §8**. La compuerta que lo bloqueaba —verificación de datos migrados— se cerró el 2026-08-12 con `verify_flow_data` en 661 = 661, y la única precondición que quedaba viva («re-correr `migrate_flow_data` justo antes») se eliminó ese mismo día al retirarse el comando del repo tras el incidente. El borrado está desbloqueado desde entonces.

## Camino mínimo al borrado, en cinco pasos

Son pasos, no estimaciones. El orden importa por dos razones: las columnas `NOT NULL` obligan a que cortar la escritura y borrar las columnas viajen juntas, y el cambio de forma del payload obliga a que backend y frontend salgan en el mismo deploy.

**Paso 0 — Contar las `Evidence` huérfanas.** Es la única precondición viva que dejó [[task-7]] y no depende de `StatusControl`. Si se va a hacer una sola tanda de migraciones, conviene resolverla antes de tocar nada.

**Paso 1 — Barrer lo muerto, sin migraciones.** Todo lo listado en «Restos ya podridos». Es reversible, no toca la base y deja el §8 con contorno nítido.

**Paso 2 — Cortar la escritura.** Quitar de `Institution.save()` las tres asignaciones legacy (`api/ies/models.py:56-57,71,86`). A partir de ahí ninguna fila nueva toca `StatusControl`.

**Paso 3 — Migraciones de borrado de columnas**, una por app (`answer`, `survey`, `example`): los seis `status_register`/`status_sending`, más los modelos de comentarios viejos, más `Evidence`, más el `comments` TextField de los tres modelos de `example`. **Los pasos 2 y 3 viajan en el mismo deploy**, porque tres de las columnas son `NOT NULL` y dejar de escribirlas sin borrarlas rompería la creación de instituciones.

**Paso 4 — Borrar el modelo, el admin y el seed.** `StatusControl`, `StatusControlAdmin`, `InitStatus` (y su llamada en `api/ies/apps.py`, y el `InitStatus()` de `api/survey/tests.py:31`), `GROUP_CHOICES` y `ROLE_CHOICES` de `ies`, `status_groups_data()` y `STATUS_GROUP_PARAMS` completos, `StatusControlSerializer` y las dos claves de `/catalogs/all/` (`status_control` y `status_groups`).

**Paso 5 — Frontend, en el mismo deploy que el paso 4**, porque el payload cambia de forma. Cae la rama `status_groups` de `_derive_field_meta` y, con ella, `status_filters`, `status_dict`, `calculate_status`, `statusGroupLabel`, `StatusDetail.vue`, `StatusChip.vue`, el bloque `status_groups` de `EditCommonFields`, `updateStatus` de `EditCommon`, la rama `related_model === 'StatusControl'` de `PanelsResult.addItem`, la rama `filter_box.collection` de `FiltersList` y de `MassiveEdit`, y los typedefs `StatusGroup`, `status_groups` y `status_filters` de `nuxt/app/types/collection.js`.

**Al cerrar, actualizar la documentación** que todavía dice «no lo borres todavía»: `.claude/skills/flow/SKILL.md:314-317`, `api/CLAUDE.md:37` y `.claude/skills/dashboard-collections/SKILL.md:59,180`, donde `status_groups` está documentado como «campos cuyo `related_model === 'StatusControl'`».

## Decisión que tomó Ricardo con este inventario

El 2026-08-20, leído lo anterior, Ricardo separó las dos mitades: [[task-7]] se ejecuta completa en una sesión aparte, y en esta sesión se retira por adelantado **solo la superficie visible** de «Status de Envío» en el dashboard —la que el inventario clasificó como UI viva sin efecto—. El razonamiento que lo justificó: ese `v-select` escribe una columna que ya no gobierna nada, pero es visible para la revisora, que puede estar operándolo creyendo que dictamina algo, mientras el flujo real se maneja con `FlowStatusActions` en el mismo header. Adelantar ese retiro quita una superficie engañosa sin depender de ninguna migración.
