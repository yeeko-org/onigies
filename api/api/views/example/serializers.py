from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from survey.models import Survey
from example.models import (
    Feature, GoodPractice, FeatureOption, FeatureGoodPractice,
    GoodPracticePackage)
from api.views.ies.serializers import (
    InstitutionSimpleSerializer, PeriodSimpleSerializer)
from flow.permissions import user_holds_root_turn
from flow.serializers import AttachmentSerializer, FlowEventSerializer


def _request_user(serializer):
    request = serializer.context.get('request')
    user = getattr(request, 'user', None)
    return user if user and user.is_authenticated else None


def is_reviewer_request(serializer) -> bool:
    user = _request_user(serializer)
    return bool(user and user.is_reviewer)


def is_admin_request(serializer) -> bool:
    user = _request_user(serializer)
    return bool(user and user.is_admin)


def split_review_fields(serializer, attrs: dict, names: list[str]) -> dict:
    """Cada lado escribe solo lo suyo: a la IES se le descartan los campos
    de la calificación y a la revisión todo lo demás (el contenido de la
    IES), en silencio, porque ambos formularios reenvían la ficha
    completa. El candado de turno del contenido vive en la vista. El
    admin escribe ambos lados.
    """
    if is_admin_request(serializer):
        return attrs
    keep_review = is_reviewer_request(serializer)
    for name in list(attrs):
        if (name in names) != keep_review:
            attrs.pop(name)
    return attrs


def hide_review_fields(serializer, data: dict, names: list[str]) -> dict:
    """Quita campos de calificación cuando quien consulta no es revisora.

    Se aplica en ``to_representation`` (no en ``__init__``)
    porque los serializers anidados se instancian en tiempo de import, sin
    ``request``; aquí el ``context`` ya está disponible y DRF lo propaga a
    cualquier profundidad.
    """
    if is_reviewer_request(serializer):
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


# Campos de la calificación: la IES no los ve ni los escribe, y son lo
# único que escribe la revisión.
FEATURE_REVIEW_FIELDS = ['final_option', 'comments', 'reviewers']
PRACTICE_REVIEW_FIELDS = ['final_value']


class FeatureGoodPracticeSerializer(serializers.ModelSerializer):
    flow_attachments = AttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = FeatureGoodPractice
        fields = '__all__'

    def validate(self, attrs: dict) -> dict:
        """El criterio no cambia de práctica ni de característica después
        de nacer, la IES no escribe la calificación y la revisión no
        escribe la marca de la IES: ambos formularios reenvían la ficha
        completa, así que esos campos se descartan en silencio en vez de
        rechazar el guardado.

        Candado de `comments`, la nota privada de la revisión por
        criterio (task-70): solo se escribe del lado de la revisión y
        mientras el envío esté en su turno, como los comentarios del
        timeline. Un valor sin cambios no cuenta como escritura, porque
        la revisión reenvía la ficha completa al calificar.
        """
        if self.instance is not None:
            attrs.pop('good_practice', None)
            attrs.pop('feature', None)
        split_review_fields(self, attrs, FEATURE_REVIEW_FIELDS)
        if not is_reviewer_request(self) or 'comments' not in attrs:
            return attrs
        current = self.instance.comments if self.instance else None
        if (attrs['comments'] or '') == (current or ''):
            return attrs
        good_practice = getattr(self.instance, 'good_practice', None)
        user = self.context['request'].user
        if good_practice is None or not user_holds_root_turn(
                user, good_practice):
            raise PermissionDenied(
                'El envío no está en revisión; los comentarios de los '
                'criterios ya no se pueden modificar.')
        return attrs

    def to_representation(self, instance) -> dict:
        data = super().to_representation(instance)
        return hide_review_fields(self, data, FEATURE_REVIEW_FIELDS)


class GoodPracticeSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoodPractice
        fields = '__all__'
        # El status solo cambia por el motor (/flow/…/transitions/).
        read_only_fields = ['status']

    def validate(self, attrs: dict) -> dict:
        return split_review_fields(self, attrs, PRACTICE_REVIEW_FIELDS)

    def to_representation(self, instance) -> dict:
        data = super().to_representation(instance)
        return hide_review_fields(self, data, PRACTICE_REVIEW_FIELDS)


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
    # Motivo que la revisión ve mientras la raíz sigue en turno de la IES
    # (`flow.permissions.root_turn_errors`); constante de clase, sin query.
    not_sent_message = serializers.ReadOnlyField(
        source='root_not_sent_message')

    def get_good_practices_count(self, obj):
        return obj.good_practices.count()

    class Meta:
        model = GoodPracticePackage
        fields = '__all__'
        read_only_fields = ['status']


class GoodPracticePackageFullSerializer(serializers.ModelSerializer):
    good_practices = GoodPracticeFullSerializer(many=True, read_only=True)
    survey_full = SurveySemiFullSerializer(read_only=True, source='survey')
    flow_events = FlowEventSerializer(many=True, read_only=True)
    not_sent_message = serializers.ReadOnlyField(
        source='root_not_sent_message')

    class Meta:
        model = GoodPracticePackage
        fields = '__all__'
        read_only_fields = ['status']

