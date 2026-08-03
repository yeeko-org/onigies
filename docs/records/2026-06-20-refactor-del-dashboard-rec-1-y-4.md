---
type: record
id: 2026-06-20-refactor-del-dashboard-rec-1-y-4
title: Refactor del dashboard — recomendaciones 1 y 4 aplicadas
date: 2026-06-20
---

# Cambios — refactor del dashboard (Rec 1 y 4)

Complemento de [[2026-06-19-recomendaciones-del-dashboard]]. Documenta los cambios ya
aplicados en ONIGIES y cómo **replicarlos en los otros 2 proyectos** que
comparten el mismo motor schema-driven.

Se implementaron dos recomendaciones:

- **Rec 1** — una sola fuente para la auto-carga por convención de nombre.
- **Rec 4 (híbrido)** — la derivación de metadatos de campo se mueve al
  backend; el front la consume del payload (sin recalcular en JS).

---

## Cambio 1 — Composable `useDynamicComponent`

**Problema:** el bloque `import()` + `.catch()` al genérico estaba copiado en
4 componentes (`PanelList`, `PanelCommon`, `PanelsResult`, `DialogEdit`).

**Solución:** `nuxt/app/composables/useDynamicComponent.js`. Usa
`import.meta.glob` (carga perezosa, un chunk por componente) y un mapa
`sufijo→genérico` interno, así que el genérico de respaldo **no depende del
llamador**: este solo pasa el sufijo.

```js
const dashboardModules = import.meta.glob('../components/dashboard/**/*.vue')
const GENERIC = '../components/dashboard/common/generic'
const FALLBACKS = {
  Header: `${GENERIC}/HeaderGeneric.vue`,
  Sheet: `${GENERIC}/SheetCommon.vue`,
  Edit: `${GENERIC}/EditGeneric.vue`,
  EditSimple: null,   // sin genérico → el panel usa EditCommon
}

export function useDynamicComponent(collectionData, suffix) {
  const comp = shallowRef('')
  const { app_label, snake_name, model_name } = collectionData
  const key = `../components/dashboard/${app_label}/${snake_name}` +
    `/${model_name}${suffix}.vue`
  const fallbackKey = FALLBACKS[suffix]
  const loader = dashboardModules[key] ||
    (fallbackKey ? dashboardModules[fallbackKey] : null)
  if (!dashboardModules[key] && import.meta.dev && fallbackKey)
    console.warn(`[useDynamicComponent] sin ${key}; se usa el genérico`)
  if (loader)
    loader().then(m => { comp.value = m.default })
  return comp
}
```

Detalles que importan al replicar:
- El glob es **relativo** (`../components/...`): `import.meta.glob` **no**
  resuelve el alias `~/`. Si la ruta de `composables/` a `components/` difiere
  en otro proyecto, ajusta el patrón.
- Distingue "el archivo propio no existe" de "error de carga" → avisa en dev
  solo cuando el componente propio falta (bonus: Rec 3).

**En cada llamador**, se borró el `import().then().catch()` y los `computed`
de `route_key`/`snake_name`/`*_name`, reemplazados por una línea por
componente (sin importar genéricos):

```js
import { useDynamicComponent } from '~/composables/useDynamicComponent.js'
const header_component = useDynamicComponent(props.collection_data, 'Header')
const sheet_component  = useDynamicComponent(props.collection_data, 'Sheet')
```

| Archivo | Sufijos |
|---|---|
| `.../common/main/PanelList.vue` | `Header`, `Sheet` |
| `.../common/main/PanelCommon.vue` | `Edit`, `EditSimple` |
| `.../common/main/PanelsResult.vue` | `Edit` |
| `.../common/dialog/DialogEdit.vue` | `Edit`, `Sheet` |
| `.../common/CardComponent.vue` | `Card` |

---

## Cambio 2 — Derivación de metadatos al backend (híbrido)

**Problema:** `composables/cats.js` recalculaba en JS `pk`, `name_field`,
`has.*` y `status_groups` que el backend ya conoce desde `model._meta`.

**Decisión:** una sola fuente de verdad = el backend. **No** se dejó fallback
en JS (reintroduciría la duplicación que la recomendación busca eliminar). En
su lugar, el orden de despliegue garantiza compatibilidad (ver abajo).

### Backend — `api/ps_schema/registry.py`

1. Helper puro `_derive_field_meta(fields)` (junto a `_model_fields`): consume
   la salida ya calculada de `_model_fields` (DRY: no vuelve a recorrer
   `_meta`) y deriva `pk`, `name_field`, `has`, `status_groups`.

```python
def _derive_field_meta(fields: list) -> dict:
    names = {f["name"] for f in fields}
    return {
        "pk": next((f["name"] for f in fields if f["primary_key"]), "id"),
        "name_field": next((n for n in NAME_FIELDS if n in names), None),
        "has": {h: h in names for h in HAS_FIELDS},
        "status_groups": [f["name"] for f in fields
                          if f.get("related_model") == "StatusControl"],
    }
```

2. Mixin `_CollectionDataMixin` que **unifica** los dos `get_collections_data`
   (antes casi idénticos). El único punto que difería —overrides de DB— se
   aísla en el hook `_db_overrides()`:

```python
class _CollectionDataMixin:
    _schemas: dict  # provisto por la subclase

    def _db_overrides(self) -> dict:
        return {}

    def get_collections_data(self) -> list:
        overrides = self._db_overrides()
        result = []
        for _app, data in self.iter_collection_data():
            snake = data['snake_name']
            ov = overrides.get(snake, {})
            merged = {
                **data,
                **{k: v for k, v in ov.items() if v is not None},
                'fields': _model_fields(self._schemas[snake].model),
            }
            merged.update(_derive_field_meta(merged['fields']))
            result.append(merged)
        return result
```

- `CatalogRegistry(_CollectionDataMixin)` usa el `_db_overrides` por defecto
  (catálogos sin overrides en DB).
- `CollectionRegistry(_CollectionDataMixin)` solo define `_db_overrides()` con
  la lectura de la tabla `Collection`.
- Ventaja extra del mixin: **garantiza** que ambos registries deriven igual
  (imposible añadirlo a uno y olvidar el otro).

Sin migración: todo se calcula en vivo y viaja en `/catalogs/all/`.

### Frontend — `nuxt/app/composables/cats.js`

Se eliminaron las derivaciones locales; el front **consume el payload**:

```js
// pk, name_field, has y status_groups vienen del payload (ps_schema).
const other_fields = Object.keys(coll.has).concat([coll.pk, coll.name_field])
...
coll.status_groups.forEach(sg => { ... })
```

Se mantiene en el front lo puramente de UI: `child_relation_fields`,
`other_fields`, `collection_filters`, `available_sorts`. Se quitaron además
unos `console.log` de depuración (Rec 6).

---

## Cambio 3 — Borrar el fetch muerto (Rec 5)

**Problema:** `composables/fetch.js` exportaba estado a nivel de módulo
(`results`, `final_filters`, `applyFilters`, `temp_reset`…). Eran singletons
compartidos entre instancias (peligrosos con `CollectionDisplay` anidados) y
**nadie los importaba**: el camino vivo son los refs **locales** de
`CollectionDisplay.vue`.

**Solución:** eliminar `composables/fetch.js`. Sin reemplazo: `CollectionDisplay`
ya es el único dueño del fetch de listas.

---

## Cambio 4 — Logging de diagnóstico solo en dev (Rec 6)

**Problema:** `console.log`/`warn`/`error` de diagnóstico sembrados en código de
runtime (composables, stores y componentes), visibles en producción.

**Solución:** un helper auto-importado `utils/log.js`:

```js
export const devWarn = (...args) => { if (import.meta.dev) console.warn(...args) }
export const devLog  = (...args) => { if (import.meta.dev) console.log(...args) }
```

`import.meta.dev` es constante en build → las llamadas se eliminan por
tree-shaking en producción. Se reemplazan los `console.*` de diagnóstico por
`devWarn`/`devLog` (uso de una línea, sin envolver en `if` cada vez).

Detalles al replicar:
- Auto-importado en `.vue`; en stores/composables `.js` que importan sus
  dependencias explícitamente, importar `devWarn` también explícitamente.
- **Conservar** los canarios de plantilla intencionales (p. ej. `{{full_main}}`
  en `EditGeneric`, `EDICIÓN 1 (REPORTAR…)` en `EditCommon`, `Sheet genérico 3`
  en `PanelCommon`): son fallback visible a propósito, no ruido.

---

## Cambio 5 — Contrato uniforme `{data}|{errors}` en las acciones del store (Rec 8)

**Problema:** las acciones CRUD del store devolvían formas inconsistentes (unas
`{errors}`, otras `response.data` crudo, otras `undefined` al tragar el error),
y el manejo de errores estaba disperso (cada caller decidía, algunos en
silencio).

**Solución:** un contrato único más dos helpers compartidos en `utils/api.js`:

```js
import { useApiError } from "~/composables/useApiError.js"
import { devWarn } from "~/utils/log.js"

export const ok = (response) => ({ data: response.data })
export const fail = (error, error_msg = null) => {
  devWarn(error)
  if (error_msg)
    useApiError().notifyApiError(error, error_msg)
  return { errors: error.response?.data ?? null }
}
```

Reglas:
- **Toda** acción CRUD del store devuelve `{ data }` (éxito) o `{ errors }`
  (fallo). `delete*` devuelve `{ data: true }`.
- Cada acción acepta un `error_msg = null` como **último** parámetro y lo
  reenvía a `fail`. Si llega un mensaje, `fail` muestra el snackbar (con el
  detalle del servidor si existe, o `error_msg` de respaldo, vía el
  `notifyApiError` ya existente). Si no, el caller decide la presentación
  (p. ej. errores **inline** en `EditCommon`).
- Los wrappers de `composables/save_elements.js`
  (`saveElement`/`patchElement`/`deleteElement`/`getElement`) solo **reenvían**
  `error_msg` a la acción correspondiente.
- Los callers leen `res.data` (éxito) o `res.errors` (control de flujo). Para
  mostrar el toast, pasan el mensaje a la acción en vez de notificar a mano.

**Eventos (parte de Rec 8):** fijar **kebab-case** en los listeners de plantilla
(`@item-saved`, `@item-deleted`, …). Es solo consistencia: Vue 3 compila
`@itemSaved` y `@item-saved` al mismo handler, así que el comportamiento no
cambia.

> `composables/useApiError.js` **no** cambia: `notifyApiError(err, fallback)`
> sigue siendo la ruta para callers que usan `$api` directo (p. ej. `flow/`) y
> ahora también lo usa `fail`.

---

## Réplica en los otros 2 proyectos

**Orden de despliegue (importante):** primero backend, luego frontend. El
cambio de backend es **aditivo y sin migración** (solo agrega claves al
payload), así que no rompe al front viejo. Si se invierte el orden, el front
nuevo se quedaría sin `coll.has`/`coll.pk` y fallaría.

1. **Backend** (`ps_schema/registry.py` de ese proyecto):
   - Copiar `NAME_FIELDS`, `HAS_FIELDS`, `_derive_field_meta`.
   - Copiar `_CollectionDataMixin`; hacer que ambos registries hereden de él y
     borrar sus `get_collections_data`; mover la lectura de `Collection` al
     hook `_db_overrides()` del registry de colecciones.
   - Verificar (abajo) que el payload trae las claves nuevas.
2. **Frontend** (`composables/cats.js`):
   - Quitar el cálculo de `pk`/`name_field`/`has`/`status_groups`; usar
     `coll.*` del payload (`other_fields` con `Object.keys(coll.has)`).
3. **Frontend** (Rec 1, independiente del backend, puede ir antes o después):
   - Crear `useDynamicComponent.js` y reemplazar los 4 bloques de auto-carga.
4. **Frontend** (Rec 5/6/8, solo frontend, sin migración):
   - **Rec 5:** comprobar que nada importa `composables/fetch.js` y borrarlo.
   - **Rec 6:** crear `utils/log.js` (`devWarn`/`devLog`) y sustituir los
     `console.*` de diagnóstico de runtime; conservar los canarios de plantilla.
   - **Rec 8:** crear `utils/api.js` (`ok`/`fail` con `error_msg`); aplicar el
     contrato `{data}|{errors}` a todas las acciones CRUD del store, reenviar
     `error_msg` desde los wrappers de `save_elements.js`, y migrar los callers
     a `res.data`/`res.errors`; pasar kebab-case en los listeners de plantilla.

> Si en algún proyecto los modelos/`_meta` difieren (p. ej. otro nombre de
> modelo de status en vez de `StatusControl`), ajusta solo `_derive_field_meta`
> y los `NAME_FIELDS`/`HAS_FIELDS`.

> **Cuidado con Rec 8 en cada proyecto:** antes de cambiar la forma de retorno,
> localiza en *ese* proyecto todos los consumidores de las acciones CRUD (los
> que leen `res` crudo, `res.id`, `res.success`, etc.) y migrálos a `res.data`/
> `res.errors`. Es la parte de mayor superficie; revisar carpeta por carpeta de
> cada app específica (la lógica genérica vive en `common/`, `store/` y
> `composables/`; cada app tendrá además sus propios callers).

---

## Verificación

**Backend** (sin migración):
```python
from ps_schema.registry import collection_registry
print(collection_registry.get_collections_data()[0].keys())
# debe incluir: pk, name_field, has, status_groups
```
O `GET /catalogs/all/` y confirmar esas claves en cada colección.

**Frontend** (`pnpm run dev`):
- Abrir una colección con componentes propios (`good_practice`) y otra que caiga
  a genéricos: filas, chips de status, filtros y panel de detalle igual que
  antes.
- En dev, el `console.warn` de `useDynamicComponent` aparece **solo** para
  componentes propios genuinamente inexistentes.
- Crear/editar/borrar un registro y un catálogo (`is_category`) para confirmar
  que `pk`/`name_field`/`has` siguen alimentando `EditCommonFields`.
- **Rec 8:** provocar un error de guardado/borrado y confirmar que el snackbar
  aparece (cuando se pasa `error_msg`) o el error inline en `EditCommon` (cuando
  no se pasa); confirmar que el éxito sigue poblando la lista/detalle con
  `res.data`.
- **Rec 6:** en consola no deben aparecer logs de diagnóstico en build de
  producción; en dev, los `devWarn` sí.
- Regresión: `pnpm run test:e2e`.