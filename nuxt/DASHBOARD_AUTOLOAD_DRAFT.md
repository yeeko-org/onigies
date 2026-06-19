# BORRADOR — Convención de auto-carga de componentes del dashboard

> Insumo para un **skill** que se escribirá en otra sesión. Es lo que sé de
> haberlo leído de pasada (`PanelCommon.vue`, `DialogEdit.vue`), **sin** una
> investigación exhaustiva. Verificar antes de convertirlo en skill.

## Idea

El dashboard genérico (colecciones schema-driven) **resuelve el componente de
detalle por convención de nombre**, importándolo dinámicamente. No hay registro
manual: basta crear el archivo con el nombre correcto en la carpeta de la app.

## Nombres y rutas

Dado `collection_data` con `app_label` (= `route_key`), `snake_name` (carpeta) y
`model_name` (PascalCase), se intentan importar:

```
~/components/dashboard/{app_label}/{snake_name}/{ModelName}Edit.vue
~/components/dashboard/{app_label}/{snake_name}/{ModelName}EditSimple.vue
~/components/dashboard/{app_label}/{snake_name}/{ModelName}Sheet.vue
```

Ej. para `example` / `good_practice_package` / `GoodPracticePackage`:
`~/components/dashboard/example/good_practice_package/GoodPracticePackageEditSimple.vue`.

## Quién monta qué (según lo visto)

- **`PanelCommon.vue`** (líneas ~21-47, 170-205):
  - Importa `{Model}Edit` y `{Model}EditSimple` dinámicamente; fallback de
    `Edit` → `common/generic/EditGeneric.vue`.
  - Si **existe `{Model}EditSimple`** → se renderiza **inline** como
    `edit_simple_component` con **solo** `v-model="full_main"`.
  - Si **no existe EditSimple** → usa `EditCommon` (con guardar/borrar) y dentro,
    vía slot `#edit`, monta `{Model}Edit` con la prop `is_edit`.
- **`DialogEdit.vue`** (líneas ~17, 34, 72-92): usa `{Model}Sheet`; fallback
  `common/generic/SheetCommon.vue`. `sheet_name = {model_name}Sheet`.

## Props que reciben

- `EditSimple` inline: **solo** `v-model="full_main"`. (No recibe `isStaff`; si
  el componente lo declara con default, ese default manda → en el dashboard la
  revisora suele quedar como staff por defecto.)
- `Edit` (dentro de EditCommon): `v-model` + `is_edit`.
- `Sheet`: `full_main` (y `show_details` en algún caso).

## Implicación práctica (la que motivó el refactor de flow)

Cualquier `{Model}EditSimple.vue` **es la vista de detalle de la revisora en el
dashboard**. Por eso no debe contener contenido del mundo IES (p. ej. la
pregunta `has_good_practices`). La vista IES vive aparte en `/respuestas`
(`GoodPracticeList.vue`), no por convención.

## Pendiente de verificar para el skill

- Cómo se calculan exactamente `model_name`, `snake_name`, `route_key`
  (¿desde `cats`/`schemas`?).
- Cuándo se usa `EditSimple` vs `Edit` vs `Sheet` (panel inline vs diálogo).
- Lista real de fallbacks genéricos en `common/generic/`.
- Si hay más props/eventos implícitos (`itemSaved`, `itemDeleted`, etc.).
