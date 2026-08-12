"""
Serializers del flujo `gen` (preguntas generales): GeneralPackage y sus
GeneralGroupResponse.

Espejo de los de GoodPracticePackage (`api/api/views/example/serializers.py`):
un serializer de lista (paquete + survey resumido + conteo de grupos) y
un Full que anida los hijos con su `status` y sus `flow_events`.

El contenido de las respuestas NO vive aquí: se escribe contra `Survey`
(columnas escalares y `population_quantities`). Estos
wrappers solo llevan flujo, por eso son de solo lectura.
"""
from rest_framework import serializers

from indicator.models import GeneralGroup
from question.models import GeneralQuestion
from survey.models import GeneralPackage, GeneralGroupResponse
from api.views.example.serializers import SurveySemiFullSerializer
from flow.serializers import AttachmentSerializer, FlowEventSerializer


class GeneralQuestionSerializer(serializers.ModelSerializer):
    """Pregunta del grupo. `effective_label` resuelve el rótulo que se
    pinta (el propio o, si va vacío, la unidad) para que el front no
    repita la regla; `label` sigue expuesto crudo porque es el que se
    edita desde el catálogo.
    """
    effective_label = serializers.CharField(read_only=True)

    class Meta:
        model = GeneralQuestion
        fields = ['id', 'name', 'text', 'hint', 'label', 'effective_label',
                  'unit', 'q_type', 'order', 'addl_config']


class GeneralGroupSerializer(serializers.ModelSerializer):
    """Catálogo del grupo, embebido para que el front pinte el grupo
    sin un fetch adicional. `name` es la PK (el código: `estructuras`,
    `poblaciones`, …), `questions` las preguntas en su orden y `order`
    el lugar que ocupa en el instrumento.
    """
    questions = GeneralQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = GeneralGroup
        fields = ['name', 'public_name', 'title', 'subtitle', 'instruction',
                  'is_population', 'order', 'questions']


class GeneralGroupResponseSerializer(serializers.ModelSerializer):
    """Wrapper de flujo por (survey, grupo), con el catálogo embebido."""
    general_group_full = GeneralGroupSerializer(
        read_only=True, source='general_group')

    class Meta:
        model = GeneralGroupResponse
        fields = '__all__'


class GeneralGroupResponseFullSerializer(GeneralGroupResponseSerializer):
    flow_events = FlowEventSerializer(many=True, read_only=True)
    # La evidencia probatoria de la sección se ancla al grupo, no al
    # Survey: cada grupo lleva la suya y la revisión la ve en su panel.
    flow_attachments = AttachmentSerializer(many=True, read_only=True)


def count_groups_by_status(package: GeneralPackage) -> dict:
    """{nombre_de_status: cuántos grupos} — resumen del avance.

    Cuenta en Python sobre los hijos ya prefetcheados: con un `annotate`
    haría un query por paquete y el conjunto es de 5 filas.
    """
    result: dict = {}
    for response in package.general_group_responses.all():
        key = response.status_id
        result[key] = result.get(key, 0) + 1
    return result


class GeneralPackageBriefSerializer(serializers.ModelSerializer):
    """Resumen del paquete para anidar en la lista de Survey: lo justo
    para el renglón colapsado (chip de status + avance), sin los grupos
    ni el timeline.
    """
    groups_by_status = serializers.SerializerMethodField()

    class Meta:
        model = GeneralPackage
        fields = ['id', 'status', 'sent_at', 'groups_by_status']

    def get_groups_by_status(self, obj) -> dict:
        return count_groups_by_status(obj)


class GeneralPackageSerializer(serializers.ModelSerializer):
    """Lista: paquete + survey resumido (institución y periodo) + un
    resumen de los grupos que cuelgan de él.
    """
    survey_full = SurveySemiFullSerializer(read_only=True, source='survey')
    general_group_responses_count = serializers.SerializerMethodField()
    groups_by_status = serializers.SerializerMethodField()

    class Meta:
        model = GeneralPackage
        fields = '__all__'

    def get_general_group_responses_count(self, obj) -> int:
        return len(obj.general_group_responses.all())

    def get_groups_by_status(self, obj) -> dict:
        return count_groups_by_status(obj)


class GeneralPackageFullSerializer(GeneralPackageSerializer):
    general_group_responses = GeneralGroupResponseFullSerializer(
        many=True, read_only=True)
    flow_events = FlowEventSerializer(many=True, read_only=True)
