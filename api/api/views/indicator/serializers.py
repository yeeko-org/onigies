from functools import cached_property

from django.db.models import Count
from rest_framework import serializers

from indicator.models import Axis, Component, GeneralGroup, Observable, Sector
from api.views.question.serializers import (
    AQuestionCatalogSerializer, BQuestionCatalogSerializer,
    GeneralQuestionCatalogSerializer, ObservableQuestionTypeSerializer,
    PlanQuestionCatalogSerializer, ReachQuestionCatalogSerializer,
    SpecialQuestionCatalogSerializer)


class ObservableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observable
        fields = '__all__'


class WeightFlagsMixin(metaclass=serializers.SerializerMetaclass):
    """Avisos del editor: ninguna de las dos bloquea el guardado."""
    uses_default_weights = serializers.BooleanField(read_only=True)
    weights_pending = serializers.BooleanField(read_only=True)


class ObservableFullSerializer(WeightFlagsMixin, serializers.ModelSerializer):
    """Los alias en plural son lo que el Sheet genérico busca para listar
    cada colección hija sin un fetch extra."""
    observable_question_types = ObservableQuestionTypeSerializer(
        many=True, read_only=True, source='type_weights')
    a_questions = AQuestionCatalogSerializer(
        many=True, read_only=True, source='aquestion_set')
    b_questions = BQuestionCatalogSerializer(
        many=True, read_only=True, source='bquestion_set')
    reach_questions = ReachQuestionCatalogSerializer(
        many=True, read_only=True, source='reachquestion_set')
    plan_questions = PlanQuestionCatalogSerializer(
        many=True, read_only=True, source='planquestion_set')
    special_questions = SpecialQuestionCatalogSerializer(
        many=True, read_only=True, source='specialquestion_set')

    class Meta:
        model = Observable
        fields = '__all__'
        read_only_fields = ['component', 'number', 'order']


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = '__all__'


class ObservableCountsSerializer(WeightFlagsMixin, ObservableSerializer):
    """Los conteos vienen anotados en el queryset y se declaran a mano
    porque un serializer escrito no los inyecta como el auto-generado."""
    a_questions_count = serializers.IntegerField(read_only=True)
    b_questions_count = serializers.IntegerField(read_only=True)
    reach_questions_count = serializers.IntegerField(read_only=True)
    plan_questions_count = serializers.IntegerField(read_only=True)
    special_questions_count = serializers.IntegerField(read_only=True)
    question_types = serializers.SlugRelatedField(
        source='type_weights', slug_field='question_type_id',
        many=True, read_only=True)
    reach_sectors_count = serializers.SerializerMethodField()
    # Hay a lo más una BQuestion por observable: las banderas suben
    # planas en vez de anidar la pregunta entera.
    b_includes_academic = serializers.SerializerMethodField()
    b_includes_admin = serializers.SerializerMethodField()

    def _b_question(self, obj: Observable):
        return next(iter(obj.bquestion_set.all()), None)

    def get_b_includes_academic(self, obj: Observable) -> bool:
        b_question = self._b_question(obj)
        return bool(b_question and b_question.includes_academic)

    def get_b_includes_admin(self, obj: Observable) -> bool:
        b_question = self._b_question(obj)
        return bool(b_question and b_question.includes_admin)

    @cached_property
    def _main_sectors_count(self) -> int:
        # `many=True` reusa una sola instancia hija para toda la lista:
        # el cache la resuelve en una consulta por request.
        return Sector.objects.filter(is_main=True).count()

    def get_reach_sectors_count(self, obj: Observable) -> int:
        """Los sectores propios más el bloque principal si lo incluye."""
        reach = next(iter(obj.reachquestion_set.all()), None)
        if reach is None:
            return 0
        total = len(reach.others_sectors.all())
        if reach.has_main_sectors:
            total += self._main_sectors_count
        return total


class ComponentFullSerializer(serializers.ModelSerializer):
    observables = serializers.SerializerMethodField()

    def get_observables(self, obj: Component) -> list:
        # El import vive aquí porque indicator.catalog_schema importa
        # este módulo: a nivel de módulo sería un ciclo.
        from indicator.catalog_schema import (
            OBSERVABLE_COUNT_FIELDS, TYPE_WEIGHTS_PREFETCH)

        queryset = obj.observables.annotate(**{
            name: Count(path, distinct=True)
            for name, path in OBSERVABLE_COUNT_FIELDS.items()
        }).prefetch_related(
            TYPE_WEIGHTS_PREFETCH, 'reachquestion_set__others_sectors',
            'bquestion_set')
        return ObservableCountsSerializer(queryset, many=True).data

    class Meta:
        model = Component
        fields = '__all__'


class AxisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Axis
        fields = '__all__'


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = '__all__'


class GeneralGroupCatalogSerializer(serializers.ModelSerializer):
    """El alias `general_questions` (el accessor es `questions`) es lo
    que el Sheet genérico busca para listar la colección hija."""
    general_questions = GeneralQuestionCatalogSerializer(
        many=True, read_only=True, source='questions')

    class Meta:
        model = GeneralGroup
        fields = '__all__'
        read_only_fields = ['name']
