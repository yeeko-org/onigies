"""
Declaraciones de catálogo de la app ies.

Institution y Period son catálogos category_subtype. Institution reusa su
ViewSet manual (queryset anotado, serializer por acción, prefetch); Period
se auto-genera (CRUD plano sobre BaseGenericViewSet).
"""
from ps_schema.registry import catalog_registry, CatalogSchema
from ies.models import Institution, Period
from api.views.ies.period_views import InstitutionCatalogViewSet


@catalog_registry.register
class InstitutionSchema(CatalogSchema):
    model = Institution
    level = "category_subtype"
    name = "Institución"            # el modelo no define Meta.verbose_name
    plural_name = "Instituciones"
    viewset_class = InstitutionCatalogViewSet
    filter_group_key = "institutions"


@catalog_registry.register
class PeriodSchema(CatalogSchema):
    model = Period
    level = "category_subtype"      # name/plural via Meta.verbose_name
    filter_group_key = "periods"
