"""Descarga pública de documentos: sin sesión, sin token."""
from django.http import FileResponse, Http404
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.views.documents.serializers import PublicDocumentPublicSerializer
from documents.generators import GENERATORS
from documents.models import PublicDocument
from utils.files import stored_file_response


class PublicDocumentListView(APIView):
    """Documentos publicados, en el orden del dashboard."""
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request: Request) -> Response:
        documents = PublicDocument.objects.filter(is_published=True)
        serializer = PublicDocumentPublicSerializer(
            documents, many=True, context={'request': request})
        return Response(serializer.data)


class PublicDocumentDownloadView(APIView):
    """Entrega el documento: generado al vuelo o el archivo subido."""
    permission_classes = [AllowAny]

    def get(self, request: Request, slug: str):
        document = PublicDocument.objects.filter(slug=slug).first()
        # Un borrador no existe para el público; la revisión sí lo
        # descarga, para revisarlo antes de publicarlo.
        user = request.user
        can_see_drafts = user.is_authenticated and user.is_reviewer
        if document is None or not (
                document.is_published or can_see_drafts):
            raise Http404("Documento no encontrado.")

        if document.generator:
            generated = GENERATORS[document.generator]
            return FileResponse(
                generated.build(), as_attachment=True,
                filename=generated.filename,
                content_type=generated.content_type)
        return stored_file_response(request, document.file)
