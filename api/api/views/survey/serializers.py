"""
Serializers de Survey — el contenedor donde vive el contenido de las
preguntas generales (grupo de flujo `gen`).

Las respuestas se escriben SIEMPRE contra el Survey, no contra el grupo:
las escalares son columnas propias, las poblaciones/autoridades son filas
de `PopulationQuantity` y la selección de poblaciones es el M2M `sectors`.
Los `GeneralGroupResponse` solo llevan flujo (ver `general_serializers`).
"""
from rest_framework import serializers

from survey.models import Survey, PopulationQuantity
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
            'id', 'sector', 'no_apply', 'name',
            'number_men', 'number_women']


class SurveySerializer(serializers.ModelSerializer):
    """Escritura y lectura del contenido de las generales.

    `population_quantities` tiene semántica de sincronización completa:
    si la clave viene, la lista ES el estado final (upsert por sector y
    borrado de los sectores ausentes); si no viene, no se toca nada.
    """
    population_quantities = PopulationQuantitySerializer(
        many=True, required=False)

    class Meta:
        model = Survey
        fields = '__all__'
        read_only_fields = ('institution', 'period')

    def validate_population_quantities(self, value: list) -> list:
        sectors = [row['sector'] for row in value]
        if len(sectors) != len(set(sectors)):
            raise serializers.ValidationError(
                'Hay sectores repetidos en la lista de poblaciones.')
        return value

    def update(self, instance: Survey, validated_data: dict) -> Survey:
        rows = validated_data.pop('population_quantities', None)
        survey = super().update(instance, validated_data)
        if rows is not None:
            self._sync_population_quantities(survey, rows)
        return survey

    def create(self, validated_data: dict) -> Survey:
        rows = validated_data.pop('population_quantities', None)
        survey = super().create(validated_data)
        if rows is not None:
            self._sync_population_quantities(survey, rows)
        return survey

    @staticmethod
    def _sync_population_quantities(survey: Survey, rows: list) -> None:
        """Deja las filas del survey idénticas a `rows` (upsert + borrado)."""
        sent_sectors = []
        for row in rows:
            data = {k: v for k, v in row.items() if k not in ('id', 'sector')}
            sector = row['sector']
            sent_sectors.append(sector.pk)
            PopulationQuantity.objects.update_or_create(
                survey=survey, sector=sector, defaults=data)
        survey.population_quantities.exclude(
            sector_id__in=sent_sectors).delete()


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
