"""
Declaraciones de catálogo de la app indicator.

Jerarquía Axis (group) → Component (type) → Observable (subtype), más Sector.
Todos se auto-generan. Component lleva full_serializer (retrieve anida
observables; la list cae al auto-gen plano) y filtra por axis; Observable
filtra por component. El filter group `axes` es multinivel.

GeneralGroup (sección «Información de base») también es catálogo: su
pregunta hija vive en question/catalog_schema.py. No lleva filter group
porque su PK es un slug, no un id, y el árbol D3 de filtros estratifica
por id; se llega a él por colección, no por `/dashboard/catalog/`.
"""
from ps_schema.registry import (
    catalog_registry, CatalogSchema, FilterGroupSchema)
from indicator.models import (
    Axis, Component, GeneralGroup, Observable, Sector)
from api.views.confirm_delete import NoDeleteMixin
from api.views.indicator.serializers import (
    ComponentFullSerializer, GeneralGroupCatalogSerializer)


@catalog_registry.register
class AxisSchema(CatalogSchema):
    model = Axis
    level = "category_group"
    name = "Eje"                    # Meta.verbose_name es "Materia (Axis)"
    plural_name = "Ejes"


@catalog_registry.register
class ComponentSchema(CatalogSchema):
    model = Component
    level = "category_type"
    filterset_fields = ['axis']
    full_serializer_class = ComponentFullSerializer


@catalog_registry.register
class ObservableSchema(CatalogSchema):
    model = Observable
    level = "category_subtype"
    name = "Observable"             # Meta.verbose_name trae sufijo largo
    plural_name = "Observables"
    filterset_fields = ['component']


@catalog_registry.register
class SectorSchema(CatalogSchema):
    model = Sector
    level = "category_subtype"
    name = "Sector Poblacional"
    plural_name = "Sectores Poblacionales"
    filter_group_key = "sectors"


@catalog_registry.register
class GeneralGroupSchema(CatalogSchema):
    model = GeneralGroup
    level = "category_type"
    name = "Grupo de preguntas base"
    plural_name = "Preguntas base"
    full_serializer_class = GeneralGroupCatalogSerializer
    # Los grupos los crea el seed (load_questionnaire); desde el
    # dashboard solo se editan sus textos y no se borra ninguno.
    extra_mixins = [NoDeleteMixin]
    cat_params = {"hide_create": True}


@catalog_registry.register_filter_group
class AxesFilterGroup(FilterGroupSchema):
    key_name = "axes"
    name = "Eje/Componentes"
    plural_name = "Ejes y Componentes"
    category_group = Axis
    category_type = Component
    category_subtype = Observable
