from rest_framework import serializers

from ies.models import Period, Institution
from survey.models import Survey, AxisValue, GeneralPackage
from example.models import GoodPracticePackage
from api.views.common_serializers import InvitationTokenBaseSerializer


class PeriodSimpleSerializer(serializers.ModelSerializer):
    is_bp_submission_closed = serializers.BooleanField(read_only=True)
    is_gen_submission_closed = serializers.BooleanField(read_only=True)

    class Meta:
        model = Period
        fields = '__all__'


class AxisValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AxisValue
        fields = '__all__'


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'


class GoodPracticePackageSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodPracticePackage
        fields = '__all__'


class GeneralPackageSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralPackage
        fields = '__all__'


class SurveyFullSerializer(SurveySerializer):
    axis_values = AxisValueSerializer(many=True, read_only=True)
    packages = GoodPracticePackageSimpleSerializer(
        many=True, read_only=True)
    general_package = GeneralPackageSimpleSerializer(read_only=True)


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
