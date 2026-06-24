"""Serializers del motor de flujo."""
from rest_framework import serializers

from flow.models import Attachment, FlowEvent, Status


class StatusSerializer(serializers.ModelSerializer):
    """Status completo para el catálogo."""
    next_statuses = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='name')
    valid_child_statuses = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='name')
    applicable_models = serializers.SerializerMethodField()

    class Meta:
        model = Status
        fields = '__all__'

    def get_applicable_models(self, obj) -> list[str]:
        return list(
            obj.applicable_models.values_list('app_label', 'model'))


class AttachmentSerializer(serializers.ModelSerializer):
    """Adjunto compacto para anidar en FlowEvent."""
    url = serializers.SerializerMethodField()

    class Meta:
        model = Attachment
        fields = ['id', 'url', 'created_at']

    def get_url(self, obj) -> str | None:
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return obj.file.url if obj.file else None


class FlowEventSerializer(serializers.ModelSerializer):
    """Evento del timeline (cambio de status o comentario puro).
    """
    attachments = AttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = FlowEvent
        fields = [
            'id', 'from_status', 'to_status',
            'user', 'comment', 'created_at', 'attachments',
        ]


class TransitionRequestSerializer(serializers.Serializer):
    """Payload para ejecutar una transición."""
    target_status = serializers.CharField()
    comment = serializers.CharField(
        required=False, allow_blank=True, default='')

    def validate_target_status(self, value: str) -> Status:
        try:
            return Status.objects.get(name=value)
        except Status.DoesNotExist:
            raise serializers.ValidationError(
                f"Status '{value}' no existe.")


class CommentSerializer(serializers.Serializer):
    """Payload para agregar un comentario puro al timeline."""
    comment = serializers.CharField(min_length=1)