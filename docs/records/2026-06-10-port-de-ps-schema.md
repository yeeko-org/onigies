---
type: record
id: 2026-06-10-port-de-ps-schema
title: Port del sistema de colecciones (ps_schema) de ibero a onigies
date: 2026-06-10
validate-paths: false
---

# Port del sistema de colecciones (ps_schema) de ibero → onigies

**Estado:** PORT COMPLETO. Fases 0-3 ✓, migraciones aplicadas, diff live
limpio, smoke visual OK, skill copiado, open_insertion backportado a ibero.
**Origen:** `D:\dev\ibero\ocs-django-db` (rediseño reciente + skill `manage-collections`).
**Destino:** `D:\dev\unam\onigies\api`.

## Objetivo y decisiones de fondo (ya tomadas)

1. **Copia local, sin paquete por ahora.** Cuando exista un 3er proyecto se comparan
   las dos versiones y se evalúa abstraer un paquete. (Por eso conviene dejar los seams
   inyectables desde ya — ver Fase 0 #1.)
2. **Igualar a ibero: modelos slim.** Borrar modelos `Level` y `FilterGroup`; reducir
   `Collection` a 6 campos (`snake_name`, `level` CharField+`LEVEL_CHOICES`, `order`,
   `icon`, `color`, `help_text`, `description`). La fuente de verdad en runtime pasa de
   la DB a las clases Python (registry). La tabla `Collection` solo guarda overrides
   editables.
3. **Orden:** mecánica de ps_schema primero, luego las apps; el teardown de modelos
   (destructivo, con migraciones) va al final.

## Patrón clave
Hoy la fuente de verdad es la **DB** (`constants.py` siembra tablas ricas, `CatalogsView`
lee de ellas). Después son las **clases Python**: `registry` genera viewsets, rutas y el
dump en runtime (`get_collections_data`, `iter_filter_group_data`, `get_catalog_dump`).
Frontend Nuxt verificado compatible: `cats.js` consume la misma forma que produce el
registry de ibero.

## Hallazgos de auditoría (onigies)

- **Ningún modelo de catálogo tiene `status_validation`** (Axis, Component, Observable,
  Sector, Institution, Period, Feature, FeatureOption, AOption, QuestionType). Solo
  `GoodPractice*` tienen `status_sending`; survey/answer tienen `status_register`.
  → Los defaults de ibero (`base="status"`, `permission="editor"`/`IsEditorOrCreateOrRead`)
  **romperían**. Defaults para onigies: `base="generic"`, `permission="editor"` mapeado a
  `IsFullEditorOrReadOnly`.
- **Permisos que ya existen en onigies** (`api/permissions.py`): `IsFullEditorOrReadOnly`
  (escribe `is_reviewer`), `IsAdminOrReadOnly` (escribe `is_admin`), `IsReviewer`,
  `IsSuperuser`. NO usar `IsEditorOrCreateOrRead` para catálogos (asume `status_validation`).
- **Base viewsets ya existen** (`api/views/common_views.py`): `BaseViewSet`,
  `BaseGenericViewSet`, `BaseStatusViewSet`.
- **`camel_to_snake`** vive en `utils.obj_str` (en ibero es `utils.universal`).
- **`yeeko_xlsx_export`** instalado en el venv ✓.
- **onigies YA tiene CRUD por catálogo** en `api/views/catalogs/urls.py` (registrados a
  mano): period, institution (`InstitutionCatalogViewSet`), feature, feature_option,
  feature_good_practice, axis, component, observable, sector. → En Fase 2 estos se
  reemplazan por `catalog_registry.register_routes` (quitar línea manual al migrar cada uno,
  para evitar doble registro).
- **Serializers no triviales a conservar** como `full_serializer_class`:
  `ComponentFullSerializer` (anida observables), `FeatureFullSerializer` (anida
  feature_options). El resto es `__all__` → auto-gen.
- **Dos endpoints `institution` por diseño, NO colapsar:**
  - `/institution/` (`InstitutionViewSet`, survey flow): la IES gestiona su institución
    (upload_logo). Front: `ies.js updateLogo` → `institution/{id}/upload_logo/`.
  - `/catalogs/institution/` (`InstitutionCatalogViewSet`): admin gestiona el catálogo.
    Front: dashboard `saveCatalog`.

## Mapeo de apps (de `constants.py` → catalog_schema.py)

- **ies**: `Institution`, `Period` (CatalogSchema, category_subtype). Filter groups:
  `institutions`, `periods`.
- **indicator**: `Axis` (category_group), `Component` (category_type, full=ComponentFull),
  `Observable` (category_subtype), `Sector` (category_subtype). Filter groups: `axes`
  (multinivel group/type/subtype), `sectors`.
- **example**: `Feature` (category_type, full=FeatureFull), `FeatureOption`
  (category_subtype) [CatalogSchema]; `GoodPracticePackage`, `GoodPractice`,
  `FeatureGoodPractice` (primary) [CollectionSchema con viewset_class existente].
  Filter group: `features`.
- **question**: `AOption`, `QuestionType` (category_subtype). Filter group: `a_options`.

## Fases

### Fase 0 — Mecánica (aditiva, no toca modelos ni constants)
Crear en `api/ps_schema/`:
- `schemas.py` — copia de ibero; cambiar default `base="status"` → `"generic"`.
- `registry.py` — copia de ibero con seams resueltos vía `settings.PS_SCHEMA` +
  `import_string` (NO imports en duro). `camel_to_snake` desde `utils.obj_str`.
- `__init__.py` — añadir `generate_serializer`.
- `core/settings`: añadir bloque `PS_SCHEMA` (BASE_VIEWSETS, PERMISSIONS,
  DEFAULT_CATALOG_BASE, DEFAULT_CATALOG_PERMISSION).
- Validación: `import ps_schema.registry` sin error.

### Fase 1 — Declarar apps (registra en el registry, aún nadie lee)
Por app: crear `{app}/catalog_schema.py` + `import {app}.catalog_schema` en `apps.ready()`.
Auditar cada catalog viewset existente: lógica propia → `viewset_class`; CRUD plano →
auto-gen. Revisar viewset por viewset con Ricardo.

### Fase 2 — Conmutar runtime al registry (cambio observable)
- `catalogs/urls.py`: `catalog_registry.register_routes(router)`; quitar registros manuales
  ya migrados.
- `catalogs/all.py` (`CatalogsView`): collections/filter_groups/dump desde el registry;
  `levels` desde `LEVEL_CHOICES`; conservar status_control e institution-by-auth.
- `api/urls.py`: `collection_registry.register_routes(router)`; quitar rutas primary
  duplicadas (good_practice, good_practice_package, feature_good_practice). Mantener
  `/institution/` (survey flow) y `/collection/` (meta).
- Validación crítica: diff de `/catalogs/all/` antes/después (script en `.claude/`).

### Fase 3 — Teardown de modelos + limpieza (migraciones que corre Ricardo)
- `ps_schema/models.py`: Collection slim; borrar Level y FilterGroup.
- Reemplazar `initial_data.py` y `migrate_ps_schemas.py` por versiones slim.
- Borrar `constants.py`.
- Adaptar `catalogs/serializers.py` (quitar Level/FilterGroup) y `ps_schemas/`.
- Ricardo corre `makemigrations`/`migrate`.

### Skill
Copiar `manage-collections/SKILL.md` a `.claude/skills/` adaptado a onigies (apps reales,
nombres de permisos, settings PS_SCHEMA, rutas). `create-skill/SKILL.md` borrado en git
status es no relacionado, no tocar.

## Decisiones resueltas
1. Maps base/permiso → configurables vía `settings.PS_SCHEMA` + import_string. ✓
2. Conservar `ComponentFullSerializer` y `FeatureFullSerializer`; resto auto-gen. ✓
3. Dos endpoints institution: mantener ambos, no colapsar. ✓

## Log de avance
- 2026-06-09: investigación completa, plan y decisiones cerradas.
- 2026-06-09: Fase 0 hecha. Creados `ps_schema/schemas.py` (defaults base/permission
  = None, resueltos por registry), `ps_schema/__init__.py` (generate_serializer),
  `ps_schema/registry.py` (seams desde settings.PS_SCHEMA + import_string,
  camel_to_snake desde utils.obj_str, sin `from __future__ import annotations`).
  Añadido bloque `PS_SCHEMA` en `core/settings/__init__.py`. Validado:
  imports OK, base default→BaseGenericViewSet, permiso default→IsFullEditorOrReadOnly.
  (RuntimeWarning de DB en app init es preexistente, no relacionado.)
- 2026-06-09: Fase 1 — app `ies`. Creado `ies/catalog_schema.py`
  (InstitutionSchema con viewset_class=InstitutionCatalogViewSet + name explícito
  porque el modelo no tiene Meta.verbose_name; PeriodSchema auto-gen). Enganchado
  `import ies.catalog_schema` en `ies/apps.py::ready()`. Validado: registro,
  viewsets y filter groups (institutions/periods) coinciden con constants.
  Decisión de auditoría: viewset propio si hay queryset anotado / serializer por
  acción / prefetch (Institution); auto-gen si es CRUD plano (Period).
- 2026-06-09: Fase 1 — apps indicator, example, question.
  - indicator: Axis(group)/Component(type)/Observable(subtype)/Sector(subtype),
    todos auto-gen. Component full_serializer=ComponentFullSerializer + filter axis;
    Observable filter component. Filter group `axes` multinivel (FilterGroupSchema).
    `sectors` vía filter_group_key. name/plural explícitos donde el verbose_name
    diverge (Eje, Observable/Observables, Sector Poblacional).
  - example: Feature(type, full=FeatureFull)/FeatureOption(subtype) catálogos;
    GoodPracticePackage/GoodPractice/FeatureGoodPractice primary con viewset_class
    (acciones send/discard/reopen, ActionFileMixin). Filter group `features`.
    Nombres en minúscula como en DB. OJO: open_insertion no existe en
    CollectionSchema → registry manda None (antes False); verificar en diff Fase 2.
  - question: AOption/QuestionType subtype auto-gen (no había viewsets). Filter
    group `a_options` con FilterGroupSchema (nombre difiere del verbose_name).
    AOption sin campo `name`: endpoint CRUD nuevo, sólo fallaría búsqueda por name.
  - Validación: `.claude/validate_ps_schema_fase1.py` → paridad total vs constants
    (colecciones, niveles, nombres explícitos, filter groups). `manage.py check`
    limpio (solo staticfiles.W004 preexistente).
  - Pendiente Fase 2: rutas nuevas que se agregan al conmutar (catalog_registry):
    /catalogs/a_option/, /catalogs/question_type/ (antes inexistentes). Dump nuevo:
    question_type. Confirmar en el diff de /catalogs/all/.
- 2026-06-09: Fase 2 (código). Editados:
  - `catalogs/all.py` (CatalogsView): collections = collection_registry +
    catalog_registry get_collections_data; filter_groups = iter_filter_group_data;
    dump = get_catalog_dump. status_control y levels siguen manuales (levels desde
    modelo Level hasta Fase 3).
  - `catalogs/urls.py`: catalog_registry.register_routes (quitados los registros
    manuales). `api/urls.py`: collection_registry.register_routes (quitados
    good_practice / good_practice_package / feature_good_practice manuales; import
    reducido a EvidenceViewSet).
  - Validado (sin tocar StatusControl): URLconf carga; registry rinde 13 colecciones
    (3 primary + 10 catálogo), 6 filter groups, dump con 10 catálogos incl.
    question_type. Routers: /catalogs/ gana a_option+question_type y pierde
    feature_good_practice; main conserva su set (primaries vía registry).
  - DIFFS DE SHAPE a confirmar en el diff live (cuando is_default esté migrado):
    (a) colecciones catálogo YA NO traen `order` (las primary sí, vía override DB);
    (b) primaries mandan open_insertion=None (antes False);
    (c) dump y collections ganan question_type.
  - BLOQUEO: `/catalogs/all/` falla por ies_statuscontrol.is_default inexistente
    (cambio en models.py sin migración; rama paralela de Ricardo). Rompe igual antes
    y después; es ortogonal. Ricardo debe `makemigrations ies` + `migrate`.
  - Para el diff live cuando la DB esté sana: usar `.claude/catalogs_tool.py`. Como el
    código de Fase 2 ya está aplicado, el "antes" se obtiene con git stash de los
    archivos tracked (catalogs/all.py, catalogs/urls.py, api/urls.py, los apps.py)
    → capture → unstash → capture → diff. Alternativa: smoke test del dashboard Nuxt.
- 2026-06-09: open_insertion soportado en CollectionSchema (schemas.py + registry
  iter_collection_data usa schema_cls.open_insertion; las 3 primary de example lo
  fijan en False). NOTA: backportar a ibero (allá también se perdía).
- 2026-06-09: Diff live `/catalogs/all/` antes/después (is_default ya migrado por
  Ricardo, nueva migración ies 0009). Resultado limpio. Diferencias y veredictos:
  * question_type nuevo (intencional). extra_massive_edit_fields:[] nuevo (inofensivo).
  * order:null en colecciones catálogo (las primary lo conservan vía override DB).
    Aprobado por Ricardo; iguala a ibero. Si el nav del dashboard se reordena feo,
    restaurar agregando order en catalog_registry.get_collections_data.
  * open_insertion: PRESERVADO (fix aplicado, primary siguen en False).
  * all_filters gana can_massive_edit:false (default FilterRef; inofensivo).
  * filter_groups[].order:null (antes 5; el front lo sobreescribe a 1). Irrelevante.
  * fields/name/level/cat_params/available_actions/icon/color: SIN cambios.
  Capturas en .claude/catalogs_before.json y catalogs_after.json.
- 2026-06-09: Smoke test. (a) Inspección del front: el nav del dashboard
  (nuxt/app/layouts/dashboard.vue, main_items y main_collections) está HARDCODEADO
  (labels/iconos/color/orden propios, referencia colecciones solo por snake_name);
  NO lee coll.order de la API → order:null en catálogos no afecta el nav.
  (b) HTTP real: runserver + GET /api/catalogs/all/ → 200, 13 colecciones,
  6 filter groups, question_type presente. Fase 2 cerrada.
- 2026-06-10: Fase 3 (código). Grep previo: las referencias a Level/FilterGroup
  resultaron más acotadas que lo anticipado — InitLevels vivía en
  ps_schema/initial_data.py (no en ies/); ies/admin.py y generate_data_dict
  no tocan esos modelos. Cambios:
  - models.py: LEVEL_CHOICES + Collection slim (7 campos, level CharField);
    eliminados Level y FilterGroup (y la línea muerta `something = [...]`).
  - initial_data.py y migrate_ps_schemas.py reemplazados por versiones ibero
    (InitCollections siembra solo overrides desde collection_registry;
    icon/color solo en creación, level siempre sincronizado).
  - catalogs/all.py: levels desde LEVEL_CHOICES ({key_name, name}).
  - catalogs/serializers.py: fuera Level/Collection/FilterGroup serializers.
  - ps_schemas/serializers.py: CollectionSerializer con lista explícita de
    7 campos (igual a ibero); el viewset no cambia (ya era idéntico).
  - admin.py: igualado a ibero (solo CollectionAdmin slim).
  - constants.py BORRADO (ya sin imports en api/; los scripts
    .claude/validate_* de Fases 1-2 quedan obsoletos, son desechables).
  - Validación: manage.py check limpio (solo warnings preexistentes).
    Diff live BLOQUEADO hasta migrar: la tabla tiene level_id (FK) y el
    modelo busca level (CharField) — mismo patrón que is_default en Fase 2.
  - Delta esperado del contrato tras migrar: levels[].order desaparece;
    verificado que el front no lo usa (cats.js guarda data.levels pero
    nadie lo consume).
  - PASOS DE RICARDO: (1) makemigrations ps_schema — al agregar level
    CharField non-null Django pedirá default: dar '' como one-off default;
    (2) migrate; (3) migrate_ps_schemas (repuebla level de las 3 primary y
    preserva icon/color/order); (4) opcional: borrar filas huérfanas de
    catálogo en Collection (institution, period, axis, ... — nadie las lee,
    collection_registry solo matchea primaries); (5) diff live:
    catalogs_tool.py capture + diff vs catalogs_after.json.
- 2026-06-10: Cierre. Ricardo corrió makemigrations/migrate/migrate_ps_schemas.
  - Paso 4: borradas las 10 filas huérfanas de catálogo en Collection
    (institution, period, axis, component, observable, sector, feature,
    feature_option, a_option, question_type); quedan solo las 3 primary.
  - Paso 5: diff live vs catalogs_after.json LIMPIO — única diferencia:
    levels[].order desaparece (esperada; el front no consume levels del
    store). Captura en .claude/catalogs_fase3.json.
  - Pendiente (a) smoke visual: hecho con Playwright MCP contra servers
    reales (:8018/:3018), auth simulada en el browser (route mock de
    GET /login/ con usuario staff ficticio + header Authorization removido
    para que la API trate las llamadas como anónimas; sin tocar DB ni crear
    usuarios). Nav del dashboard correcto (principal + Gestión Catálogos
    expandido) y vista /dashboard/catalog/axes renderiza los 4 ejes con
    orden/iconos. Capturas en .claude/dashboard-*.png. Exploración one-off:
    no amerita test e2e nuevo.
  - Pendiente (b): skill manage-collections creado en .claude/skills/
    adaptado a onigies (defaults generic/editor, ejemplos reales de
    indicator/example, nota de los dos endpoints institution).
  - Pendiente (c): backport a ibero aplicado (schemas.py CollectionSchema
    open_insertion + registry.py iter_collection_data lo propaga);
    py_compile OK. Falta commitearlo en ibero.
  - NOTA entorno nuxt: `pnpm dev` falla en no-TTY porque corepack bajó
    pnpm 11.5.3 y quiere purgar/reinstalar node_modules. Workaround usado:
    `node node_modules/nuxt/bin/nuxt.mjs dev`. Ricardo: correr `pnpm install`
    interactivo cuando convenga.
