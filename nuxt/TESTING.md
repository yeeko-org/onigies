# Testing — nuxt

## Niveles montados

Solo end-to-end con Playwright, contra el backend **mockeado** (`page.route`): la app corre de verdad, la API no. Ver el skill `playwright-e2e` para el flujo de trabajo MCP ↔ tests.

**No hay Vitest.** La lógica pura (`app/utils/sections.js` y compañía) hoy queda cubierta solo de refilón por los e2e; montarlo está pendiente como task.

## Comandos

```bash
pnpm run test:e2e            # suite completa
pnpm run test:e2e:ui         # modo interactivo
pnpm run test:e2e:debug      # paso a paso
pnpm run test:e2e:report     # abre el último reporte HTML
npx playwright test e2e/login.test.ts   # un solo spec
```

Playwright levanta el servidor solo (`pnpm run dev:test`, puerto 3019 sobre HTTPS con certificado local) y reutiliza el que ya esté corriendo.

## Flujos cubiertos

| Spec | Flujo |
|---|---|
| `login.test.ts` | login de staff a `/dashboard` y de IES a `/respuestas`, cookie de sesión, credenciales inválidas, validación de formato |
| `logout.test.ts` | el botón de salir limpia la cookie y redirige a `/login` |
| `protected-routes.test.ts` | `/dashboard` y `/respuestas` redirigen a `/login` sin sesión y se sostienen con ella |
| `register.test.ts` | alta con invitación válida, invitación ya usada, invitación inexistente, validación de contraseña |
| `forgot-password.test.ts` | solicitud de recuperación y error de servidor |
| `recover-password.test.ts` | token válido e inválido, contraseñas que no coinciden, reset exitoso con auto-login, token que expira entre validar y confirmar |
| `respuestas-tabs.test.ts` | chips del card ligados a su `?tab=`, navegación al tab correcto y deep-link que sobrevive a la recarga |

## Fixtures y credenciales

No hay credenciales reales: todo es mock. Los datos viven en `e2e/mocks/auth.ts` y los interceptores en `e2e/mocks/handlers.ts`; `e2e/fixtures.ts` instala el catch-all en cada test y `e2e/helpers.ts` setea la cookie `auth_onigies` para arrancar ya autenticado.

Dos usuarios de referencia: `mockStaffUser` (sin institución, va a `/dashboard`) y `mockIesRespuestasUser` (institución `UP` con una encuesta 2025 completa). Ese último lleva `is_test: true` a propósito, porque los tests de `/respuestas` recorren las tres secciones y una IES real solo vería las publicadas (`app/utils/sections.js`).
