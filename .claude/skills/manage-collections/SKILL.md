---
name: manage-collections
description: >
  [api] Create or edit CatalogSchema, CollectionSchema, and FilterGroupSchema
  in {app}/catalog_schema.py. Use whenever the user adds a new collection,
  catalog, or filter group, modifies an existing one, mentions the registry
  (catalog_registry / collection_registry), or asks how a model becomes a
  /catalogs/ endpoint or a dashboard collection.
---

# manage-collections

## Architecture

The full attribute reference lives in `ps_schema/schemas.py`; registry logic
in `ps_schema/registry.py`. This skill covers design decisions only.

| Level | Schema | Registry | Router |
|-------|--------|----------|--------|
| `category_group/type/subtype` | `CatalogSchema` | `catalog_registry` | `api/views/catalogs/urls.py` |
| `primary/secondary/relational` | `CollectionSchema` | `collection_registry` | `api/urls.py` |

Still registered manually in `api/urls.py`: `collection`, `evidence`,
`invitation`, `user`, `institution` (survey flow), `survey`.

**Two `institution` endpoints by design — do not collapse them:**
`/institution/` (survey flow, the IES manages its own institution) and
`/catalogs/institution/` (admin manages the catalog, via registry).

## onigies defaults (settings.PS_SCHEMA)

- `base`: keys `generic` (default → `BaseGenericViewSet`), `status`
  (`BaseStatusViewSet`), `viewset` (`ModelViewSet`).
- `permission`: keys `editor` (default → `IsFullEditorOrReadOnly`),
  `admin` (`IsAdminOrReadOnly`), `any` (`AllowAny`).
- **Never use `base="status"` on catalogs**: no catalog model in onigies
  has `status_validation`.

---

## CatalogSchema — choosing a pattern

| Pattern | When | Key attributes |
|---------|------|----------------|
| **1 — Trivial** | Basic CRUD only | `model`, `level` |
| **2 — Count + filter** | Needs annotations or filters | `count_fields`, `filterset_fields` |
| **3 — Two serializers** | Different list vs retrieve | `list_serializer_class`, `full_serializer_class` |
| **4 — Override** | Custom logic | `viewset_class` |

Real example (`indicator/catalog_schema.py`):

```python
from ps_schema.registry import catalog_registry, CatalogSchema
from indicator.models import Component

@catalog_registry.register
class ComponentSchema(CatalogSchema):
    model = Component
    level = "category_type"
    filterset_fields = ['axis']                       # pattern 2
    full_serializer_class = ComponentFullSerializer   # pattern 3
```

Set `name` / `plural_name` only when `Meta.verbose_name` diverges from the
public name (e.g. `AxisSchema`: `name="Eje"` because the verbose_name is
"Materia (Axis)").

For a simple FilterGroup (a single `category_subtype`, no group/type
siblings), declare `filter_group_key` on the schema itself
(e.g. `SectorSchema`: `filter_group_key = "sectors"`).

---

## CollectionSchema

`viewset_class` is required. `mini_viewset_class` auto-registers a
`{snake}_mini` endpoint for lightweight selectors (optional).

`icon` and `color` are **initial defaults only**: written to the DB on the
first `migrate_ps_schemas` run and never overwritten, so frontend edits are
preserved. `help_text` and `description` are DB-only (no schema attribute);
edit them via the admin or the frontend.

Real example (`example/catalog_schema.py`):

```python
from ps_schema.registry import (
    collection_registry, CollectionSchema, FilterRef)
from example.models import GoodPractice
from api.views.example import GoodPracticeViewSet

@collection_registry.register
class GoodPracticeSchema(CollectionSchema):
    model = GoodPractice
    level = "primary"
    name = "Buena práctica"
    plural_name = "Buenas prácticas"
    viewset_class = GoodPracticeViewSet
    open_insertion = False
    all_filters = [FilterRef("institutions")]
    cat_params = {"init_display": True, "hide_create": True}
```

---

## ComponentFilter — available components

```python
ComponentFilter(title="Fechas", component="RangeDates", field="date")
ComponentFilter(title="Editor", field="editor", component="UserSelect",
                hidden=True)
ComponentFilter(title="Con archivos", field="has_files",
                component="TripleBooleanFilter", hidden=True)

# OnlyByFilter with fixed options:
ComponentFilter(title="Colección", field="only_by", component="OnlyByFilter",
                options=["good_practice", "evidence"])

# OnlyByFilter with custom options:
ComponentFilter(title="Status", field="status", component="OnlyByFilter",
                custom_options=[
                    {"plural_name": "Faltan validar", "value": "to_validate"},
                    {"plural_name": "Validados", "value": "validated"},
                ])
```

---

## FilterGroupSchema — multi-level filter groups

Use when the group needs `category_type` + `category_subtype` (or also
`category_group`). For single-`category_subtype` groups, use
`filter_group_key` directly on the model's `CatalogSchema` instead.

Real example (`indicator/catalog_schema.py`):

```python
from ps_schema.registry import catalog_registry, FilterGroupSchema
from indicator.models import Axis, Component, Observable

@catalog_registry.register_filter_group
class AxesFilterGroup(FilterGroupSchema):
    key_name = "axes"
    name = "Eje/Componentes"
    plural_name = "Ejes y Componentes"
    category_group = Axis
    category_type = Component
    category_subtype = Observable
```

---

## Auto-discovery (new apps only)

If the app does not yet import its `catalog_schema` in `ready()`:

```python
# {app}/apps.py
def ready(self):
    import {app}.catalog_schema  # noqa
```

## After touching a CollectionSchema

If `snake_name`, `level`, `icon`, or `color` of a primary collection
changed, run `python manage.py migrate_ps_schemas` to sync the overrides in
the `Collection` table (it only seeds primaries; catalogs never touch the DB).
