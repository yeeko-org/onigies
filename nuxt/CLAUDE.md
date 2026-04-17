# onigies nuxt

SPA for managing educational institution (IES) data. Two user flows:

- **Dashboard** (`/dashboard/[group]`): admin/staff managing collections and catalogs
- **Respuestas/IES** (`/respuestas/[period]`): institution-facing survey submission

## Commands

```bash
pnpm dev         # HTTPS dev server on :3018
```

No linting or test scripts configured. Dev server requires `localhost-key.pem` and `localhost.pem` at repo root.

## Environment

```
NUXT_API_URL=https://...     # Django REST API base URL
NUXT_ADMIN_URL=https://...   # Django admin URL (sidebar link)
```

## Catalog-driven UI

The dashboard is **schema-driven by `/catalogs/all/`**. `middleware/dashboard.js` calls `fetchCatalogs()`, which loads collections metadata, filter groups, and catalog items. Then:

1. `composables/cats.js` `calculateSchemas()` enriches each collection with field metadata, filters, sorts, `has.*` flags, and `is_category` flag.
2. `composables/nodes.js` `calculateNewCats()` builds D3 `stratify()` trees for hierarchical filter selects. Rebuilds after any catalog mutation.
3. `composables/fetch.js` manages debounced (600 ms) list fetching with global `results`, `loading_fetch`, `final_filters` refs.

All stored in `useMainStore` (`store/index.js`).

### Collection vs category

- Regular collections (`is_category: false`): API `/{snake_name}/` — store actions `saveSimple`, `deleteSimple`, etc.
- Category collections (`is_category: true`, level starts with `category_`): API `/catalogs/{snake_name}/` — actions `saveCatalog`, `deleteCatalog` also update `cats` in place.

`composables/save_elements.js` exports `saveElement`, `patchElement`, `deleteElement`, `getElement` — route automatically based on `collection_data.is_category`.

## Stores (`app/store/`)

- `index.js` (`useMainStore`) — central: `cats`, `schemas`, `all_nodes`, `current_collection_data`, all CRUD actions
- `auth.js` (`useAuthStore`) — `user_onigies`, `is_logged`, token; role getters `is_staff`, `is_full_editor`, `is_mini_editor`
- `ies.js` (`useIesStore`) — `ies_data`, `surveys`, `current_period`
- `dash.js` — dashboard ephemeral state

## Layouts

| Layout | Routes | Middleware |
|---|---|---|
| `dashboard.vue` | `/dashboard/**` | `dashboard.js` (auth + `fetchCatalogs` + `current_collection`) |
| `ies.vue` | `/respuestas/**` | `authenticated.js` |
| `login.vue` | `/login`, `/register` | — |

## Gotchas

- **Icons:** Material Symbols Outlined, NOT MDI. Use strings like `"search"`, `"close"`, `"add"` directly. Icon set `ms` registered in `plugins/vuetify.ts`.
- **Axios `$api`:** injected via `plugins/api.ts`, attaches `Authorization: Token <value>` from the `auth_onigies` cookie.
- **Vuetify theme:** `primary #8a221f` (dark red), `accent #f59322` (orange, for buttons and user actions).
- Main list+filter component: `CollectionDisplay.vue` (owns `final_filters`, `results`, `loading_fetch`; debounces search). Generic CRUD primitives in `common/generic/` and dialogs in `common/dialog/`.