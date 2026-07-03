"""
Vistas del motor de flujo de validación.

Endpoints:
  POST /flow/<app>/<model>/<pk>/transitions/ — ejecutar transición
  GET  /flow/<app>/<model>/<pk>/events/     — timeline del objeto
  POST /flow/<app>/<model>/<pk>/events/     — agregar comentario puro
  GET  /flow/statuses/                       — catálogo de status
"""
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from flow.models import FlowEvent, Status
from flow.serializers import (
    CommentSerializer,
    FlowEventSerializer,
    StatusSerializer,
    TransitionRequestSerializer,
)
from flow.services import execute_transition, get_user_flow_role
from flow.registry import is_flow_participant


class FlowObjectMixin:
    """
    Resuelve el objeto del flujo desde la URL (<app_label>/<model>/<pk>).
    Verifica que el modelo participe en el flujo.
    """

    def _get_flow_object(self, app_label: str, model_name: str, pk: int):
        try:
            model = apps.get_model(app_label, model_name)
        except LookupError:
            raise NotFound(f"Modelo '{app_label}.{model_name}' no encontrado.")

        if not is_flow_participant(model):
            raise NotFound(
                f"'{app_label}.{model_name}' no participa en el flujo.")

        qs = model.objects.select_related('status')
        try:
            return qs.get(pk=pk)
        except model.DoesNotExist:
            raise NotFound(f"Objeto {pk} no encontrado.")

    def _get_content_type(self, obj) -> ContentType:
        return ContentType.objects.get_for_model(obj)


class FlowTransitionView(FlowObjectMixin, APIView):
    """
    POST — ejecuta una transición sobre el objeto. Las transiciones
    disponibles se calculan en el cliente desde el catálogo de status
    (mismas reglas que `get_available_transitions`: rol + next_statuses +
    applicable_models). La regla de hijos se valida aquí, en el POST.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, app_label, model_name, pk):
        """Ejecuta la transición indicada en el payload."""
        obj = self._get_flow_object(app_label, model_name, pk)
        serializer = TransitionRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        target: Status = serializer.validated_data['target_status']
        comment: str = serializer.validated_data.get('comment', '')

        try:
            event = execute_transition(
                request.user, obj, target, comment or None)
        except ValueError as exc:
            errors = exc.args[0]
            return Response(
                {'detail': errors[0] if len(errors) == 1 else errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            FlowEventSerializer(event, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )


class FlowEventView(FlowObjectMixin, APIView):
    """
    GET  — timeline completo del objeto (cambios de status + comentarios).
    POST — agrega un comentario puro (sin cambio de status).
    """
    permission_classes = [IsAuthenticated]

    def _get_events(self, obj):
        ct = self._get_content_type(obj)
        return (FlowEvent.objects
                .filter(content_type=ct, object_id=obj.pk)
                .select_related('from_status', 'to_status', 'user')
                .prefetch_related('attachments'))

    def get(self, request, app_label, model_name, pk):
        """Retorna el timeline del objeto, del más reciente al más antiguo."""
        obj = self._get_flow_object(app_label, model_name, pk)
        events = self._get_events(obj)
        serializer = FlowEventSerializer(
            events, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, app_label, model_name, pk):
        """Agrega un comentario puro al timeline (sin cambiar el status)."""
        obj = self._get_flow_object(app_label, model_name, pk)

        # Solo comenta quien tiene el turno: el rol del usuario debe coincidir
        # con el role del status actual (guard simétrico IES/revisora).
        current_role = obj.status.role if obj.status else None
        if get_user_flow_role(request.user) != current_role:
            return Response(
                {'detail': 'No es tu turno para comentar en este objeto.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ct = self._get_content_type(obj)
        event = FlowEvent.objects.create(
            content_type=ct,
            object_id=obj.pk,
            from_status=None,
            to_status=None,
            user=request.user,
            comment=serializer.validated_data['comment'],
        )
        return Response(
            FlowEventSerializer(event, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )


class StatusViewSet(ReadOnlyModelViewSet):
    """
    Catálogo de status del flujo. Solo lectura.
    Soporta filtrado por ?group=bp|cp|gen.
    """
    serializer_class = StatusSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'name'

    def get_queryset(self):
        qs = (Status.objects
              .prefetch_related(
                  'next_statuses', 'valid_child_statuses',
                  'applicable_models')
              .order_by('group', 'order'))
        group = self.request.query_params.get('group')
        if group:
            qs = qs.filter(group=group)
        return qs