---
name: playwright-e2e
description: "[nuxt] Playwright end-to-end tests with mocked backend for
  the Nuxt app. Use whenever the user wants to navigate the app with the
  Playwright MCP, add or modify E2E tests, mock auth endpoints, or debug
  a flow in the browser. Covers the 3-phase workflow MCP ↔ tests: review
  existing coverage before opening the browser, take notes during
  exploration, and propose new tests after. Also trigger when the user
  mentions `playwright`, `e2e`, `test:e2e`, `page.route`, or asks to
  verify a user flow interactively."
---

# playwright-e2e

End-to-end testing for the Nuxt SPA. Tests run against a **mocked backend** — Django does NOT run. Playwright intercepts every request to `http://localhost:8019/*` via `page.route`.

## Stack snapshot

| | Dev | Test |
|---|---|---|
| Nuxt | `https://localhost:3018` | `https://localhost:3019` |
| Env file | `.env` | `.env.test` |
| Backend URL (mocked) | `http://localhost:8018/api` | `http://localhost:8019/api` |

Running tests: `pnpm test:e2e` (headless), `pnpm test:e2e:ui` (interactive debug).

## Project layout

```
nuxt/
├── playwright.config.ts       # baseURL, webServer :3019, ignoreHTTPSErrors
├── e2e/
│   ├── fixtures.ts            # custom `test` with auto-installed catchAll
│   ├── helpers.ts             # fillLoginForm, setAuthCookie, ...
│   ├── mocks/
│   │   ├── auth.ts            # JSON fixtures (users, tokens)
│   │   └── handlers.ts        # mockLoginSuccess, mockInvitationValid, ...
│   └── *.test.ts              # one file per flow
```

Import pattern in tests:

```ts
import { test, expect } from './fixtures'  // NOT from '@playwright/test'
```

The custom `test` installs a **catchAll**: any request to the fake backend without an explicit mock returns `501 {"detail": "No mock for <METHOD> <URL>"}`. If a test fails with that message, the fix is to add a mock, not to tweak assertions.

## Workflow: MCP ↔ e2e tests

Follow these 3 phases each time Playwright MCP is used to test a flow.

### Phase 1 — Pre-MCP: review existing coverage

Before opening the browser:

1. Read `e2e/*.test.ts` and check whether the flow already has coverage.
2. If a test covers the scenario, **run it** (`pnpm test:e2e e2e/<file>.test.ts`) instead of firing up MCP.
3. If the test exists but is incomplete or broken, note the gap and use MCP only on the uncovered part.
4. If there is no coverage, proceed to Phase 2.

### Phase 2 — During MCP: record interactions

While navigating with the `mcp__plugin_playwright_playwright__*` tools, keep running notes of:

- URLs visited and in what order (include the `?token=...` query if any)
- Fields filled and with what values
- What was verified visually (text, element, redirect, cookie)
- Workarounds needed (Vuetify input quirks, async `onMounted` races)
- Bugs or unexpected behavior found

### Phase 3 — Post-MCP: evaluate and generate tests

After finishing MCP exploration, evaluate:

- **New flow with no test?** → Propose generating one.
- **Bug found?** → Propose a regression test that reproduces it.
- **Existing test incomplete?** → Propose an update.
- **One-off exploration?** → Report findings; do not generate a test.

Ask the user before generating or modifying tests. The user reviews each diff in PyCharm.

## Selector conventions

- **Prefer `getByLabel` / `getByRole` / `getByText`** — resilient to layout changes.
- **Vuetify `v-text-field`** exposes its label to `getByLabel`. Use `{ exact: true }` when multiple labels overlap (e.g. "Contraseña" vs "Confirmar contraseña" vs "Nueva contraseña").
- **Icon buttons** (tooltip-only) do NOT get an accessible name from Vuetify's `v-tooltip`. Add `data-testid="<purpose>-button"` to the source component and use `getByTestId`.
- **Alerts** — `.v-alert` is the root class. `page.locator('.v-alert')` works for any variant.

## Mocking patterns

Atomic helpers live in `mocks/handlers.ts`. Compose them per scenario.

```ts
import { test, expect } from './fixtures'
import { mockLoginSuccess, mockCurrentUser } from './mocks/handlers'
import { mockStaffUser } from './mocks/auth'

test('staff login', async ({ page }) => {
  await mockLoginSuccess(page, mockStaffUser)
  await mockCurrentUser(page, mockStaffUser)  // for post-redirect checkAuthSimple
  await page.goto('/login')
  // ...
})
```

Add new helpers to `handlers.ts` when an endpoint appears in more than one test. Keep JSON shapes in `auth.ts`.

**Post-login noise:** after a successful login the middleware `dashboard.js` calls `fetchCatalogs()` (GET `/catalogs/all/`). Mock it with `{}` to avoid the catchAll 501 cluttering logs.

## Auth cookie

- Name: `auth_onigies`
- Set via UI login OR directly with `setAuthCookie(context, token)` from `helpers.ts`.
- Cleared by the store action `logout()`; tests verify with `getAuthCookieValue`.

## Current coverage (2026-04)

| Flow | File | Notes |
|---|---|---|
| Login (staff, ies, invalid, validation) | `login.test.ts` | |
| Register via invitation | `register.test.ts` | |
| Forgot password | `forgot-password.test.ts` | |
| Recover password (incl. token race) | `recover-password.test.ts` | |
| Logout | `logout.test.ts` | Uses `data-testid="logout-button"` |
| Protected routes | `protected-routes.test.ts` | Both `/dashboard` and `/respuestas` use middleware `dashboard` |

## Next level: E2E against real backend

Current setup mocks the backend. If/when integration-level E2E is needed:

1. Add `pytest-django`, `pytest-playwright`, `LiveServerTestCase`.
2. Spin Django on `:8019` with SQLite-in-memory and fixtures.
3. Remove the catchAll (or narrow it) for those tests.
4. Use a separate Playwright `project` so the two suites coexist.

Do NOT implement until the user requests it — the unit/pytest layer of `api/` already covers most integration concerns.