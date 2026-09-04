from rest_framework import serializers

from indicator.models import Axis, Component, GeneralGroup, Observable, Sector
from api.views.question.serializers import (
    AQuestionCatalogSerializer, BQuestionCatalogSerializer,
    GeneralQuestionCatalogSerializer, PlanQuestionCatalogSerializer,
    ReachQuestionCatalogSerializer, SpecialQuestionCatalogSerializer)


class ObservableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observable
        fields = '__all__'


class ObservableFullSerializer(serializers.ModelSerializer):
    """Observable con sus cinco familias de preguntas anidadas.

    Los alias en plural (`a_questions`, `b_questions`, …) son lo que el
    Sheet genérico busca para listar cada colección hija sin un fetch
    extra; los accessors del modelo son los `*_set` por defecto.

    Editable solo el texto del instrumento. `number` y `order` numeran
    el cuestionario y `component` lo cuelga de su rama: los mueve el
    seed. Las ponderaciones son metodología, no redacción.
    """
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
        read_only_fields = [
            'component', 'number', 'order',
            'a_weight', 'b_weight', 'reach_weight', 'plan_weight',
            'special_weight', 'pop_weight',
        ]


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = '__all__'


class ComponentFullSerializer(serializers.ModelSerializer):
    observables = ObservableSerializer(many=True, read_only=True)
    # observables_count = serializers.SerializerMethodField()
    #
    # def get_observables_count(self, obj: Component):
    #     return obj.observables.count()

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
    """Grupo de preguntas base con sus preguntas anidadas.

    El alias `general_questions` (el accessor del modelo es `questions`)
    es lo que el Sheet genérico busca para listar la colección hija sin
    un fetch extra. `name` es la PK y la clave del código: solo lectura.
    """
    general_questions = GeneralQuestionCatalogSerializer(
        many=True, read_only=True, source='questions')

    class Meta:
        model = GeneralGroup
        fields = '__all__'
        read_only_fields = ['name']






