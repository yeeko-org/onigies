from django.db.models import Max
from rest_framework import serializers

from question.models import (
    AOption, AQuestion, BQuestion, GeneralQuestion, ObservableQuestionType,
    PlanQuestion, QuestionType, QuestionnaireSettings, ReachQuestion,
    SpecialQuestion)


class ContentGatedSerializer(serializers.ModelSerializer):
    """La liberación va en `get_extra_kwargs` y no sobre los campos ya
    construidos: un relacional de solo lectura nace sin `queryset` y
    apagarle la bandera después lo deja inservible para escribir."""

    open_fields: list = []
    # Clave natural: solo en el alta.
    open_create_fields: list = []

    def get_extra_kwargs(self) -> dict:
        extra_kwargs = super().get_extra_kwargs()
        if not QuestionnaireSettings.is_open():
            return extra_kwargs
        writable = list(self.open_fields)
        if self.instance is None:
            writable += self.open_create_fields
        for name in writable:
            kwargs = dict(extra_kwargs.get(name, {}))
            kwargs.pop('read_only', None)
            extra_kwargs[name] = kwargs
        return extra_kwargs


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


class ObservableQuestionTypeSerializer(ContentGatedSerializer):
    """Con el cuestionario cerrado solo `weight` se escribe: qué tipos
    aplican a un observable lo fija la siembra."""
    final_weight = serializers.DecimalField(
        max_digits=5, decimal_places=2, read_only=True)
    public_name = serializers.CharField(
        source='question_type.public_name', read_only=True)

    open_create_fields = ['observable', 'question_type']

    class Meta:
        model = ObservableQuestionType
        fields = [
            'id', 'observable', 'question_type', 'weight', 'final_weight',
            'public_name']
        read_only_fields = ['observable', 'question_type']


class ObservableQuestionSerializer(ContentGatedSerializer):
    """`order` no se edita nunca porque forma con `observable` la clave
    natural del seed: cambiarlo haría que `load_questionnaire` duplique
    la fila en vez de actualizarla."""

    open_create_fields = ['observable']

    class Meta:
        fields = '__all__'
        read_only_fields = ['observable', 'order']

    @property
    def _has_order(self) -> bool:
        return any(f.name == 'order' for f in self.Meta.model._meta.fields)

    def create(self, validated_data: dict):
        observable = validated_data['observable']
        if self._has_order:
            top = self.Meta.model.objects.filter(
                observable=observable).aggregate(top=Max('order'))['top']
            validated_data['order'] = (top or 0) + 1
        instance = super().create(validated_data)
        # Que una sola acción del dashboard baste: sin fila puente el
        # bloque no cuenta en el observable.
        ObservableQuestionType.objects.get_or_create(
            observable=observable,
            question_type=QuestionType.for_model(self.Meta.model))
        return instance


class AQuestionCatalogSerializer(ObservableQuestionSerializer):
    class Meta(ObservableQuestionSerializer.Meta):
        model = AQuestion


class BQuestionCatalogSerializer(ObservableQuestionSerializer):
    open_fields = ['includes_academic', 'includes_admin']

    class Meta(ObservableQuestionSerializer.Meta):
        model = BQuestion
        read_only_fields = ObservableQuestionSerializer.Meta.read_only_fields \
            + ['includes_academic', 'includes_admin']


class ReachQuestionCatalogSerializer(ObservableQuestionSerializer):
    open_fields = [
        'has_main_sectors', 'others_sectors', 'has_general_planning']

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


REOPEN_MESSAGE = (
    "El cuestionario ya se cerró: reabrirlo se hace desde el admin de "
    "Django.")


class QuestionnaireSettingsSerializer(serializers.ModelSerializer):
    """`title` existe porque el modelo no tiene `name` ni `title` y la
    fila saldría «SIN NOMBRE» en el dashboard."""
    title = serializers.SerializerMethodField()

    def get_title(self, obj: QuestionnaireSettings) -> str:
        return str(obj)

    def validate(self, attrs: dict) -> dict:
        # Cerrar es de ida: una vez congelado el instrumento, reabrirlo
        # deja de estar al alcance de quien edita desde el dashboard.
        if attrs.get('content_open') and self.instance \
                and not self.instance.content_open:
            raise serializers.ValidationError(
                {'content_open': REOPEN_MESSAGE})
        return attrs

    class Meta:
        model = QuestionnaireSettings
        fields = ['id', 'title', 'content_open', 'seeded_at']
        read_only_fields = ['seeded_at']


class GeneralQuestionCatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralQuestion
        fields = '__all__'
        # `name` mapea la columna del Survey donde aterriza la respuesta;
        # `q_type` / `addl_config` anclan comportamiento que vive en código.
        read_only_fields = ['name', 'q_type', 'addl_config']
