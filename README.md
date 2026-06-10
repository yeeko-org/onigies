# onigies

Monorepo de la plataforma web de ONIGIES — Observatorio Nacional de
Igualdad de Género de las Instituciones de Educación Superior.

## Subproyectos

| Directorio | Stack | Puerto |
|------------|-------|--------|
| [`api/`](api/README.md) | Django REST Framework | 8018 |
| [`nuxt/`](nuxt/README.md) | Nuxt 4 + Vuetify 3 | 3018 |

Cada subproyecto tiene su propio README con instrucciones de instalación
y configuración.

## Inicio rápido

```bash
# Terminal 1 — backend
cd api
python manage.py runserver

# Terminal 2 — frontend
cd nuxt
pnpm run dev
```

## Tests

```bash
cd api  && pytest             # Tests unitarios/integración Django
cd nuxt && pnpm run test:e2e  # Tests E2E Playwright (backend mockeado)
```

Ver [`nuxt/README.md`](nuxt/README.md#tests-e2e-playwright) para
detalles de E2E.