---
type: record
id: 2026-09-04-prototipo-edicion-cuestionario-deploy-e-incidente-netlify
date: 2026-09-04
---

# Prototipo de edición del cuestionario desde el dashboard, deploy y el incidente del build de Netlify

Sesión del 4 de septiembre de 2026, en modo duo, arrancada quince minutos antes de una reunión presencial con Rubén. La reunión tiene audio y se documentará en una sesión propia; este record cubre solo lo que la sesión produjo en código, en producción y en el skill de deploy. En paralelo se armó el documento de correcciones de redacción del instrumento para [[task-116]] (ver esa task).

## El prototipo: [[task-42]] de golpe

Un ejecutor Opus construyó en una sola pasada, front y back, la edición de los textos del cuestionario desde el dashboard. Lo que quedó:

- **Backend, sin migraciones.** `Observable` gana un serializer completo que anida sus cinco familias de preguntas (A, transversalización, alcance, planes, especial), y cada familia entra como catálogo propio filtrado por observable. Solo el texto es escribible; número, orden, componente, las seis ponderaciones y las banderas de comportamiento viajan de solo lectura. Ni alta ni baja en observables ni preguntas (`NoDeleteMixin` + `hide_create`), porque el seed los gobierna y las respuestas capturadas cuelgan de ellos.
- **Permisos:** el default del registry, escribir exige `is_reviewer`. Verificado con peticiones reales: revisora 200, IES 403, anónimo 401, DELETE 405. La lectura anónima de catálogos es comportamiento preexistente de todos los catálogos; ahora cubre también los textos del instrumento.
- **Frontend:** `ObservableHeader` y `ObservableEditSimple` (seis textos del observable), un editor compartido para las cinco familias y diez envoltorios finos que existen solo porque la convención de nombre del dashboard resuelve `{Model}{Suffix}.vue`. La entrada del menú «Ejes y Componentes» pasó a «Cuestionario: ejes, observables y preguntas».
- **Verificado en navegador** en local: edición guardada con snackbar, valor confirmado en base y restaurado.

Tres llamadas quedaron abiertas para Ricardo y viven en la task: el `order` de solo lectura por ser clave natural del seed, la duplicidad entre `BQuestion.text` y `Observable.reach_instances_question`, y un test de regresión propuesto. Ejes y componentes siguen con alta y baja, asimetría por alcance.

## El deploy

Ricardo pidió subirlo a producción de inmediato. Se siguió el runbook de `deploy-api` y el fast-forward de [[adr-0001]]: `main` y `production` al mismo ref.

- `bad2f71` — el prototipo. Pytest 94 ✓. Sin cambios en `models.py` ni en migraciones en el rango.
- Servidor: árbol limpio (solo los untracked de siempre), pull, `migrate` sin nada que aplicar, `makemigrations --check` «No changes detected», recarga con SIGHUP.
- Smoke: `/api/catalogs/all/`, `/api/`, `/api/catalogs/observable/1/` y `/api/catalogs/a_question/?observable=1` en 200; el observable 1.1 devuelve 7 opciones A y 1 pregunta B anidadas. Producción ya tenía los 41 observables sembrados. Log de errores sin trazas nuevas.

## El incidente: Netlify no publicó

El API salió; el frontend no. Doce minutos después del push, el manifiesto de build de Nuxt (`/_nuxt/builds/latest.json`) seguía con el id del 20 de agosto, tanto en `onigies.netlify.app` como a través del proxy de la UNAM. Ricardo trajo el log del panel: el build murió instalando dependencias.

```
npm error Cannot read properties of null (reading 'edgesOut')
```

Falló con la caché del 20 de agosto y también con «Clear cache and retry deploy». El commit no tocaba `package.json`; el lockfile de npm no existía. Causa: el repo no versionaba ningún lockfile —el `.gitignore` raíz ignora `*-lock.yaml`—, así que Netlify resolvía el árbol de cero con npm 10.9.8 en cada build, y una versión transitiva publicada entre deploys detonó un bug del arborist de npm al resolver los peers bajo `nuxt`. Reproducido en local desde un `package.json` pelón: mismo error. La instalación en frío con `pnpm install --frozen-lockfile` sobre el `pnpm-lock.yaml` local pasó.

Resolución, `e01c3e6`: se versiona `nuxt/pnpm-lock.yaml` con una excepción `!nuxt/pnpm-lock.yaml` en el `.gitignore` raíz. Netlify detecta el lockfile y pasa de npm a pnpm con las versiones exactas que corren en local. Antes del push se emuló el build de Netlify (`NODE_ENV=production NITRO_PRESET=netlify pnpm run build`): pasó y produjo `dist/` con la etiqueta nueva del menú. Netlify publicó a los 20 segundos de vigilancia; el chunk con la etiqueta se confirmó siguiendo los imports del entry, porque los chunks de layout son lazy y no aparecen en el HTML.

Hallazgo lateral: `pnpm run generate` falla en local al prerenderizar `/` (`vue/index.mjs does not provide an export named 'default'`). No afecta el deploy porque Netlify corre `nuxt build`, pero obliga a que el comando de build siga siendo ese hasta que se arregle.

## Documentación

Todo el aprendizaje quedó en el skill `deploy-api`, sección nueva «Frontend build on Netlify» (lockfile, emulación local, verificación por build id, qué hacer cuando falla), enlazada desde el paso 4 del checklist previo, y un puntero en el skill `deployment`. La descripción del skill perdió el prefijo `[api]` porque ahora cubre el monorepo; Ricardo lo revisa.
