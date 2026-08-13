from rest_framework import serializers

from survey.models import Survey
from example.models import (
    Feature, GoodPractice, FeatureOption, FeatureGoodPractice,
    GoodPracticePackage)
from api.views.ies.serializers import (
    InstitutionSimpleSerializer, PeriodSimpleSerializer)
from flow.serializers import AttachmentSerializer, FlowEventSerializer


def hide_review_fields(serializer, data: dict, names: list[str]) -> dict:
    """Quita campos de calificación cuando quien consulta no es revisora.

    Se aplica en ``to_representation`` (no en ``__init__``)
    porque los serializers anidados se instancian en tiempo de import, sin
    ``request``; aquí el ``context`` ya está disponible y DRF lo propaga a
    cualquier profundidad.
    """
    request = serializer.context.get('request')
    user = getattr(request, 'user', None)
    if user and user.is_authenticated and user.is_reviewer:
        return data
    for name in names:
        data.pop(name, None)
    return data


class FeatureOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureOption
        fields = '__all__'


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'


class FeatureFullSerializer(FeatureSerializer):
    feature_options = FeatureOptionSerializer(
        many=True, read_only=True, source='options')


class FeatureGoodPracticeSerializer(serializers.ModelSerializer):
    flow_attachments = AttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = FeatureGoodPractice
        fields = '__all__'

    def to_representation(self, instance) -> dict:
        data = super().to_representation(instance)
        return hide_review_fields(
            self, data, ['final_option', 'comments', 'reviewers'])


class GoodPracticeSerializer(serializers.ModelSerializer):
    # status = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = GoodPractice
        fields = '__all__'

    def to_representation(self, instance) -> dict:
        data = super().to_representation(instance)
        return hide_review_fields(self, data, ['final_value'])


class GoodPracticeFullSerializer(GoodPracticeSerializer):
    feature_values = FeatureGoodPracticeSerializer(many=True, read_only=True)
    flow_events = FlowEventSerializer(many=True, read_only=True)
    flow_attachments = AttachmentSerializer(many=True, read_only=True)


class SurveySemiFullSerializer(serializers.ModelSerializer):
    institution_full = InstitutionSimpleSerializer(
        read_only=True, source='institution')
    period_full = PeriodSimpleSerializer(read_only=True, source='period')

    class Meta:
        model = Survey
        fields = '__all__'


class GoodPracticePackageSerializer(serializers.ModelSerializer):
    good_practices_count = serializers.SerializerMethodField()
    survey_full = SurveySemiFullSerializer(read_only=True, source='survey')
    # status = serializers.PrimaryKeyRelatedField(read_only=True)

    def get_good_practices_count(self, obj):
        return obj.good_practices.count()

    class Meta:
        model = GoodPracticePackage
        fields = '__all__'


class GoodPracticePackageFullSerializer(serializers.ModelSerializer):
    good_practices = GoodPracticeFullSerializer(many=True, read_only=True)
    survey_full = SurveySemiFullSerializer(read_only=True, source='survey')
    flow_events = FlowEventSerializer(many=True, read_only=True)
    # status = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = GoodPracticePackage
        fields = '__all__'

