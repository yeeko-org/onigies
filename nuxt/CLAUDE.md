# onigies nuxt

SPA for managing educational institution (IES) data. Two user flows:

- **Dashboard** (`/dashboard/[group]`): admin/staff managing collections and catalogs
- **Respuestas/IES** (`/respuestas/[period]`): institution-facing survey submission

## Commands

```bash
pnpm run dev              # HTTPS dev server on :3018
pnpm run dev:test         # HTTPS test server on :3019 (uses .env.test)
pnpm run test:e2e         # Run Playwright tests (mocked backend)
pnpm run test:e2e:ui      # Interactive UI mode — best for debug
pnpm run test:e2e:debug   # Step-through debug with inspector
pnpm run test:e2e:report  # Open last HTML report
```

Dev server requires `localhost-key.pem` and `localhost.pem` at repo root.

## Environment

```
NUXT_API_URL=https://...     # Django REST API base URL
NUXT_ADMIN_URL=https://...   # Django admin URL (sidebar link)
```

## E2E tests

Playwright on `:3019` with a mocked Django backend — every request to `:8019` is intercepted via `page.route`; unmocked hits return `501`. Tests import `test`/`expect` from `./fixtures`, not `@playwright/test`.

See `.claude/skills/playwright-e2e/SKILL.md` for MCP ↔ test workflow, selector conventions, layout, and coverage.

## Catalog-driven UI

Dashboard is schema-driven by `/catalogs/all/`, loaded via `middleware/dashboard.js` → `fetchCatalogs()`. All state lives in `useMainStore`.

- `composables/cats.js` — enriches each collection with field metadata, filters, sorts, `has.*` and `is_category` flags
- `composables/nodes.js` — builds D3 `stratify()` trees for hierarchical selects; rebuilds on catalog mutation
- List fetching (debounced search, `results`, `loading_fetch`, `final_filters`) lives **locally** in `CollectionDisplay.vue`

### Collection vs category

- Regular (`is_category: false`): API `/{snake_name}/` — actions `saveSimple`, `deleteSimple`.
- Category (`is_category: true`, level starts with `category_`): API `/catalogs/{snake_name}/` — actions `saveCatalog`, `deleteCatalog` also update `cats` in place.

`composables/save_elements.js` routes `saveElement`/`patchElement`/`deleteElement`/`getElement` based on `is_category`.

## Stores (`app/store/`)

- `index.js` (`useMainStore`) — central: `cats`, `schemas`, `all_nodes`, `current_collection_data`, all CRUD actions. **Contract:** every CRUD action returns `{data}` on success or `{errors}` on failure (helpers `ok`/`fail` in `utils/api.js`). Pass an optional `error_msg` as the **last** arg to auto-show the error snackbar; omit it to handle the error inline (e.g. `EditCommon`).
- `auth.js` (`useAuthStore`) — `user_onigies`, `is_logged`, token; role getters `is_staff`, `is_full_editor`, `is_mini_editor`
- `ies.js` (`useIesStore`) — `ies_data`, `surveys`, `current_period`
- `dash.js` — dashboard ephemeral state

## Shared building blocks

- `composables/usePermissions.js` — `USER_PERMISSIONS` / `INVITATION_PERMISSIONS` constants; single source of truth.
- `composables/useApiError.js` — `notifyApiError(err, fallback?)` for DRF error → snackbar (used by `$api`-direct callers like `flow/` and by `fail`).
- `utils/api.js` — `ok`/`fail`, the `{data}|{errors}` contract helpers for store actions.
- `utils/log.js` — `devWarn`/`devLog`: dev-only logging (no-op in prod). Use instead of bare `console.*` for diagnostics.
- `composables/useDates.js` — `formatDate(dateStr)` (dayjs, locale `es`).
- `components/dashboard/common/dialog/DialogDelete.vue` — confirm dialog with `title`/`subtitle`/`loading`/default slot; reusable beyond delete.

## Layouts

| Layout | Routes | Middleware |
|---|---|---|
| `dashboard.vue` | `/dashboard/**` | `dashboard.js` (auth + `fetchCatalogs` + `current_collection`) |
| `ies.vue` | `/respuestas/**` | `dashboard.js` (applied per-page; needs catalogs too) |
| `login.vue` | `/login`, `/register`, `/forgot-password`, `/recover-password` | — |

## Gotchas

- **Icons:** Material Symbols Outlined, NOT MDI. Use strings like `"search"`, `"close"`, `"add"` directly. Icon set `ms` registered in `plugins/vuetify.ts`.
- **Axios `$api`:** injected via `plugins/api.ts`, attaches `Authorization: Token <value>` from the `auth_onigies` cookie.
- **Vuetify theme:** `primary #8a221f` (dark red), `accent #f59322` (orange, for buttons and user actions).
- Main list+filter component: `CollectionDisplay.vue` (owns `final_filters`, `results`, `loading_fetch`; debounces search). Generic CRUD primitives in `common/generic/` and dialogs in `common/dialog/`.