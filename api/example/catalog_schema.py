"""
Declaraciones de catálogo y colección de la app example.

Catálogos (category_*): Feature (full_serializer anida options en retrieve),
FeatureOption. Filter group `features` (type + subtype).

Colecciones primary (ViewSet manual con acciones/mixins propios):
GoodPracticePackage, GoodPractice, FeatureGoodPractice. Conservan los nombres
en minúscula tal como están hoy en la DB (constants), no el verbose_name.
"""
from ps_schema.registry import (
    catalog_registry, collection_registry,
    CatalogSchema, CollectionSchema, FilterGroupSchema, FilterRef)
from example.models import (
    Feature, FeatureOption, GoodPracticePackage, GoodPractice,
    FeatureGoodPractice)
from api.views.example import (
    GoodPracticePackageViewSet, GoodPracticeViewSet,
    FeatureGoodPracticeViewSet)
from api.views.example.serializers import FeatureFullSerializer


@catalog_registry.register
class FeatureSchema(CatalogSchema):
    model = Feature
    level = "category_type"
    full_serializer_class = FeatureFullSerializer


@catalog_registry.register
class FeatureOptionSchema(CatalogSchema):
    model = FeatureOption
    level = "category_subtype"


@catalog_registry.register_filter_group
class FeaturesFilterGroup(FilterGroupSchema):
    key_name = "features"
    name = "Característica"
    plural_name = "Características"
    category_type = Feature
    category_subtype = FeatureOption


@collection_registry.register
class GoodPracticePackageSchema(CollectionSchema):
    model = GoodPracticePackage
    level = "primary"
    name = "Envío de buenas prácticas"
    plural_name = "Envíos de buenas prácticas"
    viewset_class = GoodPracticePackageViewSet
    open_insertion = False
    all_filters = [FilterRef("periods")]
    cat_params = {"init_display": True, "hide_create": True}


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


@collection_registry.register
class FeatureGoodPracticeSchema(CollectionSchema):
    model = FeatureGoodPractice
    level = "primary"
    name = "Relación característica - buena práctica"
    plural_name = "Relaciones característica - buena práctica"
    viewset_class = FeatureGoodPracticeViewSet
    open_insertion = False
