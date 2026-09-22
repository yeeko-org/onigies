import os

from django.urls import reverse
from django.utils import timezone
from rest_framework import serializers

from documents.models import PublicDocument


def download_url(request, document: PublicDocument) -> str:
    """URL absoluta de descarga, la misma para archivo subido o generado."""
    path = reverse('public_document_download', args=[document.slug])
    return request.build_absolute_uri(path) if request else path


class PublicDocumentSerializer(serializers.ModelSerializer):
    """Gestión desde el dashboard; valida archivo XOR generador."""
    download_url = serializers.SerializerMethodField()
    file_name = serializers.SerializerMethodField()

    class Meta:
        model = PublicDocument
        fields = [
            'id', 'title', 'slug', 'description', 'file', 'file_name',
            'generator', 'is_published', 'order', 'download_url',
            'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {'slug': {'required': False}}

    def get_download_url(self, obj: PublicDocument) -> str:
        return download_url(self.context.get('request'), obj)

    def get_file_name(self, obj: PublicDocument) -> str | None:
        return os.path.basename(obj.file.name) if obj.file else None

    def validate_slug(self, value: str) -> str:
        instance = self.instance
        if instance and instance.generator and value != instance.slug:
            raise serializers.ValidationError(
                "El slug de un documento generado no se puede cambiar.")
        return value

    def validate(self, attrs):
        instance = self.instance
        file = attrs.get('file', instance.file if instance else None)
        generator = attrs.get(
            'generator', instance.generator if instance else '')
        if bool(file) == bool(generator):
            raise serializers.ValidationError(
                "Sube un archivo o elige un generador, no ambos ni ninguno.")
        return attrs


class PublicDocumentPublicSerializer(serializers.ModelSerializer):
    """Lista pública: solo lo que el sitio y las IES necesitan."""
    download_url = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = PublicDocument
        fields = [
            'title', 'slug', 'description', 'download_url', 'updated_at']

    def get_download_url(self, obj: PublicDocument) -> str:
        return download_url(self.context.get('request'), obj)

    def get_updated_at(self, obj: PublicDocument) -> str:
        # Lo generado se arma al descargarlo: su fecha es la de ahora.
        date = timezone.now() if obj.generator else obj.updated_at
        return serializers.DateTimeField().to_representation(date)
