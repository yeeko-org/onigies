from rest_framework import serializers

from question.models import (
    AOption, AQuestion, BQuestion, GeneralQuestion, PlanQuestion,
    ReachQuestion, SpecialQuestion)


class AOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AOption
        fields = '__all__'


class ObservableQuestionSerializer(serializers.ModelSerializer):
    """Base de las preguntas por observable como catálogo del dashboard.

    El equipo del observatorio corrige redacción; la estructura del
    instrumento (a qué observable cuelga, en qué orden se re-siembra,
    qué banderas de comportamiento lleva) no se toca desde aquí. Cada
    subclase declara su modelo y agrega a `read_only_fields` lo suyo.

    `order` es de solo lectura porque en AQuestion, BQuestion y
    PlanQuestion forma con `observable` la clave natural del seed:
    cambiarlo haría que `load_questionnaire` duplique la fila en vez de
    actualizarla.
    """

    class Meta:
        fields = '__all__'
        read_only_fields = ['observable', 'order']


class AQuestionCatalogSerializer(ObservableQuestionSerializer):
    class Meta(ObservableQuestionSerializer.Meta):
        model = AQuestion


class BQuestionCatalogSerializer(ObservableQuestionSerializer):
    """`includes_academic` / `includes_admin` deciden qué tablas de
    captura se pintan: son estructura, no texto."""

    class Meta(ObservableQuestionSerializer.Meta):
        model = BQuestion
        read_only_fields = ObservableQuestionSerializer.Meta.read_only_fields \
            + ['includes_academic', 'includes_admin']


class ReachQuestionCatalogSerializer(ObservableQuestionSerializer):
    """Las banderas de sectores arman el checklist de población."""

    class Meta(ObservableQuestionSerializer.Meta):
        model = ReachQuestion
        read_only_fields = ObservableQuestionSerializer.Meta.read_only_fields \
            + ['has_main_sectors', 'others_sectors', 'has_general_planning']


class PlanQuestionCatalogSerializer(ObservableQuestionSerializer):
    class Meta(ObservableQuestionSerializer.Meta):
        model = PlanQuestion


class SpecialQuestionCatalogSerializer(ObservableQuestionSerializer):
    class Meta(ObservableQuestionSerializer.Meta):
        model = SpecialQuestion


class GeneralQuestionCatalogSerializer(serializers.ModelSerializer):
    """Pregunta base como catálogo editable del dashboard.

    `name` mapea la columna del Survey donde aterriza la respuesta y
    `addl_config` / `q_type` anclan comportamiento que vive en código:
    viajan para poder leerlos, nunca para escribirlos.
    """
    class Meta:
        model = GeneralQuestion
        fields = '__all__'
        read_only_fields = ['name', 'q_type', 'addl_config']
