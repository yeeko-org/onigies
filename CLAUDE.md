# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ONIGIES frontend — a Nuxt 4 + Vuetify 3 SPA for managing educational institution (IES) data. It has two distinct user flows:
- **Dashboard** (`/dashboard/[group]`): Admin/staff view for managing collections and catalogs
- **Respuestas/IES** (`/respuestas/[period]`): Institution-facing survey/questionnaire submission flow

## Commands in development

```bash
pnpm dev         # Start dev server (HTTPS, port 3018)
```

No linting or test scripts are configured.

## Environment Variables

Create a `.env` file with:
```
NUXT_API_URL=https://...    # Django REST API base URL
NUXT_ADMIN_URL=https://...  # Django admin URL (linked from dashboard sidebar)
```

The dev server requires `localhost-key.pem` and `localhost.pem` SSL cert files in the repo root.

## Architecture

### Data Flow: Catalog-Driven UI

The entire dashboard UI is **schema-driven** by the `/catalogs/all/` API endpoint. On navigation, `middleware/dashboard.js` calls `fetchCatalogs()` which:
1. Fetches collections metadata, filter group definitions, and all catalog items from `/catalogs/all/`
2. `composables/cats.js` `calculateSchemas()` enriches each collection with field metadata, available filters/sorts, `has.*` flags, and `is_category` flag
3. `composables/nodes.js` `calculateNewCats()` builds D3 stratified trees from catalog hierarchies (used for hierarchical filter selects)

All of this is stored in `useMainStore` (`store/index.js`).

### Collection vs. Category distinction

- Regular collections (`is_category: false`): API at `/{snake_name}/` — full CRUD via store actions `saveSimple`, `deleteSimple`, etc.
- Category collections (`is_category: true`, level starts with `category_`): API at `/catalogs/{snake_name}/` — store actions `saveCatalog`, `deleteCatalog` also update the local `cats` state in-place.

`composables/save_elements.js` exports `saveElement`, `patchElement`, `deleteElement`, `getElement` which automatically route to the correct store action based on `collection_data.is_category`.

### Pinia Stores (`app/store/`)

- **`index.js` (`useMainStore`)**: Central state — `cats` (raw catalog data), `schemas` (computed schemas), `all_nodes` (D3 filter trees), `current_collection_data`, `current_filter_group_data`. All API CRUD actions live here.
- **`auth.js` (`useAuthStore`)**: Auth state — `user_onigies`, `is_logged`, token. Role getters: `is_staff`, `is_full_editor`, `is_mini_editor`.
- **`ies.js` (`useIesStore`)**: IES-specific state — `ies_data`, `surveys`, `packages`, `current_period`.
- **`dash.js`**: Dashboard-specific ephemeral state.

### API Plugin (`app/plugins/api.ts`)

Injects `$api` (axios instance) with `baseURL = NUXT_API_URL` and auto-attaches `Authorization: Token <value>` from the `auth_onigies` cookie via a request interceptor.

### Layouts and Routing

| Layout | Routes | Middleware |
|---|---|---|
| `dashboard.vue` | `/dashboard/**` | `dashboard.js` — checks auth, calls `fetchCatalogs`, sets `current_collection` from `[group]` param |
| `ies.vue` | `/respuestas/**` | `authenticated.js` |
| `login.vue` | `/login`, `/register` | — |

### Key Components

- **`CollectionDisplay.vue`**: The main reusable list+filter component. Manages its own `final_filters`, `results`, `loading_fetch`. Debounces search and re-fetches on filter changes. Used by `pages/dashboard/[group].vue`.
- **`common/main/PanelsResult.vue`**: Renders paginated results from `CollectionDisplay`.
- **`common/generic/`**: Generic CRUD card (`CardGeneric`), edit form (`EditGeneric`), header (`HeaderGeneric`), sheet (`SheetCommon`).
- **`common/dialog/`**: `DialogEdit`, `DialogDelete`, `DialogSearch`.
- **`common/select/FiltersList.vue`**: Renders the active filter widgets for a collection.

### Composables

- `composables/cats.js`: Schema computation from raw API catalog — called once on app init.
- `composables/nodes.js`: D3 `stratify()` tree builder for hierarchical filter groups.
- `composables/save_elements.js`: CRUD helpers routing between catalog/regular endpoints.
- `composables/fetch.js`: Older global reactive state for filters (module-level refs); mostly superseded by `CollectionDisplay`'s local state pattern.
- `composables/filters.js`: `applyFilters()`, status filter definitions.
- `composables/useRules.js`: Vuetify form validation rules.

### Icons

Icons use **Material Symbols Outlined** (not MDI). Use icon name strings like `"search"`, `"close"`, `"add"` directly in Vuetify components. The custom icon set `ms` is registered in `plugins/vuetify.ts`.

### Vuetify Theme Colors

- `primary`: `#8a221f` (dark red)
- `secondary`: purple darken-1
- `accent`: `#f59322` (orange)