"""
Serializers de la captura del cuestionario principal (flujo `cp`).

Lectura: el eje (`AxisValue`) trae sus observables en orden, cada uno
con su `ObservableResponse` (booleano inicial + status), sus
`GroupResponse` por tipo con las respuestas tipadas ya guardadas, y el
instrumento (preguntas A/B/Reach/Plan/Special del observable) para que
el frontend no cruce catálogos. Las preguntas viajan con serializers de
solo lectura propios: los del catálogo (`api/views/question`) son
escritores bajo la compuerta del cuestionario y consultan el interruptor
en cada instanciación, un costo inútil en 41 observables.

Escritura: `ObservableResponse.value` (dominio en `answer.services`) y
las respuestas tipadas de un `GroupResponse` completo, por upsert sobre
`(group_response, question)`.
"""
from django.core.validators import MinValueValidator
from rest_framework import serializers

from answer.models import (
    AResponse, BResponse, GroupResponse, ObservableResponse, PlanResponse,
    ReachResponse, SpecialResponse)
from flow.serializers import AttachmentSerializer, FlowEventSerializer
from indicator.models import Axis, Observable, Sector
from question.models import (
    AOption, AQuestion, BQuestion, PlanQuestion, ReachQuestion,
    SpecialQuestion)
from survey.models import AxisValue


# ---------------------------------------------------------------------------
# Instrumento (solo lectura)
# ---------------------------------------------------------------------------

class AOptionReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = AOption
        fields = ['id', 'text', 'value']


class SectorReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = ['id', 'name', 'description', 'needs_name', 'order']


class AQuestionReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = AQuestion
        fields = ['id', 'text', 'order']


class BQuestionReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = BQuestion
        fields = ['id', 'text', 'order', 'includes_academic',
                  'includes_admin']


class ReachQuestionReadSerializer(serializers.ModelSerializer):
    """`sectors` es la lista efectiva de poblaciones a marcar: las
    principales (si `has_main_sectors`) más las propias, en su orden."""
    sectors = serializers.SerializerMethodField()

    class Meta:
        model = ReachQuestion
        fields = ['id', 'text', 'has_main_sectors', 'has_general_planning',
                  'sectors']

    def get_sectors(self, obj: ReachQuestion) -> list:
        rows = list(obj.others_sectors.all())
        if obj.has_main_sectors:
            rows = list(self.context['main_sectors']) + rows
        rows.sort(key=lambda s: (s.order, s.id))
        return SectorReadSerializer(rows, many=True).data


class PlanQuestionReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanQuestion
        fields = ['id', 'text', 'order']


class SpecialQuestionReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialQuestion
        fields = ['id', 'text']


class ObservableReadSerializer(serializers.ModelSerializer):
    component_name = serializers.CharField(
        source='component.name', read_only=True)
    a_questions = AQuestionReadSerializer(
        many=True, read_only=True, source='aquestion_set')
    b_questions = BQuestionReadSerializer(
        many=True, read_only=True, source='bquestion_set')
    reach_questions = ReachQuestionReadSerializer(
        many=True, read_only=True, source='reachquestion_set')
    plan_questions = PlanQuestionReadSerializer(
        many=True, read_only=True, source='planquestion_set')
    special_questions = SpecialQuestionReadSerializer(
        many=True, read_only=True, source='specialquestion_set')

    class Meta:
        model = Observable
        fields = ['id', 'number', 'order', 'name', 'description',
                  'init_question', 'a_main_question', 'a_main_subtitle',
                  'note', 'component', 'component_name', 'a_questions',
                  'b_questions', 'reach_questions', 'plan_questions',
                  'special_questions']


# ---------------------------------------------------------------------------
# Respuestas tipadas (lectura y escritura anidada)
# ---------------------------------------------------------------------------

class AResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AResponse
        fields = ['id', 'question', 'selected_option']


class BResponseSerializer(serializers.ModelSerializer):
    academic_instances_complying = serializers.IntegerField(
        required=False, allow_null=True,
        validators=[MinValueValidator(0)])
    admin_instances_complying = serializers.IntegerField(
        required=False, allow_null=True,
        validators=[MinValueValidator(0)])

    class Meta:
        model = BResponse
        fields = ['id', 'question', 'academic_instances_complying',
                  'admin_instances_complying']


class ReachResponseSerializer(serializers.ModelSerializer):
    sectors = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Sector.objects.all(), required=False)

    class Meta:
        model = ReachResponse
        fields = ['id', 'question', 'not_focalized', 'sectors']

    def validate(self, attrs: dict) -> dict:
        question = attrs.get('question')
        if (attrs.get('not_focalized') and question is not None
                and not question.has_general_planning):
            raise serializers.ValidationError({
                'not_focalized': 'Esta pregunta no ofrece la opción de '
                                 'planeación general.'})
        return attrs


class PlanResponseSerializer(serializers.ModelSerializer):
    media_plans = serializers.IntegerField(
        required=False, allow_null=True,
        validators=[MinValueValidator(0)])
    superior_plans = serializers.IntegerField(
        required=False, allow_null=True,
        validators=[MinValueValidator(0)])
    postgraduate_plans = serializers.IntegerField(
        required=False, allow_null=True,
        validators=[MinValueValidator(0)])

    class Meta:
        model = PlanResponse
        fields = ['id', 'question', 'media_plans', 'superior_plans',
                  'postgraduate_plans']


class SpecialResponseSerializer(serializers.ModelSerializer):
    total = serializers.IntegerField(
        required=False, allow_null=True,
        validators=[MinValueValidator(0)])
    complying = serializers.IntegerField(
        required=False, allow_null=True,
        validators=[MinValueValidator(0)])

    class Meta:
        model = SpecialResponse
        fields = ['id', 'question', 'total', 'complying']


# (clave del payload, serializer, tipo de pregunta al que pertenece)
TYPED_RESPONSES = (
    ('a_responses', AResponseSerializer, 'a_questions'),
    ('b_responses', BResponseSerializer, 'b_questions'),
    ('reach_responses', ReachResponseSerializer, 'reach'),
    ('plan_responses', PlanResponseSerializer, 'plans'),
    ('special_responses', SpecialResponseSerializer, 'special'),
)


class GroupResponseSerializer(serializers.ModelSerializer):
    """Grupo por tipo con sus respuestas tipadas. Las cinco listas
    viajan siempre (vacías en los tipos que no aplican) para que el
    payload sea uniforme.

    En escritura solo se acepta la lista del tipo del grupo, y cada
    pregunta debe pertenecer al observable del grupo: así una fila no
    puede colgarse del grupo equivocado.
    """
    a_responses = AResponseSerializer(many=True, required=False)
    b_responses = BResponseSerializer(many=True, required=False)
    reach_responses = ReachResponseSerializer(many=True, required=False)
    plan_responses = PlanResponseSerializer(many=True, required=False)
    special_responses = SpecialResponseSerializer(many=True, required=False)

    class Meta:
        model = GroupResponse
        fields = ['id', 'observable_response', 'question_type', 'status',
                  'a_responses', 'b_responses', 'reach_responses',
                  'plan_responses', 'special_responses']
        read_only_fields = ['observable_response', 'question_type',
                            'status']

    def validate(self, attrs: dict) -> dict:
        group: GroupResponse = self.instance
        observable_id = group.observable_response.observable_id
        for key, _, type_name in TYPED_RESPONSES:
            rows = attrs.get(key)
            if rows is None:
                continue
            if type_name != group.question_type_id:
                raise serializers.ValidationError({
                    key: f'Este grupo es de tipo «{group.question_type_id}»; '
                         f'no admite {key}.'})
            questions = [row['question'] for row in rows]
            if len(questions) != len({q.pk for q in questions}):
                raise serializers.ValidationError({
                    key: 'Hay preguntas repetidas en la lista.'})
            foreign = [q for q in questions
                       if q.observable_id != observable_id]
            if foreign:
                raise serializers.ValidationError({
                    key: 'Una de las preguntas no pertenece a este '
                         'observable.'})
        return attrs

    def update(self, instance: GroupResponse, validated_data: dict):
        for key, _, _ in TYPED_RESPONSES:
            rows = validated_data.pop(key, None)
            if rows is not None:
                self._sync_rows(instance, key, rows)
        return instance

    @staticmethod
    def _sync_rows(group: GroupResponse, key: str, rows: list) -> None:
        """Upsert por (grupo, pregunta); nunca borra por omisión: la IES
        captura en varias sesiones."""
        manager = getattr(group, key)
        for row in rows:
            sectors = row.pop('sectors', None)
            data = {k: v for k, v in row.items()
                    if k not in ('id', 'question')}
            obj, _ = manager.update_or_create(
                question=row['question'], defaults=data)
            if sectors is not None:
                obj.sectors.set(sectors)


class GroupResponseFullSerializer(GroupResponseSerializer):
    flow_events = FlowEventSerializer(many=True, read_only=True)
    flow_attachments = AttachmentSerializer(many=True, read_only=True)

    class Meta(GroupResponseSerializer.Meta):
        fields = GroupResponseSerializer.Meta.fields + [
            'value', 'flow_events', 'flow_attachments']
        read_only_fields = GroupResponseSerializer.Meta.read_only_fields + [
            'value']


class ObservableResponseSerializer(serializers.ModelSerializer):
    """Escritura del booleano inicial: solo `value` es editable, y su
    efecto sobre el flujo lo aplica la vista vía `answer.services`."""

    class Meta:
        model = ObservableResponse
        fields = ['id', 'survey', 'observable', 'axis_value', 'status',
                  'value']
        read_only_fields = ['survey', 'observable', 'axis_value', 'status']


class ObservableResponseFullSerializer(ObservableResponseSerializer):
    observable_full = ObservableReadSerializer(
        read_only=True, source='observable')
    group_responses = GroupResponseFullSerializer(
        many=True, read_only=True, source='statuses')
    flow_events = FlowEventSerializer(many=True, read_only=True)

    class Meta(ObservableResponseSerializer.Meta):
        fields = ObservableResponseSerializer.Meta.fields + [
            'observable_full', 'group_responses', 'flow_events']


# ---------------------------------------------------------------------------
# Eje
# ---------------------------------------------------------------------------

class AxisReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Axis
        fields = ['id', 'order', 'name', 'short_name', 'slug', 'icon',
                  'color', 'hex_color', 'description']


def count_by_status(rows) -> dict:
    """{status: cuántos} sobre hijos ya prefetcheados."""
    result: dict = {}
    for row in rows:
        result[row.status_id] = result.get(row.status_id, 0) + 1
    return result


class AxisValueSerializer(serializers.ModelSerializer):
    """Lista: eje + institución/periodo resumidos + conteo de observables
    por status (para el encabezado y los íconos)."""
    axis_full = AxisReadSerializer(read_only=True, source='axis')
    institution = serializers.IntegerField(
        source='survey.institution_id', read_only=True)
    institution_acronym = serializers.CharField(
        source='survey.institution.acronym', read_only=True)
    period = serializers.IntegerField(
        source='survey.period_id', read_only=True)
    observables_by_status = serializers.SerializerMethodField()

    class Meta:
        model = AxisValue
        fields = ['id', 'survey', 'axis', 'status', 'axis_full',
                  'institution', 'institution_acronym', 'period',
                  'observables_by_status']

    def get_observables_by_status(self, obj: AxisValue) -> dict:
        return count_by_status(obj.observable_responses.all())


GEN_DENOMINATORS = ('academic_instances', 'admin_instances', 'media_plans',
                    'superior_plans', 'postgraduate_plans')


class AxisValueFullSerializer(AxisValueSerializer):
    """Detalle: el cuestionario del eje con respuestas, más lo que la
    captura necesita a mano: las opciones A globales, los denominadores
    declarados en información base y el estado de la compuerta."""
    observable_responses = ObservableResponseFullSerializer(
        many=True, read_only=True)
    flow_events = FlowEventSerializer(many=True, read_only=True)
    a_options = serializers.SerializerMethodField()
    gen_denominators = serializers.SerializerMethodField()
    cp_capture = serializers.SerializerMethodField()

    class Meta(AxisValueSerializer.Meta):
        fields = AxisValueSerializer.Meta.fields + [
            'value', 'observable_responses', 'flow_events', 'a_options',
            'gen_denominators', 'cp_capture']

    def get_a_options(self, obj) -> list:
        return AOptionReadSerializer(
            AOption.objects.order_by('-value'), many=True).data

    def get_gen_denominators(self, obj: AxisValue) -> dict:
        """{name: {value, no_apply}} de las preguntas generales que
        acotan los conteos de B y de planes; null cuando no hay fila."""
        rows = {
            row.general_question.name: {
                'value': row.value_integer, 'no_apply': row.no_apply}
            for row in obj.survey.question_responses.all()
            if row.general_question.name in GEN_DENOMINATORS
        }
        return {name: rows.get(name) for name in GEN_DENOMINATORS}

    def get_cp_capture(self, obj: AxisValue) -> dict:
        from survey.cp_gate import capture_state
        return capture_state(obj.survey)
