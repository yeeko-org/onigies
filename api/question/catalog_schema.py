"""
Declaraciones de catálogo de la app question.

AOption y QuestionType son catálogos category_subtype auto-generados (no
existían viewsets manuales). El filter group `a_options` usa FilterGroupSchema
porque su nombre difiere del verbose_name del modelo AOption.

GeneralQuestion (sección «Información de base») cuelga de
indicator.GeneralGroup y se edita desde el detalle de su grupo.

Las cinco preguntas por observable (A, B, alcance, planes, especial)
siguen el mismo patrón contra indicator.Observable: catálogo por tipo,
filtradas por observable y anidadas en el detalle del observable. Se
editan sus textos, nunca se crean ni se borran: las siembra
load_questionnaire y sus respuestas ya capturadas cuelgan de ellas.

Nota: AOption no tiene campo `name`; el endpoint CRUD auto-generado es nuevo
(antes no existía ruta), así que sólo fallaría una búsqueda por `name`, que
hoy no ocurría. Sin regresión respecto al estado previo.
"""
from ps_schema.registry import (
    catalog_registry, CatalogSchema, FilterGroupSchema)
from question.models import (
    AOption, AQuestion, BQuestion, GeneralQuestion, PlanQuestion,
    QuestionType, ReachQuestion, SpecialQuestion)
from api.views.confirm_delete import NoDeleteMixin
from api.views.question.serializers import (
    AQuestionCatalogSerializer, BQuestionCatalogSerializer,
    GeneralQuestionCatalogSerializer, PlanQuestionCatalogSerializer,
    ReachQuestionCatalogSerializer, SpecialQuestionCatalogSerializer)


class ObservableQuestionSchema(CatalogSchema):
    """Base de las cinco preguntas por observable.

    No se registra: solo comparte el nivel, el filtro por observable y
    la doble cerradura de alta y baja. Cada subclase pone su modelo, su
    serializer y sus nombres.
    """
    level = "category_subtype"
    filterset_fields = ['observable']
    extra_mixins = [NoDeleteMixin]
    cat_params = {"hide_create": True}


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


@catalog_registry.register
class AQuestionSchema(ObservableQuestionSchema):
    model = AQuestion
    name = "Opción de institucionalización"
    plural_name = "Opciones de institucionalización"
    serializer_class = AQuestionCatalogSerializer


@catalog_registry.register
class BQuestionSchema(ObservableQuestionSchema):
    model = BQuestion
    name = "Pregunta de transversalización"
    plural_name = "Preguntas de transversalización"
    serializer_class = BQuestionCatalogSerializer


@catalog_registry.register
class ReachQuestionSchema(ObservableQuestionSchema):
    model = ReachQuestion
    name = "Pregunta de alcance"
    plural_name = "Preguntas de alcance de población"
    serializer_class = ReachQuestionCatalogSerializer


@catalog_registry.register
class PlanQuestionSchema(ObservableQuestionSchema):
    model = PlanQuestion
    name = "Pregunta de planes"
    plural_name = "Preguntas de planes de estudio"
    serializer_class = PlanQuestionCatalogSerializer


@catalog_registry.register
class SpecialQuestionSchema(ObservableQuestionSchema):
    model = SpecialQuestion
    name = "Pregunta especial"
    plural_name = "Preguntas especiales"
    serializer_class = SpecialQuestionCatalogSerializer


@catalog_registry.register_filter_group
class AOptionsFilterGroup(FilterGroupSchema):
    key_name = "a_options"
    name = "Opción de Respuesta Institucionalización"
    plural_name = "Opciones de Respuesta Institucionalización"
    category_subtype = AOption
