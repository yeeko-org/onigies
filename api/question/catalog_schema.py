"""
Declaraciones de catálogo de la app question.

AOption y QuestionType son catálogos category_subtype auto-generados (no
existían viewsets manuales). El filter group `a_options` usa FilterGroupSchema
porque su nombre difiere del verbose_name del modelo AOption.

Nota: AOption no tiene campo `name`; el endpoint CRUD auto-generado es nuevo
(antes no existía ruta), así que sólo fallaría una búsqueda por `name`, que
hoy no ocurría. Sin regresión respecto al estado previo.
"""
from ps_schema.registry import (
    catalog_registry, CatalogSchema, FilterGroupSchema)
from question.models import AOption, QuestionType


@catalog_registry.register
class AOptionSchema(CatalogSchema):
    model = AOption
    level = "category_subtype"


@catalog_registry.register
class QuestionTypeSchema(CatalogSchema):
    model = QuestionType
    level = "category_subtype"


@catalog_registry.register_filter_group
class AOptionsFilterGroup(FilterGroupSchema):
    key_name = "a_options"
    name = "Opción de Respuesta Institucionalización"
    plural_name = "Opciones de Respuesta Institucionalización"
    category_subtype = AOption
