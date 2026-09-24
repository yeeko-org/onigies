from rest_framework import serializers

from ies.models import Period, Institution
from survey.models import Survey, AxisValue, GeneralPackage
from example.models import GoodPracticePackage
from api.views.common_serializers import InvitationTokenBaseSerializer


class PeriodSimpleSerializer(serializers.ModelSerializer):
    is_bp_submission_closed = serializers.BooleanField(read_only=True)
    is_gen_submission_closed = serializers.BooleanField(read_only=True)
    is_cp_open = serializers.BooleanField(read_only=True)

    class Meta:
        model = Period
        fields = '__all__'


class AxisValueSerializer(serializers.ModelSerializer):
    """Renglón del eje en la lista de /respuestas: status propio más
    conteo de observables por status (encabezado e íconos). Cuenta en
    Python sobre los hijos prefetcheados (41 filas por eje)."""
    observables_by_status = serializers.SerializerMethodField()
    # Motivo que la revisión ve mientras la raíz sigue en turno de la IES
    # (`flow.permissions.root_turn_errors`); constante de clase, sin query.
    not_sent_message = serializers.ReadOnlyField(
        source='root_not_sent_message')

    class Meta:
        model = AxisValue
        fields = '__all__'

    def get_observables_by_status(self, obj: AxisValue) -> dict:
        result: dict = {}
        for row in obj.observable_responses.all():
            result[row.status_id] = result.get(row.status_id, 0) + 1
        return result


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'


class GoodPracticePackageSimpleSerializer(serializers.ModelSerializer):
    not_sent_message = serializers.ReadOnlyField(
        source='root_not_sent_message')

    class Meta:
        model = GoodPracticePackage
        fields = '__all__'


class GeneralPackageSimpleSerializer(serializers.ModelSerializer):
    not_sent_message = serializers.ReadOnlyField(
        source='root_not_sent_message')

    class Meta:
        model = GeneralPackage
        fields = '__all__'


class SurveyFullSerializer(SurveySerializer):
    axis_values = AxisValueSerializer(many=True, read_only=True)
    packages = GoodPracticePackageSimpleSerializer(
        many=True, read_only=True)
    general_package = GeneralPackageSimpleSerializer(read_only=True)
    # Compuerta de respuesta del cuestionario principal: el frontend
    # inhabilita la captura con `open` y explica con `reason`.
    cp_capture = serializers.SerializerMethodField()

    def get_cp_capture(self, obj: Survey) -> dict:
        from survey.cp_gate import capture_state
        return capture_state(obj)


class InstitutionSimpleSerializer(serializers.ModelSerializer):
    # El logo se sube aparte (acción upload_logo): al guardar el resto de
    # la institución nunca viaja un archivo, así que no puede exigirse.
    logo = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Institution
        fields = '__all__'


class InstitutionDetailSerializer(serializers.ModelSerializer):
    invitation_tokens = InvitationTokenBaseSerializer(
        many=True, read_only=True)
    logo = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Institution
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Import diferido: rompe el ciclo ies.serializers ⇄ example.serializers
        from api.views.example import GoodPracticePackageSerializer
        self.fields['good_practice_packages'] = GoodPracticePackageSerializer(
            many=True, read_only=True)


class InstitutionSerializer(serializers.ModelSerializer):
    good_practice_packages_count = serializers.ReadOnlyField()
    good_practices_count = serializers.ReadOnlyField()
    logo = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Institution
        fields = '__all__'


class InstitutionFullSerializer(serializers.ModelSerializer):
    surveys = SurveyFullSerializer(many=True, read_only=True)

    class Meta:
        model = Institution
        fields = '__all__'
