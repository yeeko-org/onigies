from rest_framework import serializers

from indicator.models import Axis, Component, GeneralGroup, Observable, Sector
from api.views.question.serializers import GeneralQuestionCatalogSerializer



class ObservableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observable
        fields = '__all__'


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






