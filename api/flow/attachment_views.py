"""
Vistas de adjuntos del flujo (`flow.Attachment`).

Endpoints genéricos, un solo juego para todos los targets:
  GET    /flow/<app>/<model>/<pk>/attachments/       — lista
  POST   /flow/<app>/<model>/<pk>/attachments/       — sube (multipart)
  DELETE /flow/<app>/<model>/<pk>/attachments/<id>/  — borra

El adjunto se ancla AL OBJETO (GenericFK `target`), nunca al evento del
timeline: `event` queda en null. Quién puede escribir se deriva del
flujo (turno de la raíz + `content_editable` del status propio), así que
la revisión solo lee y una IES nunca toca archivos de otra institución.
"""
from django.apps import apps
from rest_framework import status as http_status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from flow.models import Attachment
from flow.permissions import (
    user_can_act_on_flow_object, user_can_edit_flow_content)
from flow.registry import (
    get_flow_delegate, is_flow_participant, resolve_flow_owner)
from flow.serializers import AttachmentSerializer, AttachmentUploadSerializer


class AttachmentTargetMixin:
    """
    Resuelve el target del adjunto desde la URL y aplica los permisos.

    A diferencia de `FlowObjectMixin`, admite también los satélites que
    no participan del flujo pero declaran `flow_delegate`
    (FeatureGoodPractice → GoodPractice): el objeto que gobierna los
    permisos es el delegado.
    """

    def _get_target(self, app_label: str, model_name: str, pk: int):
        """Instancia adjuntable de la URL, o 404."""
        try:
            model = apps.get_model(app_label, model_name)
        except LookupError:
            raise NotFound(f"Modelo '{app_label}.{model_name}' no encontrado.")

        delegate = get_flow_delegate(model)
        if not is_flow_participant(model) and delegate is None:
            msg = f"'{app_label}.{model_name}' no admite adjuntos."
            raise NotFound(msg)

        qs = model.objects.select_related(delegate or 'status')
        try:
            return qs.get(pk=pk)
        except model.DoesNotExist:
            raise NotFound(f"Objeto {pk} no encontrado.")

    def _check_read(self, request, target) -> None:
        """403 si quien consulta no es de la institución dueña."""
        owner = resolve_flow_owner(target)
        if not user_can_act_on_flow_object(request.user, owner):
            raise PermissionDenied("No tienes acceso a este objeto.")

    def _check_write(self, request, target) -> None:
        """403 si no puede subir ni borrar adjuntos de este objeto.

        Los adjuntos son evidencia de la IES: la revisión solo lee,
        aunque tenga acceso al objeto. Para la IES rige la misma regla
        que el contenido, así que enviado el paquete ya no se toca.
        """
        self._check_read(request, target)
        if request.user.is_reviewer:
            raise PermissionDenied(
                "La revisión no modifica los adjuntos de la IES.")
        owner = resolve_flow_owner(target)
        if not user_can_edit_flow_content(request.user, owner):
            raise PermissionDenied(
                "No puedes modificar los adjuntos en este estado.")


class FlowAttachmentView(AttachmentTargetMixin, APIView):
    """
    GET  — adjuntos del objeto, del más reciente al más antiguo.
    POST — sube un adjunto (multipart, campo `file`).
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, app_label, model_name, pk):
        """Lista los adjuntos anclados al objeto."""
        target = self._get_target(app_label, model_name, pk)
        self._check_read(request, target)
        serializer = AttachmentSerializer(
            target.flow_attachments.all(), many=True,
            context={'request': request})
        return Response(serializer.data)

    def post(self, request, app_label, model_name, pk):
        """Adjunta un archivo al objeto y registra quién lo subió."""
        target = self._get_target(app_label, model_name, pk)
        self._check_write(request, target)

        serializer = AttachmentUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        attachment = Attachment.objects.create(
            target=target,
            file=serializer.validated_data['file'],
            uploaded_by=request.user,
        )
        return Response(
            AttachmentSerializer(
                attachment, context={'request': request}).data,
            status=http_status.HTTP_201_CREATED,
        )


class FlowAttachmentDetailView(AttachmentTargetMixin, APIView):
    """DELETE — borra un adjunto del objeto."""
    permission_classes = [IsAuthenticated]

    def delete(self, request, app_label, model_name, pk, attachment_id):
        """Borra el adjunto, siempre acotado al target de la URL."""
        target = self._get_target(app_label, model_name, pk)
        self._check_write(request, target)

        # Se busca dentro de la relación del target, no por id suelto:
        # así un id ajeno es 404 y no hay borrado cruzado.
        try:
            attachment = target.flow_attachments.get(pk=attachment_id)
        except Attachment.DoesNotExist:
            raise NotFound(f"Adjunto {attachment_id} no encontrado.")

        attachment.delete()
        return Response(status=http_status.HTTP_204_NO_CONTENT)
