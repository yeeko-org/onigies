# Recomendaciones — integración frontend/backend del dashboard

Observaciones tras leer el sistema schema-driven completo (`/catalogs/all/` →
`cats.js` → `collection_data` → `CollectionDisplay` → `Panel*` →
auto-carga por convención). Ordenadas por **relación impacto/esfuerzo**: las
primeras son las que más rinden para un mantenedor solo.

Leyenda: 🟢 bajo esfuerzo · 🟡 medio · 🔴 alto · ⭐ alto impacto.

---

## ✅ 1. ⭐🟢 Extraer la auto-carga por convención a un solo composable

---

## ⛔ 2. ⭐🟡 Mover los guardados en cascada (`saveComplex`) al backend

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

## ⛔ 10. 🟢 Sacar los supuestos de dominio ajeno del código genérico

En `save_elements.js` hay nombres que no son de ONIGIES
(`involved`, `eventlocation`, `clicks`, `displacement_`, `participants`,
`interests`). Son herencia de otro proyecto y ensucian lógica que pretende ser
genérica.

**Recomendación:** si alguna excepción sigue siendo necesaria, declararla como
config de schema en el backend (p. ej. `skip_on_cascade`) en vez de un array
literal en JS. Si no, borrarlas. (Queda subsumido si haces §2.)

---

## ✅ 3. ⭐🟢 Hacer visible el fallback silencioso de la convención

## ✅ 4. ⭐🟡 Decidir dónde vive la lógica: backend vs `cats.js`

---

## ✅ 5. 🟡 Eliminar el camino de fetch muerto/paralelo

## ✅ 6. 🟢 Limpiar ruido de depuración en producción

## ✅ 8. 🟢 Unificar manejo de errores y nombres de eventos

---

## ➡ 7. 🟡 No mutar props; subir el cambio o centralizar la lista

`PanelsResult` y `PanelList` mutan `props.results` directamente
(`.unshift`, `.splice`, asignación por índice) tras guardar/borrar. Funciona en
Vue 3 con arrays reactivos, pero el dueño del array es el padre
(`CollectionDisplay`). Es un anti-patrón que dificulta razonar el flujo.

**Recomendación:** emitir el cambio hacia arriba (`@item-saved`, `@item-deleted`
ya existen) y que `CollectionDisplay` —dueño de `results`— aplique la mutación;
o mover la lista a una pequeña store/composable si se comparte. Decisión tuya:
es deuda de prolijidad, no un bug.

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

## 11. 🟡 Tipado del contrato `collection_data`

Todo es `Object` suelto. Siendo el `collection_data` el corazón del sistema,
un error de nombre de propiedad se descubre en runtime.

**Recomendación (incremental):** un `typedef` JSDoc de `collection_data` y
`field` para autocompletado/avisos en el IDE, sin migrar a TS. Si más adelante
adoptas TS, puedes **generar** los tipos desde el payload del backend (una sola
fuente).
