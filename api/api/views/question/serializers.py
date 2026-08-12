from rest_framework import serializers

from question.models import AOption, GeneralQuestion


class AOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AOption
        fields = '__all__'


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
