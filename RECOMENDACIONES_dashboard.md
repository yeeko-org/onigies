# Recomendaciones — integración frontend/backend del dashboard

Observaciones tras leer el sistema schema-driven completo (`/catalogs/all/` →
`cats.js` → `collection_data` → `CollectionDisplay` → `Panel*` →
auto-carga por convención). Ordenadas por **relación impacto/esfuerzo**: las
primeras son las que más rinden para un mantenedor solo.

Leyenda: 🟢 bajo esfuerzo · 🟡 medio · 🔴 alto · ⭐ alto impacto.

---

## 1. ⭐🟢 Extraer la auto-carga por convención a un solo composable

**Hoy:** el bloque que resuelve un componente por nombre (`import()` con
`.catch()` al genérico) está **copiado en cuatro archivos** —
`PanelCommon.vue`, `PanelsResult.vue`, `PanelList.vue`, `DialogEdit.vue`— con
variaciones sutiles (qué sufijos, qué fallback, si hay fallback). Es el patrón
más central del dashboard y el más repetido.

**Recomendación:** un composable único, p. ej.

```js
// composables/useDynamicComponent.js
export function useDynamicComponent(collectionData, suffix, fallback = null) {
  const comp = shallowRef('')
  const { app_label, snake_name, model_name } = collectionData
  const path = `~/components/dashboard/${app_label}/${snake_name}/${model_name}${suffix}.vue`
  import(/* @vite-ignore */ path)
    .then(m => { comp.value = m.default })
    .catch(() => {
      if (fallback) import(fallback).then(m => { comp.value = m.default })
    })
  return comp
}
```

Uso: `const header = useDynamicComponent(props.collection_data, 'Header', '.../HeaderGeneric.vue')`.

**Por qué:** una sola fuente de verdad para la convención. Hoy si cambias la
ruta o el naming tienes que tocar 4 lugares y es fácil que diverjan. Además
permite añadir en un solo punto el aviso de §3.

> Nota Vite: las rutas totalmente dinámicas requieren que el patrón sea
> analizable. Si el `import()` con plantilla deja de funcionar al extraerlo,
> usa `import.meta.glob('~/components/dashboard/**/*.vue', { eager:false })` y
> resuelve contra ese mapa — de paso te da la lista de componentes existentes.

---

## 2. ⭐🟡 Mover los guardados en cascada (`saveComplex`) al backend

**Hoy:** `composables/save_elements.js::saveOneToMany`/`saveComplex` arma a
mano una cascada de guardados de relaciones `one_to_many`, contando peticiones
(`total_requests += 2`, `resolved_requests`), con recursión, banderas
(`first_special`, `normal_save`) y un `participants_dict`. Es frágil:
concurrencia manual, sin transacción, y arrastra supuestos de otro proyecto
(`['involved','eventlocation','clicks']`, `displacement_`, `participants`).

**Recomendación:** un endpoint transaccional por colección que reciba el objeto
con sus hijos y los persista en el servidor (serializers anidados escribibles
de DRF, o una acción `@action` que envuelva en `transaction.atomic`). El
frontend manda **una** petición y recibe el árbol guardado.

**Por qué:** atomicidad (hoy un fallo a mitad deja datos a medias), menos
código frágil en el cliente, y elimina los arrays hardcodeados de exclusión.
Es el cambio que más reduce superficie de bugs difíciles.

---

## 3. ⭐🟢 Hacer visible el fallback silencioso de la convención

**Hoy:** si te equivocas en el nombre de `{Model}Header.vue` (mayúscula,
carpeta, sufijo), el `.catch()` carga el genérico **sin avisar**. Depurar
"¿por qué no aparece mi componente?" es a ciegas.

**Recomendación:** en el composable de §1, en modo dev,
`console.warn` cuando se cae al fallback, indicando la ruta intentada. Mejor
aún: validar contra el mapa de `import.meta.glob` y avisar solo si el archivo
*no existe* (distinguir "no lo creé" de "error al cargarlo").

---

## 4. ⭐🟡 Decidir dónde vive la lógica: backend vs `cats.js`

`cats.js` **re-deriva** en el cliente cosas que el backend ya sabe: `pk`,
`name_field`, `has.*`, `other_fields`, `child_relation_fields`,
`status_groups`. Es ~135 líneas que mezclan responsabilidades y tienen
`console.log` de depuración dentro.

**Recomendación:** mover esa derivación al payload del backend
(`ps_schema/registry.py` ya calcula `fields[]` y los metadatos base — puede
calcular también `name_field`, `pk`, `has`, etc.). El frontend quedaría como
consumidor "tonto" de un contrato más rico. Si prefieres mantenerlo en el
cliente, al menos **partir `calculateSchemas`** en funciones pequeñas y
testeables (`enrichFields`, `buildFilters`, `buildSorts`).

**Por qué:** una sola fuente de verdad del esquema y menos lógica duplicada en
dos lenguajes. Hoy un cambio de convención (p. ej. añadir `subtitle` a
`name_fields`) implica tocar JS aunque el modelo viva en Python.

---

## 5. 🟡 Eliminar el camino de fetch muerto/paralelo

`composables/fetch.js` exporta refs **a nivel de módulo** (`results`,
`final_filters`, `applyFilters`, …) pero `CollectionDisplay.vue` **redefine
todo localmente** y no usa el composable. Hay dos implementaciones del mismo
concepto.

**Riesgo extra:** los refs a nivel de módulo son **singletons compartidos**
entre instancias. Como `SheetCommon` monta un `CollectionDisplay` anidado
dentro de otro, si alguien volviera a `fetch.js` esas instancias colisionarían.

**Recomendación:** borrar el estado exportado de `fetch.js` (o convertirlo en
una *factory* `useCollectionFetch()` que devuelva refs nuevos por instancia) y
dejar `CollectionDisplay` como único dueño. Documentar cuál es el camino vivo.

---

## 6. 🟢 Limpiar ruido de depuración en producción

`console.log` sembrados en código de runtime: `cats.js` (logs de
`category_group`), `store/index.js` ("previous to setCollectionData"),
`nodes.js`. Y placeholders canario en plantillas (`EDICIÓN 1 (REPORTAR...)`,
`EditGeneric` volcando `{{full_main}}`, "Sheet genérico 3").

**Recomendación:** quitar o envolver en `if (import.meta.dev)`. Los canarios
de plantilla puedes conservarlos pero documentarlos como intencionales en el
skill (ya lo están como fallback).

---

## 7. 🟡 No mutar props; subir el cambio o centralizar la lista

`PanelsResult` y `PanelList` mutan `props.results` directamente
(`.unshift`, `.splice`, asignación por índice) tras guardar/borrar. Funciona en
Vue 3 con arrays reactivos, pero el dueño del array es el padre
(`CollectionDisplay`). Es un anti-patrón que dificulta razonar el flujo.

**Recomendación:** emitir el cambio hacia arriba (`@item-saved`, `@item-deleted`
ya existen) y que `CollectionDisplay` —dueño de `results`— aplique la mutación;
o mover la lista a una pequeña store/composable si se comparte. Decisión tuya:
es deuda de prolijidad, no un bug.

---

## 8. 🟢 Unificar manejo de errores y nombres de eventos

- **Errores inconsistentes:** algunas acciones devuelven `{errors}`
  (`saveSimple`, `deleteSimple`), otras tragan el error y devuelven `undefined`
  (`getSimple`, `patchSimple`). El consumidor no sabe qué esperar.
  → Estandarizar vía `useApiError`/`notifyApiError` (ya existe) y un retorno
  uniforme `{data}|{errors}`.
- **Eventos:** conviven `item-saved`/`itemSaved`, `update-page-number`,
  `select-item`. → fijar kebab-case en plantillas y un glosario corto.

---

## 9. 🟡 Cerrar la migración de status al motor `flow`

`HeaderCommon` ya bifurca: si `main.status` es objeto usa `FlowStatusChip`
(motor nuevo), si no, los `status_groups` viejos con `status_filters`
**hardcodeado** en `composables/filters.js`. Mientras coexistan, hay dos
modelos mentales de estado y un mapa de status duplicado en el front.

**Recomendación:** terminar la migración (ver skill `flow` y
`PLAN_flujo_validacion.md`), hacer que el backend entregue la metadata de
status, y borrar `status_filters` del front. Reduce un punto de verdad
duplicado y simplifica `HeaderCommon`/`EditCommonFields`.

---

## 10. 🟢 Sacar los supuestos de dominio ajeno del código genérico

En `save_elements.js` hay nombres que no son de ONIGIES
(`involved`, `eventlocation`, `clicks`, `displacement_`, `participants`,
`interests`). Son herencia de otro proyecto y ensucian lógica que pretende ser
genérica.

**Recomendación:** si alguna excepción sigue siendo necesaria, declararla como
config de schema en el backend (p. ej. `skip_on_cascade`) en vez de un array
literal en JS. Si no, borrarlas. (Queda subsumido si haces §2.)

---

## 11. 🟡 Tipado del contrato `collection_data`

Todo es `Object` suelto. Siendo el `collection_data` el corazón del sistema,
un error de nombre de propiedad se descubre en runtime.

**Recomendación (incremental):** un `typedef` JSDoc de `collection_data` y
`field` para autocompletado/avisos en el IDE, sin migrar a TS. Si más adelante
adoptas TS, puedes **generar** los tipos desde el payload del backend (una sola
fuente).

---

## Orden sugerido de ejecución

1. **§1 + §3** (composable de auto-carga con aviso) — desbloquea y limpia 4
   archivos, riesgo casi nulo.
2. **§5 + §6** (borrar fetch muerto y logs) — limpieza rápida.
3. **§4** (mover derivación de schema al backend) — define la frontera FE/BE.
4. **§2 + §10** (cascada al backend) — la mayor ganancia de robustez.
5. **§9** (cerrar flow), **§7/§8/§11** — prolijidad continua.

> Principio transversal: el dashboard es excelente como *motor genérico*. El
> riesgo no es la idea, es la **erosión** — convención repetida a mano, lógica
> duplicada en dos lenguajes y restos de otro proyecto. Cada punto de arriba
> empuja hacia "una sola fuente de verdad por concepto".
