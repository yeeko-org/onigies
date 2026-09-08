from rest_framework import serializers

from question.models import (
    AOption, AQuestion, BQuestion, GeneralQuestion, ObservableQuestionType,
    PlanQuestion, QuestionType, ReachQuestion, SpecialQuestion)


class AOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AOption
        fields = '__all__'


class QuestionTypeCatalogSerializer(serializers.ModelSerializer):
    observables_count = serializers.IntegerField(
        read_only=True)

    class Meta:
        model = QuestionType
        fields = '__all__'
        # Claves que el código busca y amarres a los modelos de captura:
        # viajan para leerse, nunca para escribirse.
        read_only_fields = [
            'name', 'model_question', 'model_response', 'required']


class ObservableQuestionTypeSerializer(serializers.ModelSerializer):
    """Solo `weight` se escribe: qué tipos aplican a un observable lo
    fija la siembra. `final_weight` es la propia si existe, si no la del
    tipo."""
    final_weight = serializers.DecimalField(
        max_digits=5, decimal_places=2, read_only=True)
    public_name = serializers.CharField(
        source='question_type.public_name', read_only=True)

    class Meta:
        model = ObservableQuestionType
        fields = [
            'id', 'observable', 'question_type', 'weight', 'final_weight',
            'public_name']
        read_only_fields = ['observable', 'question_type']


class ObservableQuestionSerializer(serializers.ModelSerializer):
    """`order` no se edita porque forma con `observable` la clave
    natural del seed: cambiarlo haría que `load_questionnaire` duplique
    la fila en vez de actualizarla."""

    class Meta:
        fields = '__all__'
        read_only_fields = ['observable', 'order']


class AQuestionCatalogSerializer(ObservableQuestionSerializer):
    class Meta(ObservableQuestionSerializer.Meta):
        model = AQuestion


class BQuestionCatalogSerializer(ObservableQuestionSerializer):
    class Meta(ObservableQuestionSerializer.Meta):
        model = BQuestion
        read_only_fields = ObservableQuestionSerializer.Meta.read_only_fields \
            + ['includes_academic', 'includes_admin']


class ReachQuestionCatalogSerializer(ObservableQuestionSerializer):
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
    class Meta:
        model = GeneralQuestion
        fields = '__all__'
        # `name` mapea la columna del Survey donde aterriza la respuesta;
        # `q_type` / `addl_config` anclan comportamiento que vive en código.
        read_only_fields = ['name', 'q_type', 'addl_config']
