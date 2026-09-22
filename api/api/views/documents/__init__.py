"""ViewSet de gestión de documentos públicos (dashboard)."""
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.permissions import IsReviewer
from api.views.common_views import BaseGenericViewSet
from api.views.documents.serializers import PublicDocumentSerializer
from documents.models import PublicDocument

GENERATED_DELETE_ERROR = (
    "Los documentos generados desde la base no se pueden eliminar.")


class PublicDocumentViewSet(BaseGenericViewSet):
    # También la lectura: la lista de gestión incluye borradores, que el
    # público solo ve publicados por /public-documents/.
    permission_classes = [IsReviewer]
    queryset = PublicDocument.objects.all()
    serializer_class = PublicDocumentSerializer
    search_fields = ['title', 'description']

    # Solo los generados se protegen; los subidos se eliminan. Se guardan
    # las dos vías: `confirm-delete` de CustomDeleteMixin no pasa por
    # `destroy`.
    def _generated_refusal(self):
        if self.get_object().generator:
            return Response(
                {"detail": GENERATED_DELETE_ERROR},
                status=status.HTTP_400_BAD_REQUEST)
        return None

    def destroy(self, request, *args, **kwargs):
        return self._generated_refusal() or super().destroy(
            request, *args, **kwargs)

    # Al sobrescribir hay que repetir el decorador: sin él, el router ya
    # no registra la ruta `confirm-delete`.
    @action(detail=True, methods=["delete"], url_path="confirm-delete")
    def confirm_delete(self, request, pk=None):
        return self._generated_refusal() or super().confirm_delete(
            request, pk=pk)
