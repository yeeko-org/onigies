# Mejoras al dashboard a partir del design system ONIGIES

Documento de propuestas para implementar — en sesiones futuras — el
design system de `docs/onigies-design-system/` sobre el dashboard
actual (`nuxt/app`, rutas `/dashboard` y `/respuestas`).

**Alcance.** Este documento se concentra en el dashboard administrativo
(admin app). El sitio público vive en el repo legacy y se reescribirá
después.

**Estado al cierre de esta sesión.**

- `nuxt/app/plugins/vuetify.ts` ya quedó alineado con la paleta del
  design system: `primary` = índigo `#2C2F6E`, `accent` = turquesa
  `#14A8A0`, y sobrescritura de los 4 ejes (`purple`, `blue`, `amber`,
  `pink`) con los hex del design system. Los `VBtn` ahora usan `accent`
  por default.
- El resto de cambios se documenta aquí, agrupado en fases.

---

## Fase 0 · Limpieza inmediata

Detalles que descubrimos al tocar `vuetify.ts` y que conviene resolver
antes de tareas mayores.

1. **Diagnóstico de TypeScript en `materialSymbols` icon set.**
   `vuetify.ts:16-19` declara `component: (props: {tag, icon}) => ...`,
   pero el tipo `IconSet` de Vuetify espera
   `IconComponent = FunctionalComponent<IconProps>`. La firma no encaja
   y el LSP marca `TS2322`. Es prexistente — solo se hizo visible al
   editar el archivo. Fix sugerido: importar `IconProps` desde
   `vuetify` y tipar `props` como `IconProps` (o `as IconSet` si se
   acepta un cast).
2. **Decidir el destino de los 82 usos actuales de `color="primary"`.**
   Con `primary` cambiando de vinotinto (`#8a221f`) a índigo
   (`#2C2F6E`), 38 archivos repintan su color principal. Hay que pasar
   visualmente por cada sección y decidir caso por caso:
   - Si era un botón de acción → migrar a `color="accent"` (turquesa).
   - Si era chrome institucional (app-bar, encabezados, badges
     estructurales) → dejarlo en `primary` (índigo).
   - Si era un acento decorativo → considerar uno de los 4 ejes.
3. **Confirmar comportamiento del default global de `VBtn`.** Acabamos
   de agregar `defaults.VBtn.color = 'accent'`. Los botones sin
   atributo `color` ahora son turquesa; los que ya tienen `color="..."`
   explícito no cambian. Vale la pena un barrido visual para detectar
   botones que se ponen turquesa cuando deberían quedarse neutros (por
   ejemplo, botones de cancelar, botones en headers).
4. **`secondary` quedó como `colors.purple.darken1` de Material.** El
   design system no define un "secondary" formal — está sin uso
   explícito en el dashboard. Opciones: borrarlo, mapearlo al índigo
   `#1A1C46` (`--indigo-900`), o reusar uno de los ejes según
   convención. Decisión pendiente.

---

## Fase 1 · Tokens y tipografía global

El design system está pensado como **tokens CSS variables** + **tipo
escala Material**. Hoy el dashboard usa Roboto y la escala default de
Vuetify.

1. **Importar `colors_and_type.css` como hoja global.**
   En `nuxt.config.ts`, agregar el CSS del design system. Esto da
   acceso a todas las variables (`--rosa-500`, `--neu-raised`,
   `--radius-md`, etc.) en todos los componentes — sin reescribir cada
   propiedad.

   ```ts
   // nuxt/nuxt.config.ts
   css: [
     '~/assets/styles/onigies-design-system.css', // copia local
     // o referencia directa: '../docs/onigies-design-system/project/colors_and_type.css'
   ]
   ```

   Recomendación: **copiar** el CSS al directorio `nuxt/app/assets/` y
   dejar `docs/` como referencia inmutable. Si el design system cambia,
   se re-sincroniza manualmente — evita acoplar el build al directorio
   `docs/`.

2. **Tipografías.** Reemplazar `@fontsource/roboto` por **Plus Jakarta
   Sans** (display) + **Manrope** (body) + **JetBrains Mono**
   (tabular). El design system las consume vía Google Fonts.
   - Decisión pendiente: ¿bundle local (`@fontsource/...`) o Google
     Fonts CDN? Local es más rápido en producción pero suma peso al
     build. Google Fonts añade un round-trip pero con cache global.
   - Bandera del design system: las fuentes son sustituciones; el
     equipo de comunicación de ONIGIES tendría que confirmar antes de
     un lanzamiento público.

3. **Iconografía.** Migrar de Material Icons (set actual) a **Material
   Symbols Rounded**. El plugin ya tiene un wrapper `materialSymbols`
   en `vuetify.ts:16-19` que renderiza `<span class=
   "material-symbols-outlined">` — habría que:
   - Cambiar `material-symbols-outlined` → `material-symbols-rounded`.
   - Asegurar que la fuente del CDN se cargue (en `nuxt.config.ts` o
     en un layout root).
   - Verificar cobertura de glifos para iconos usados hoy
     (`baby_changing_station`, `self_improvement`, etc., están en
     Symbols Rounded por defecto).

---

## Fase 2 · Layout del dashboard (chrome)

El `dashboard.vue` actual usa un `v-app-bar` horizontal + un
`v-navigation-drawer` temporal (overlay). El design system propone un
**sidebar fijo de 248px en índigo profundo + topbar translúcido
flotante**. Esto cambia bastante la sensación.

1. **Sidebar fijo (248px) en índigo `--indigo-700`.**
   Layout actual: `v-navigation-drawer` se abre y se cierra. Propuesto:
   `permanent` con ancho fijo de 248px, color `--indigo-700`, items en
   blanco con opacidad por estado (activo/hover).
   - Implica ajustar todos los `v-main` y `v-container` para asumir el
     gutter izquierdo.
   - El sidebar conserva el patrón "secciones agrupadas" del design
     system: `Trabajo`, `Datos`, `Publicación` (ver
     `docs/onigies-design-system/project/ui_kits/admin_dashboard/Sidebar.jsx`).
   - Pie del sidebar: bloque "Ciclo activo · 2026" + botón de ajustes.

2. **Topbar translúcido con backdrop-blur.**
   `rgba(246,244,249,0.78)` + `backdrop-filter: blur(16px)`. Contiene
   breadcrumb a la izquierda, search pill al centro (con neumorfismo
   `inset`), iconos de acción y user-pill a la derecha.
   - Reemplaza el `v-app-bar` actual con `color="primary"`. Implica
     mover el logout y el toggle a la nueva estructura.

3. **Canvas neumórfico.**
   Cambiar el fondo de la app de blanco a `--bg-page` (`#F6F4F9`).
   Vuetify por default usa `#FFFFFF`. Esto se hace en `vuetify.ts` o
   con CSS global sobre `<v-app>`. Es el cambio que **habilita** la
   estética neumórfica: las cartas con `--neu-raised` solo se ven bien
   sobre este fondo.

---

## Fase 3 · Patrones de componente

Una vez que el chrome está listo, hay 5 patrones recurrentes para
adoptar:

### 3.1 KPI cards (encabezado de cada vista)

Los `index.html` del admin abren con una fila de 4 KPIs neumórficos.
Cada uno: icono circular pressed, número grande tabular, label, delta
chip con tinte de éxito/peligro. Útil para `/respuestas` (avance por
estado, totales) y para una futura página `/dashboard` de resumen.

Ver `KpiRow.jsx` y CSS `.adm-kpi*` en `admin.css`.

### 3.2 Tabla de evidencias (densa, con chip de eje)

El design system propone tablas con:
- Cabecera ALL-CAPS, tracking `0.12em`, color `--fg-3`.
- Filas con padding `12px 10px`, hover `--neutral-100`, selected
  `--violeta-50`.
- Primera columna: ID mono.
- Chip de eje como segunda columna (con `--rosa-50`/`--violeta-50`/etc
  como fondo + dot del color brand).
- Status pill al final (`adm-status--ok|review|warn|rej`).

Aplica a `CollectionDisplay.vue` y a las listas de buenas prácticas
(`GoodPracticeList.vue`).

### 3.3 Botones (jerarquía clara)

Tres variantes documentadas:
- `adm-btn--primary` → fondo turquesa, sombra material `--elev-2`,
  hover sube a `--elev-3`. Para acciones de mayor peso.
- `adm-btn--ghost` → fondo `--bg-page`, sombra neumórfica
  `--neu-raised-sm`. Para acciones secundarias.
- `adm-btn--text` (a derivar) → solo color, sin fondo. Para enlaces
  internos tipo "Ver todo".

Hoy se usa `v-btn` con variantes Vuetify (`flat`, `outlined`, `text`).
Mapeo recomendado:

| Variante Vuetify | Mapeo design system |
|---|---|
| `v-btn` sin variant | `adm-btn--primary` (accent fill) |
| `v-btn variant="tonal"` | `adm-btn--ghost` |
| `v-btn variant="text"` | text-only, color turquesa |

### 3.4 Form inputs neumórficos

Inputs con `--neu-inset-sm` (sombras hacia adentro) en lugar del border
clásico de Vuetify. Foco con `--glow-primary` (4px de halo turquesa).
- `v-text-field`, `v-select`, `v-textarea`, `v-date-input` necesitan
  CSS override.
- Es un cambio bastante visible — vale la pena maquetar primero un
  ejemplo y validar antes de migrar todo.

### 3.5 Confirm dialogs / modales

El design system usa Material para floating UI:
- Modal con `--elev-5`, `--radius-lg`, scrim `rgba(20,19,27,0.45)` con
  `backdrop-filter: blur(6px)`.
- Spring open con `--ease-spring` 320ms.

Aplicable a `ConfirmActionDialog.vue`, `NotReadyDialog.vue`,
`DialogDelete.vue`.

---

## Fase 4 · Detalle visual

Refinamientos que no son estructurales pero suben mucho la sensación
de calidad. Mejor hacerlos al final.

1. **Tabular numerals en columnas de datos.**
   `font-variant-numeric: tabular-nums` en todo `<td>` que contenga
   números (KPIs, scores, IDs, fechas). Es un one-liner por componente
   y vale mucho visualmente.

2. **Hover/press states en cards clickeables.**
   `.adm-card` con cursor pointer: hover sube de `--neu-raised` a
   `--neu-raised-lg` + `translateY(-1px)`. Press inset.

3. **Sentence case en todos los labels.**
   El design system es estricto: "Descarga de resultados", **no** "DESCARGA
   DE RESULTADOS" ni "Descarga De Resultados". ALL-CAPS solo para
   overlines de sección (con `letter-spacing: 0.12em`) y para acrónimos
   institucionales (BUAP, CIAD).

4. **Espaciado en 4px grid.**
   Pasar de `mt-2`, `ma-3` de Vuetify a tokens `--sp-1`...`--sp-11`. Es
   doloroso a corto plazo pero da consistencia y permite cambios
   globales (escalado para tablet/mobile) desde un solo lugar.

5. **Idioma de UI strings.**
   Hay textos en inglés residual (botón `Close` en el snackbar de
   `dashboard.vue:316`). Revisar todos los componentes y traducir.

---

## Fase 5 · Sitio público (fuera de alcance inmediato)

El design system documenta también el observatorio público
(`ui_kits/public_site/`). Cuando se aborde la migración del sitio
público al monorepo, los patrones que aplican son:

- Hero con **gradient wash pastel** (oklch blend, blur, gain bajo).
- Tarjetas de ejes (`EjesGrid.jsx`) con icono Material Symbols + chip
  del color brand.
- `IndiceGauge.jsx` — gauge animado para el índice global.
- `IesTable.jsx` — tabla densa con ordenamiento y filtros.
- `HistoricalDots.jsx` — visualización compacta de evolución
  histórica.

Estos viven hoy en el repo legacy en Python 2 + Vue 2 y no se tocan
aquí; quedan como referencia para cuando se programe esa migración.

---

## Convenciones que NO cambiamos

Para evitar drift, vale la pena fijar lo siguiente como contrato del
proyecto:

- **Los 4 ejes mantienen los hex del design system.** Cualquier cambio
  de paleta requiere actualizar `vuetify.ts` y el CSS del design
  system simultáneamente.
- **Turquesa nunca se usa como chip de eje.** Es el color de acción
  global y debe leerse sin ambigüedad. Si necesitas un 5º color para
  datos, usa una de las shades neutras o ámbar `--ambar-200`.
- **No emoji en UI del producto.** El logo y la paleta ya cargan la
  calidez; los emoji rompen el registro institucional.
- **Spanish (México) como idioma canónico.** Casing tipo sentencia, no
  Title Case ni ALL-CAPS arbitrario.

---

## Notas para una sesión futura sobre el Admin de Django

Aunque este documento se centra en el dashboard Nuxt, varios principios
aplican al Admin de Django (templates de `email_send/`, formularios
del propio admin):

- Inputs neumórficos no escalan al admin de Django (mucho CSS por
  reescribir), pero **sí** vale la pena adoptar la paleta y la
  tipografía global en los `base_email.html` y plantillas asociadas.
- Las plantillas de correo deberían usar `--primary-500` (turquesa)
  para botones de acción y `--neutral-50` (`#F6F4F9`) como fondo de
  card. Esto se hace **en línea** con `style="background: #F6F4F9"`,
  ya que los clientes de correo no soportan CSS variables.
- Status pills (`--success-tint`, `--danger-tint`) son útiles en
  notificaciones de aprobación/rechazo de evidencia.