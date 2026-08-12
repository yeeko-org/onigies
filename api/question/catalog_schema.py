"""
Declaraciones de catálogo de la app question.

AOption y QuestionType son catálogos category_subtype auto-generados (no
existían viewsets manuales). El filter group `a_options` usa FilterGroupSchema
porque su nombre difiere del verbose_name del modelo AOption.

GeneralQuestion (sección «Información de base») cuelga de
indicator.GeneralGroup y se edita desde el detalle de su grupo.

Nota: AOption no tiene campo `name`; el endpoint CRUD auto-generado es nuevo
(antes no existía ruta), así que sólo fallaría una búsqueda por `name`, que
hoy no ocurría. Sin regresión respecto al estado previo.
"""
from ps_schema.registry import (
    catalog_registry, CatalogSchema, FilterGroupSchema)
from question.models import AOption, GeneralQuestion, QuestionType
from api.views.confirm_delete import NoDeleteMixin
from api.views.question.serializers import GeneralQuestionCatalogSerializer


@catalog_registry.register
class AOptionSchema(CatalogSchema):
    model = AOption
    level = "category_subtype"


@catalog_registry.register
class QuestionTypeSchema(CatalogSchema):
    model = QuestionType
    level = "category_subtype"


@catalog_registry.register
class GeneralQuestionSchema(CatalogSchema):
    model = GeneralQuestion
    level = "category_subtype"
    name = "Pregunta del grupo"     # el verbose_name trae sufijo largo
    plural_name = "Preguntas del grupo"
    # El grupo la anida en su detalle, pero el filtro deja abierta la
    # sub-lista paginada del Sheet genérico si algún grupo crece.
    filterset_fields = ['general_group']
    serializer_class = GeneralQuestionCatalogSerializer
    # Ninguna pregunta muere desde la API: se lleva las respuestas ya
    # capturadas (la FK de GeneralQuestionResponse es PROTECT).
    extra_mixins = [NoDeleteMixin]
    cat_params = {"hide_create": True}


@catalog_registry.register_filter_group
class AOptionsFilterGroup(FilterGroupSchema):
    key_name = "a_options"
    name = "Opción de Respuesta Institucionalización"
    plural_name = "Opciones de Respuesta Institucionalización"
    category_subtype = AOption
