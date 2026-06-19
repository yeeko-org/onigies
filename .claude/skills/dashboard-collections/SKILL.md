---
name: dashboard-collections
description: >
  [nuxt] How the schema-driven dashboard renders any collection: the
  convention-based dynamic-import of {Model}Header/Sheet/Edit/EditSimple
  components, the catalog payload contract, the automatic filter bar, and the
  related-objects (child collection) lists. Use whenever adding or editing a
  dashboard view for a model, wiring a new collection's detail/edit/header
  component, debugging why a generic fallback renders, touching filters at the
  top of a list, or working in components/dashboard/** or CollectionDisplay.
---

# dashboard-collections (frontend)

The dashboard is **100% schema-driven**. One backend payload (`/catalogs/all/`)
describes every collection; the frontend renders lists, filters, detail panels
and edit forms generically. To customize a model you do **not** register
anything — you just drop a `.vue` file with the right name in the right folder
and it is auto-imported by convention. This skill is the frontend consumer of
the backend `manage-collections` skill (read that one for how the payload is
produced).

## 1. Data flow (where everything starts)

```
middleware/dashboard.js → store.fetchCatalogs()
  GET /catalogs/all/  → data
    ├─ calculateSchemas(data)   composables/cats.js   → store.schemas
    ├─ calculateNewCats(...)    composables/nodes.js  → store.all_nodes (D3 trees)
    └─ calculate_status(...)    composables/filters.js→ store.status
  store.current_collection_data = schemas.collections_dict[current_collection]
```

- `store.schemas.collections_dict[snake_name]` is the **`collection_data`**
  object passed down through almost every component. Memorize its shape — it
  drives all rendering.
- Pages are thin: `pages/dashboard/[group].vue` just renders
  `<CollectionDisplay v-if="cats_ready" />`. The `[group]` route param sets
  `current_collection` via the layout middleware.

### `collection_data` shape (built in `composables/cats.js`)

Backend-provided (`ps_schema/registry.py::_base_collection_dict` + fields):
`app_label`, `snake_name`, `model_name` (PascalCase), `name`, `plural_name`,
`level`, `pk`, `fields[]`, `available_actions[]`, `xls_export`, `cat_params`
(spread to top level — e.g. `init_display`, `hide_create`).

Each `fields[]` entry carries `name`, `relation_type`
(`simple|one_to_many|many_to_many|one_to_one|relation`), `related_snake_name`,
`related_model`, `field_type`, `default`, `null`. Computed front-side by
`calculateSchemas`:

| Property | Meaning |
|---|---|
| `pk` | primary-key field name (fallback `'id'`) |
| `name_field` | first of `name`/`title` present — used as the row title |
| `has.{comments,description,help_text,order,color,icon}` | booleans: does the model have that field |
| `other_fields` | simple fields not already handled generically |
| `is_category` | `level.startsWith('category_')` → routes to `/catalogs/` API |
| `child_relation_fields` | fields with `one_to_many`/`many_to_many` → child lists |
| `status_groups` | field names whose `related_model === 'StatusControl'` |
| `collection_filters` | the assembled, ordered filter list (see §4) |
| `available_sorts` | the “Ordenar por” select options |

## 2. The auto-load convention (the core)

Given `collection_data`, four optional per-model components are resolved by
**dynamic import of a path built from the name**. No registry. The path is:

```
~/components/dashboard/{app_label}/{snake_name}/{model_name}{Suffix}.vue
```

e.g. `example` / `good_practice` / `GoodPractice` →
`~/components/dashboard/example/good_practice/GoodPracticeHeader.vue`.

If the file does not exist, the `.catch()` of the dynamic `import()` loads a
generic fallback instead (except `EditSimple`, which silently renders nothing
and makes the panel fall back to `EditCommon`).

| Suffix | Resolved in | Fallback | Role |
|---|---|---|---|
| `Header` | `PanelList.vue` | `HeaderGeneric.vue` | collapsed row: icon, title, status chips, comment icon, `#details` slot |
| `Sheet` | `PanelList.vue`, `DialogEdit.vue` | `SheetCommon.vue` | expanded read-only detail + **child collections** (§5) |
| `Edit` | `PanelCommon.vue`, `PanelsResult.vue`, `DialogEdit.vue` | `EditGeneric.vue` | form fields, mounted inside `EditCommon`'s `#edit` slot |
| `EditSimple` | `PanelCommon.vue` | *(none)* | full inline editor that **replaces** `EditCommon` entirely |

The resolution code is identical everywhere — this exact block:

```js
const route_key  = computed(() => props.collection_data.app_label)
const snake_name = computed(() => props.collection_data.snake_name)
const edit_name  = computed(() => `${props.collection_data.model_name}Edit`)

import(`~/components/dashboard/${route_key.value}/${snake_name.value}/${edit_name.value}.vue`)
  .then(m => { edit_component.value = m.default })
  .catch(() => import('~/.../EditGeneric.vue').then(m => { edit_component.value = m.default }))
```

### Edit vs EditSimple (the decision that bit you on `flow`)

In `PanelCommon.vue`:

- **`{Model}EditSimple` exists** → rendered inline with **only** `v-model="full_main"`.
  It owns the whole detail/edit UI: no generic header fields, no save/delete from
  `EditCommon`. **It is the reviewer's detail view in the dashboard.** Do not put
  IES-survey content here (that lives in `/respuestas`).
- **No `EditSimple`** → `EditCommon` renders generic fields (`EditCommonFields.vue`:
  name, order, status, comments, icon/color, description, help_text) + your
  `{Model}Edit` inside the `#edit` slot, with the Guardar/Eliminar buttons.

> Gotcha: `EditSimple` receives **only** `v-model`. It does **not** get `isStaff`
> or other props — if the component declares such a prop with a default, that
> default wins in the dashboard.

### Props each component receives

| Component | Props in |
|---|---|
| `Header` | `main` (the row object), `collection_data`, `show_details`, `parent`, `is_simple`; emits `open-panel` |
| `Sheet` | `full_main` (fetched detail), `show_details`, `collection_data` |
| `Edit` | `v-model` (= `full_main`/`element_to_edit`), `is_edit`, `is_massive_edit`; emits `itemSaved` |
| `EditSimple` | `v-model` only |

Real example — `GoodPracticeHeader.vue` wraps `HeaderCommon` and fills the
`#details` slot with a `DisplayGroup` (axes); see
`components/dashboard/example/good_practice/`.

## 3. Component tree of a list view

```
CollectionDisplay.vue          owns filters, search (debounce 800ms), sort, paging, fetch
  ├─ filter chips + FiltersList.vue          (§4)
  └─ PanelsResult.vue          actions bar (create/reorder/massive), add+edit dialog, pagination
       └─ PanelList.vue        resolves {Model}Header + {Model}Sheet; v-for rows
            └─ PanelCommon.vue  one expansion panel; on open fetches full detail;
                                resolves {Model}Edit + {Model}EditSimple
```

- **`CollectionDisplay.vue`** is the entry point and the place that calls
  `fetchElements`. It has **local** `results`/`final_filters`/`loading_fetch`
  refs (note: the same-named module-level refs in `composables/fetch.js` are a
  parallel older path — CollectionDisplay does not use them; see §6).
- `PanelCommon.openMain()` lazily fetches the full object via
  `getElement(collection_data, id)` only when the row is expanded — the list
  endpoint returns light rows, the detail endpoint returns the full object.

## 4. Automatic filter bar

The filters shown at the top of every list are assembled in `cats.js` into
`collection_data.collection_filters` (sorted by `order`) and rendered by
`FiltersList.vue`. Sources, in order of assembly:

1. **`all_filters`** declared on the backend `CollectionSchema`
   (`FilterRef("institutions")`, `ComponentFilter(...)`). A `FilterRef` resolves
   against `filters_dict` (the registered `FilterGroupSchema`s); a custom
   `ComponentFilter` (no `filter_name`) keeps `is_custom: true`.
2. **Category filter group** — if `is_category`, the matching `FilterGroupSchema`
   is pushed (multi-level group/type/subtype select).
3. **Status groups** — for each `StatusControl` field, the matching entry from
   `status_filters` (`composables/filters.js`) is pushed.

`FiltersList.vue` dispatches each filter to a widget by shape:

| Filter shape | Widget |
|---|---|
| has `collection` | `StatusDetail` (status select) |
| has `key_name` | `SelectGroup` (hierarchical D3-tree select from `all_nodes`) |
| has `component` | custom: `TripleBooleanFilter`, `RangeDates`, `UserSelect`, `OnlyByFilter` |

Chips above the bar toggle which filters are visible; `simplified_filters`
(≤3 filters) collapses the chip row and inlines the widgets next to the search
box. All widgets write into the single `final_filters` ref, whose deep-watch
triggers the (debounced) refetch.

## 5. Related-objects (child collection) lists

`SheetCommon.vue` is the generic expanded detail. It iterates
`collection_data.child_relation_fields` (the `one_to_many` / `many_to_many`
fields) and, for each related collection found in `schemas.collections_dict`,
renders one of two ways:

- **Inherited data present** (`full_main['{snake}s']` array exists) → renders
  `PanelsResult` inline with `in_sheet` (no extra fetch; data came nested in the
  detail payload).
- **Only a count** (`full_main['{snake}s_count']`) → renders a nested
  `CollectionDisplay` with `direct_sheet` and
  `init_filters={ [parent_snake]: parent_id }` — a fully filtered sub-list that
  fetches on demand.

This is how a parent's detail panel shows its children with working filters and
pagination, with zero per-model code. To customize, write a `{Model}Sheet.vue`
that does something other than the default child-iteration.

## 6. CRUD routing: collection vs category

`composables/save_elements.js` routes every write by `is_category`:

| | Regular (`is_category:false`) | Category (`is_category:true`) |
|---|---|---|
| API base | `/{snake_name}/` | `/catalogs/{snake_name}/` |
| save/patch/delete | `saveSimple`/`patchSimple`/`deleteSimple` | `saveCatalog`/`patchCatalog`/`deleteCatalog` |
| side effect | none (server is source of truth) | also mutates `store.cats` in place + rebuilds `all_nodes` |

`getLastId()` (store) decides POST vs PUT from the pk and `is_new`. `EditCommon`
calls `saveElement`/`deleteElement`; it never talks to the API directly.

## 7. Adding a custom view — checklist

1. Confirm the collection exists in the backend registry (`manage-collections`).
2. Decide the level of customization:
   - **Just a richer row** → add `{Model}Header.vue`.
   - **Custom read-only detail / children layout** → add `{Model}Sheet.vue`.
   - **Custom form fields inside the generic frame** → add `{Model}Edit.vue`.
   - **Fully bespoke inline detail+edit** → add `{Model}EditSimple.vue` (replaces
     the generic frame; remember it only gets `v-model`).
3. Put it under `components/dashboard/{app_label}/{snake_name}/` with the exact
   `{model_name}{Suffix}.vue` name (PascalCase model, snake folder).
4. No import, no registration — the dynamic import finds it.

## Key files

| Concern | File |
|---|---|
| Payload → schema enrichment | `composables/cats.js` |
| D3 filter trees | `composables/nodes.js` |
| CRUD routing | `composables/save_elements.js` |
| Store + actions | `app/store/index.js` |
| List entry / filters | `components/dashboard/CollectionDisplay.vue` |
| Actions bar + edit dialog | `.../common/main/PanelsResult.vue` |
| Row resolver (Header/Sheet) | `.../common/main/PanelList.vue` |
| Panel + Edit/EditSimple resolver | `.../common/main/PanelCommon.vue` |
| Generic fallbacks | `.../common/generic/{HeaderGeneric,SheetCommon,EditGeneric,EditCommon,EditCommonFields}.vue` |
| Filter widgets | `.../common/select/FiltersList.vue` |
| Backend contract | skill `manage-collections`, `api/ps_schema/registry.py` |