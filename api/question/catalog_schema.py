"""
Declaraciones de catálogo de la app question.
"""
from ps_schema.registry import (
    catalog_registry, CatalogSchema, FilterGroupSchema)
from question.models import (
    AOption, AQuestion, BQuestion, GeneralQuestion, ObservableQuestionType,
    PlanQuestion, QuestionType, ReachQuestion, SpecialQuestion)
from api.views.confirm_delete import NoDeleteMixin
from api.views.question.serializers import (
    AQuestionCatalogSerializer, BQuestionCatalogSerializer,
    GeneralQuestionCatalogSerializer, ObservableQuestionTypeSerializer,
    PlanQuestionCatalogSerializer, QuestionTypeCatalogSerializer,
    ReachQuestionCatalogSerializer, SpecialQuestionCatalogSerializer)


class ObservableQuestionSchema(CatalogSchema):
    """Base sin registrar de las cinco preguntas por observable: se
    siembran y nunca se crean ni se borran desde la API, porque sus
    respuestas ya capturadas cuelgan de ellas."""
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
    name = "Tipo de pregunta"
    plural_name = "Tipos de pregunta"
    # `name` es la clave interna (PK de texto), no el rótulo a leer.
    name_field = "public_name"
    serializer_class = QuestionTypeCatalogSerializer
    count_fields = {"observables_count": "observable_weights"}
    # Los seis tipos los fija migrate_initial_data y el código los busca
    # por `name`: solo se editan rótulos y ponderaciones.
    extra_mixins = [NoDeleteMixin]
    cat_params = {"hide_create": True}


@catalog_registry.register
class ObservableQuestionTypeSchema(CatalogSchema):
    """No se lista suelta: se llega por el detalle del observable o por
    el del tipo de pregunta. De ahí los dos filtros."""
    model = ObservableQuestionType
    level = "category_subtype"
    filterset_fields = ['observable', 'question_type']
    serializer_class = ObservableQuestionTypeSerializer
    extra_mixins = [NoDeleteMixin]
    cat_params = {"hide_create": True}


@catalog_registry.register
class GeneralQuestionSchema(CatalogSchema):
    model = GeneralQuestion
    level = "category_subtype"
    name = "Pregunta del grupo"
    plural_name = "Preguntas del grupo"
    filterset_fields = ['general_group']
    serializer_class = GeneralQuestionCatalogSerializer
    # La FK de GeneralQuestionResponse es PROTECT: borrar no es opción.
    extra_mixins = [NoDeleteMixin]
    cat_params = {"hide_create": True}


@catalog_registry.register
class AQuestionSchema(ObservableQuestionSchema):
    model = AQuestion
    icon = "gavel"
    color = "indigo"
    serializer_class = AQuestionCatalogSerializer


@catalog_registry.register
class BQuestionSchema(ObservableQuestionSchema):
    model = BQuestion
    icon = "account_tree"
    color = "indigo"
    serializer_class = BQuestionCatalogSerializer


@catalog_registry.register
class ReachQuestionSchema(ObservableQuestionSchema):
    model = ReachQuestion
    icon = "groups"
    color = "indigo"
    serializer_class = ReachQuestionCatalogSerializer


@catalog_registry.register
class PlanQuestionSchema(ObservableQuestionSchema):
    model = PlanQuestion
    plural_name = "Preguntas de planes de estudio"
    icon = "menu_book"
    color = "deep-purple"
    serializer_class = PlanQuestionCatalogSerializer


@catalog_registry.register
class SpecialQuestionSchema(ObservableQuestionSchema):
    model = SpecialQuestion
    icon = "star"
    color = "deep-purple"
    serializer_class = SpecialQuestionCatalogSerializer


@catalog_registry.register_filter_group
class AOptionsFilterGroup(FilterGroupSchema):
    key_name = "a_options"
    name = "Opción de respuesta de armonización e institucionalización"
    plural_name = (
        "Opciones de respuesta de armonización e institucionalización")
    category_subtype = AOption
