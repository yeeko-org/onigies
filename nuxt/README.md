# onigies_nuxt

Frontend de la plataforma ONIGIES (Observatorio Nacional de Igualdad de
Género de las IES).

Stack: **Nuxt 4** + **Vuetify 3** + **Pinia** · Puerto: **3018** (HTTPS)

## Requisitos previos

- Node.js 20+
- pnpm 9+
- Certificados SSL locales (`localhost-key.pem` y `localhost.pem`) en `nuxt/`

Para generar los certificados (sólo en local):

```bash
mkcert localhost
```

Requiere tener [mkcert](https://github.com/FiloSottile/mkcert) instalado.

## Configuración

Crea `nuxt/.env` basándote en `nuxt/.env.template`:

```bash
cp .env.template .env
```

| Variable | Descripción |
|---|---|
| `NUXT_API_URL` | URL base del API (ej. `http://localhost:8018/api`) |
| `NUXT_ADMIN_URL` | URL del admin Django (ej. `http://localhost:8018/admin`) |

## Instalación

```bash
pnpm install
```

## Comandos

```bash
pnpm run dev    # Servidor de desarrollo (HTTPS, puerto 3018)
```

## Tests E2E (Playwright)

Pruebas end-to-end con backend mockeado (Django no corre durante los
tests). Cubren login, register con invitación, recuperación de
contraseña, logout y rutas protegidas.

```bash
pnpm run test:e2e         # headless, todas las pruebas
pnpm run test:e2e:ui      # modo UI interactivo (recomendado para debug)
pnpm run test:e2e:debug   # paso a paso con inspector
pnpm run test:e2e:report  # abre el reporte HTML de la última corrida
```

Primera corrida: Playwright levanta automáticamente un servidor Nuxt
de pruebas en `https://localhost:3019` (puerto dedicado, no afecta tu
`pnpm run dev`). Si ya tienes el servidor encendido, lo reusa.

Los tests viven en `e2e/`. Para detalles arquitectónicos (mocks,
convenciones de selectores, flujo de trabajo con Playwright MCP) ver
[`CLAUDE.md`](CLAUDE.md) y el skill
[`.claude/skills/playwright-e2e/`](../.claude/skills/playwright-e2e/SKILL.md).

## Implementación en producción:
```bash
pnpm run build
```

