"""
Declaraciones de catálogo de la app ies.
"""
from ps_schema.registry import (
    catalog_registry, CatalogSchema, ComponentFilter)
from ies.models import Institution, Period
from api.views.ies.period_views import InstitutionCatalogViewSet


@catalog_registry.register
class InstitutionSchema(CatalogSchema):
    model = Institution
    level = "category_subtype"
    viewset_class = InstitutionCatalogViewSet
    filter_group_key = "institutions"
    # El filtrado real lo hace InstitutionCatalogViewSet.filterset_fields:
    # este schema usa viewset_class propio, así que filterset_fields aquí
    # no se aplicaría.
    all_filters = [
        ComponentFilter(
            title="De prueba", field="is_test",
            component="TripleBooleanFilter"),
    ]


@catalog_registry.register
class PeriodSchema(CatalogSchema):
    model = Period
    level = "category_subtype"      # name/plural via Meta.verbose_name
    filter_group_key = "periods"
