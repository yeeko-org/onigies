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
pnpm dev    # Servidor de desarrollo (HTTPS, puerto 3018)
```

## Implementación en producción:
```bash
pnpm build
```

