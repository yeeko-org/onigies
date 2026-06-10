"""
Declaraciones de schema para colecciones del sistema.

Dos familias, separadas por level:

  CatalogSchema   — category_group / category_type / category_subtype
  CollectionSchema — primary / secondary / relational

Más FilterGroupSchema para grupos de filtros multi-nivel.

Los registries (catalog_registry, collection_registry) viven en registry.py.
Los imports públicos se re-exportan desde registry.py para no romper código
existente.
"""
from dataclasses import dataclass, asdict
from typing import Literal


CatalogLevel = Literal[
    "category_group", "category_type", "category_subtype",
]
MainLevel = Literal[
    "primary", "secondary", "relational",
]
CollectionLevel = Literal[
    "primary", "secondary", "relational",
    "category_group", "category_type", "category_subtype",
]


# ---------------------------------------------------------------------------
# Declaraciones de filtro tipadas (usadas en CollectionSchema.all_filters)
# ---------------------------------------------------------------------------

@dataclass
class FilterRef:
    """Referencia a un FilterGroup existente por key_name."""
    filter_name: str
    hidden: bool = False
    can_massive_edit: bool = False


@dataclass
class ComponentFilter:
    """Filtro renderizado como componente Vue en el dashboard."""
    title: str
    component: str
    field: str
    hidden: bool = False
    options: list | None = None        # para OnlyByFilter
    custom_options: list | None = None


def filter_to_dict(f: FilterRef | ComponentFilter) -> dict:
    """Serializa un filtro dataclass a dict plano, omitiendo los None."""
    return {k: v for k, v in asdict(f).items() if v is not None}


# ---------------------------------------------------------------------------
# BaseSchema — compartido por CatalogSchema y CollectionSchema
# ---------------------------------------------------------------------------

class BaseSchema:
    """
    Mixin de tipado puro. Solo los atributos genuinamente compartidos
    entre CatalogSchema y CollectionSchema. Sin lógica propia — toda la
    lógica vive en los registries.
    """
    model: type = None
    level: str = None           # tipo estricto definido en cada subclase
    name: str = None            # fallback: model._meta.verbose_name
    plural_name: str = None     # fallback: model._meta.verbose_name_plural
    can_merge: bool = False
    can_massive_edit: bool = False
    # Campos NO-filtro a habilitar en edición masiva (los filtros usan
    # FilterRef.can_massive_edit). Solo aplica si can_massive_edit=True.
    extra_massive_edit_fields: list = []
    sort_fields: list = []
    cat_params: dict = {}
    viewset_class: type | None = None


# ---------------------------------------------------------------------------
# CatalogSchema — category_group / category_type / category_subtype
# ---------------------------------------------------------------------------

class CatalogSchema(BaseSchema):
    """
    Declaración de una colección de tipo catálogo (category_*).

    Genera un ViewSet automáticamente para los patrones 1-3.
    Usa `viewset_class` para override manual (patrón 4).
    Puede declarar su FilterGroup simple con `filter_group_key`.
    """

    level: CatalogLevel = None

    # --- UI metadata --------------------------------------------------------
    open_insertion: bool = None
    optional_category: bool = False

    # --- Generación de ViewSet ----------------------------------------------
    # base / permission: claves resueltas por el registry desde
    # settings.PS_SCHEMA (BASE_VIEWSETS / PERMISSIONS). None = usar el
    # default del proyecto (DEFAULT_CATALOG_BASE / DEFAULT_CATALOG_PERMISSION).
    # También admite una clase directa.
    base: str | type | None = None
    permission: str | type | None = None

    # count_fields: {"annotation_name": "related_field_or_path"}
    count_fields: dict = {}

    # filterset_fields: None = heredar del base; [] = deshabilitar
    filterset_fields: list | None = None

    # extra_mixins: insertados antes de la clase base en el MRO
    extra_mixins: list = []

    # --- Serializers --------------------------------------------------------
    serializer_class: type | None = None
    full_serializer_class: type | None = None   # retrieve / create / update
    list_serializer_class: type | None = None   # list action

    # --- FilterGroup simple (un solo nivel de categoría) --------------------
    # filter_group_key auto-genera un FilterGroup para este schema. Solo
    # apto cuando este schema es el único category_subtype/type del grupo
    # (sin hermanos category_group / category_type).
    filter_group_key: str | None = None       # key_name del FilterGroup
    filter_group_addl_config: dict = {}


# ---------------------------------------------------------------------------
# CollectionSchema — primary / secondary / relational
# ---------------------------------------------------------------------------

class CollectionSchema(BaseSchema):
    """
    Declaración de una colección principal, secundaria o relacional.

    Siempre usa ViewSet manual — `viewset_class` es obligatorio.
    Alimenta el router principal vía `collection_registry.register_routes()`.
    """

    level: MainLevel = None

    # --- UI metadata (exclusivo de colecciones no-catálogo) -----------------
    open_insertion: bool = None
    color: str = None
    icon: str = None
    all_filters: list = []     # List[FilterRef | ComponentFilter]
    xls_export: bool = False
    xls_export_class: type | None = None
    can_massive_delete: bool = False

    # Si se define, register_routes también registra {snake_name}_mini
    mini_viewset_class: type | None = None


# ---------------------------------------------------------------------------
# FilterGroupSchema — grupos de filtros multi-nivel
# ---------------------------------------------------------------------------

class FilterGroupSchema:
    """
    Declaración de un FilterGroup que agrupa múltiples niveles de catálogo
    (category_group + category_type + category_subtype).

    Para grupos simples (solo category_subtype), usar
    `CatalogSchema.filter_group_key` en el schema correspondiente en lugar
    de esta clase.

    Se registra con `catalog_registry.register_filter_group`.
    """
    key_name: str = None
    name: str = None
    plural_name: str = None
    main_collection: str = None          # "app-snake_name"
    category_group: type | None = None   # modelo Django
    category_type: type | None = None    # modelo Django
    category_subtype: type | None = None  # modelo Django
    addl_config: dict = {}
