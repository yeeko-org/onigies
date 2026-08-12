"""
Serializers de Survey — el contenedor donde vive el contenido de las
preguntas generales (grupo de flujo `gen`).

Las respuestas se escriben SIEMPRE contra el Survey, no contra el grupo:
las escalares son columnas propias y las poblaciones/autoridades son
filas de `PopulationQuantity`, donde también vive su existencia
(`is_present`, adr-0012).
Los `GeneralGroupResponse` solo llevan flujo (ver `general_serializers`).
"""
from rest_framework import serializers

from survey.models import (
    Survey, PopulationQuantity, GeneralQuestionResponse)
from api.views.ies.serializers import (
    InstitutionSimpleSerializer, PeriodSimpleSerializer)
from api.views.survey.general_serializers import (
    GeneralPackageBriefSerializer, GeneralPackageFullSerializer)


class PopulationQuantitySerializer(serializers.ModelSerializer):
    """Fila de población por sector, anidada en el Survey.

    `survey` no se declara: lo fija el padre en la sincronización, y
    aceptarlo abriría la puerta a escribir en el survey de otra IES.
    """

    class Meta:
        model = PopulationQuantity
        fields = [
            'id', 'sector', 'no_apply', 'name', 'is_present',
            'number_women', 'number_men', 'number_non_binary']


class GeneralQuestionResponseSerializer(serializers.ModelSerializer):
    """Metadatos de la respuesta a una pregunta general, anidados en el
    Survey. Hoy solo el «No aplica»; el valor sigue viviendo en la
    columna del Survey que nombra la pregunta.

    `survey` no se declara, por lo mismo que en las poblaciones: lo fija
    el padre en la sincronización.
    """

    class Meta:
        model = GeneralQuestionResponse
        fields = ['id', 'general_question', 'no_apply']


class SurveySerializer(serializers.ModelSerializer):
    """Escritura y lectura del contenido de las generales.

    `population_quantities` y `question_responses` se sincronizan por
    upsert: las filas que llegan se crean o actualizan y las ausentes se
    quedan como están — una fila contestada sin conteos debe sobrevivir
    (adr-0012).
    """
    population_quantities = PopulationQuantitySerializer(
        many=True, required=False)
    question_responses = GeneralQuestionResponseSerializer(
        many=True, required=False)
    # Contrato heredado: el frontend lee `sectors` como lista de ids.
    # Ahora es derivado y de solo lectura (adr-0012).
    sectors = serializers.ReadOnlyField()

    class Meta:
        model = Survey
        # `sectors_legacy` no se expone: es la fuente histórica que ya no
        # se escribe (adr-0012) y con `__all__` viajaba como M2M editable,
        # o sea una segunda forma de declarar presencia que contradice a
        # `is_present`.
        exclude = ['sectors_legacy']
        read_only_fields = ('institution', 'period')

    def validate_population_quantities(self, value: list) -> list:
        sectors = [row['sector'] for row in value]
        if len(sectors) != len(set(sectors)):
            raise serializers.ValidationError(
                'Hay sectores repetidos en la lista de poblaciones.')
        return value

    def validate_question_responses(self, value: list) -> list:
        questions = [row['general_question'] for row in value]
        if len(questions) != len(set(questions)):
            raise serializers.ValidationError(
                'Hay preguntas repetidas en la lista de respuestas.')
        return value

    def update(self, instance: Survey, validated_data: dict) -> Survey:
        rows = validated_data.pop('population_quantities', None)
        responses = validated_data.pop('question_responses', None)
        survey = super().update(instance, validated_data)
        if rows is not None:
            self._sync_population_quantities(survey, rows)
        if responses is not None:
            self._sync_question_responses(survey, responses)
        self._clear_non_binary(survey, validated_data)
        return survey

    def create(self, validated_data: dict) -> Survey:
        rows = validated_data.pop('population_quantities', None)
        responses = validated_data.pop('question_responses', None)
        survey = super().create(validated_data)
        if rows is not None:
            self._sync_population_quantities(survey, rows)
        if responses is not None:
            self._sync_question_responses(survey, responses)
        self._clear_non_binary(survey, validated_data)
        return survey

    @staticmethod
    def _sync_population_quantities(survey: Survey, rows: list) -> None:
        """Crea o actualiza las filas que llegan; nunca borra por
        omisión (una fila contestada sin conteos debe sobrevivir)."""
        for row in rows:
            data = {k: v for k, v in row.items() if k not in ('id', 'sector')}
            # Una población ausente o no aplicable no puede quedarse con
            # conteos viejos: se limpian del lado del servidor.
            if data.get('is_present') is False or data.get('no_apply'):
                data.update(
                    number_women=None, number_men=None,
                    number_non_binary=None)
            PopulationQuantity.objects.update_or_create(
                survey=survey, sector=row['sector'], defaults=data)

    @staticmethod
    def _sync_question_responses(survey: Survey, rows: list) -> None:
        """Upsert de los metadatos por pregunta; nunca borra por omisión.

        `name` es el contrato: nombra la columna del Survey donde
        aterriza el valor, así que un «No aplica» la deja en nulo — no
        puede quedarse un dato viejo bajo una respuesta que ya dice que
        no aplica. Se resuelve contra los campos reales del modelo
        porque hay `name` que no son columna (las preguntas de captura
        derivada) y porque `sectors` o `is_test` son propiedades.
        """
        columns = {
            field.name for field in Survey._meta.get_fields()
            if getattr(field, 'concrete', False)}
        to_clear = {}
        for row in rows:
            question = row['general_question']
            no_apply = row.get('no_apply', False)
            GeneralQuestionResponse.objects.update_or_create(
                survey=survey, general_question=question,
                defaults={'no_apply': no_apply})
            if no_apply and question.name in columns:
                to_clear[question.name] = None
        if not to_clear:
            return
        for column, value in to_clear.items():
            setattr(survey, column, value)
        survey.save(update_fields=list(to_clear))

    @staticmethod
    def _clear_non_binary(survey: Survey, validated_data: dict) -> None:
        """Apagar la pregunta previa borra los conteos no binarios ya
        capturados. Solo un `false` explícito limpia (mismo criterio que
        `is_present`): el nulo es «sin contestar», no un «no».
        Corre después del upsert para ganarle a los conteos que hayan
        llegado en el mismo request.
        """
        if validated_data.get('measures_non_binary') is not False:
            return
        survey.population_quantities.update(number_non_binary=None)


class SurveyListSerializer(SurveySerializer):
    """Lista del dashboard: institución, periodo y el paquete de
    generales resumido (status y avance del renglón colapsado)."""
    institution_full = InstitutionSimpleSerializer(
        read_only=True, source='institution')
    period_full = PeriodSimpleSerializer(read_only=True, source='period')
    general_package = GeneralPackageBriefSerializer(read_only=True)


class SurveyFullSerializer(SurveyListSerializer):
    """Detalle: agrega el paquete de generales con sus grupos y flujo."""
    general_package = GeneralPackageFullSerializer(read_only=True)
