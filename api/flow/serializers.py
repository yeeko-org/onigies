"""Serializers del motor de flujo."""
from django.core.files.uploadedfile import UploadedFile
from rest_framework import serializers

from flow.models import Attachment, FlowEvent, Status

MAX_ATTACHMENT_SIZE = 30 * 1024 * 1024


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
    """Adjunto de un objeto del flujo.

    Se anida tanto en FlowEvent como en los serializers de detalle de
    los targets (`flow_attachments`). `uploaded_by` viaja como pk: el
    front resuelve el nombre con su catálogo de usuarias, igual que con
    `FlowEvent.user`.
    """
    name = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Attachment
        fields = ['id', 'name', 'url', 'uploaded_by', 'created_at']

    def get_name(self, obj) -> str:
        """Nombre visible: solo el archivo, sin la ruta de subida."""
        return obj.file.name.rsplit('/', 1)[-1] if obj.file else ''

    def get_url(self, obj) -> str | None:
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return obj.file.url if obj.file else None


class AttachmentUploadSerializer(serializers.Serializer):
    """Payload de subida de un adjunto (multipart).

    No se valida extensión ni content-type a propósito: la evidencia de
    una IES llega en formatos impredecibles y filtrarlos bloquearía
    entregas legítimas. El único tope es el tamaño.
    """
    file = serializers.FileField()

    def validate_file(self, value: UploadedFile) -> UploadedFile:
        if value.size > MAX_ATTACHMENT_SIZE:
            raise serializers.ValidationError(
                "El archivo supera el límite de 30 MB.")
        return value


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