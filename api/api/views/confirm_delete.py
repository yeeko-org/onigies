from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from utils.register_merge import related_objects_report


# class CustomDeleteMixin(viewsets.ModelViewSet):
class NoDeleteMixin:
    """Colecciones donde ninguna fila muere desde la API.

    Las preguntas del cuestionario se editan pero no se borran: una
    pregunta borrada se lleva las respuestas capturadas o queda huérfana
    en los históricos. Las bajas de la etapa de pruebas van por seed/ORM.

    Se quita `delete` de los métodos aceptados —no se sobrescribe
    `destroy`— para que también quede fuera la acción `confirm-delete`
    de CustomDeleteMixin.
    """

    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'options']


class CustomDeleteMixin:
    disable_protection: bool = False

    def destroy(self, request, *args, **kwargs):
        if self.disable_protection:
            return super().destroy(request, *args, **kwargs)  # type: ignore
        instance = self.get_object()  # type: ignore

        report_data = []
        errors = []
        related_objects_report(
            instance, instance._meta.related_objects, report_data, errors)

        for report in report_data:
            if report["affected_records"]:
                return Response(
                    {"report_data": report_data, "errors": errors},
                    status=status.HTTP_400_BAD_REQUEST)

        return super().destroy(request, *args, **kwargs)  # type: ignore

    @action(detail=True, methods=["delete"], url_path="confirm-delete")
    def confirm_delete(self, request, pk=None):
        instance = self.get_object()  # type: ignore
        instance.delete()
        return Response({"detail": "All information deleted."}, status=status.HTTP_204_NO_CONTENT)
