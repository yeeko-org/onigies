"""
Vistas del motor de flujo de validación.

Endpoints:
  POST /flow/<app>/<model>/<pk>/transitions/ — ejecutar transición
  GET  /flow/<app>/<model>/<pk>/events/     — timeline del objeto
  POST /flow/<app>/<model>/<pk>/events/     — agregar comentario puro
  PATCH/DELETE /flow/<app>/<model>/<pk>/events/<event_pk>/
                                             — editar / borrar comentario
  POST /flow/<app>/<model>/<pk>/admin-transitions/ — válvula de admin
  GET  /flow/statuses/                       — catálogo de status
"""
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from flow.models import FlowEvent, Status
from flow.serializers import (
    AdminTransitionRequestSerializer,
    CommentSerializer,
    FlowEventSerializer,
    StatusSerializer,
    TransitionRequestSerializer,
)
from flow.services import (
    execute_admin_transition, execute_transition, get_user_flow_role,
    is_admin_event)
from flow.registry import is_flow_participant
from flow.permissions import (
    resolve_flow_root, round_started_at, user_can_act_on_flow_object,
    user_holds_root_turn)


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

    def _check_ownership(self, request, obj) -> None:
        """403 si la persona usuaria no pertenece a la institución dueña.

        Las revisoras pasan siempre; una IES solo puede tocar objetos de
        su propia institución (ver flow.permissions).
        """
        if not user_can_act_on_flow_object(request.user, obj):
            raise PermissionDenied(
                "No tienes acceso a este objeto del flujo.")


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
        self._check_ownership(request, obj)
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


class FlowAdminTransitionView(FlowObjectMixin, APIView):
    """
    POST — válvula de admin (adr-0023): lleva un hijo o nieto a cualquier
    destino de la revisión mientras la raíz esté en rol reviewer, fuera
    de `next_statuses`. Mismo payload y misma respuesta que
    `FlowTransitionView`, con el comentario obligatorio.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, app_label, model_name, pk):
        if not request.user.is_admin:
            raise PermissionDenied(
                "Solo una cuenta de administración puede hacer cambios "
                "administrativos de estatus.")
        obj = self._get_flow_object(app_label, model_name, pk)
        self._check_ownership(request, obj)
        serializer = AdminTransitionRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        target: Status = serializer.validated_data['target_status']
        comment: str = serializer.validated_data['comment']

        try:
            event = execute_admin_transition(
                request.user, obj, target, comment)
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
        self._check_ownership(request, obj)
        events = self._get_events(obj)
        serializer = FlowEventSerializer(
            events, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, app_label, model_name, pk):
        """Agrega un comentario puro al timeline (sin cambiar el status)."""
        obj = self._get_flow_object(app_label, model_name, pk)
        self._check_ownership(request, obj)

        # Solo comenta el lado que tiene el turno de la RAÍZ, como el resto
        # del motor: un hijo en un status de la revisión no se comenta
        # mientras la IES no haya enviado el paquete o el eje.
        if not user_holds_root_turn(request.user, obj):
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


class FlowEventDetailView(FlowObjectMixin, APIView):
    """
    PATCH  — edita el texto de un comentario del timeline.
    DELETE — borra el comentario: la fila si es un comentario puro; solo
             el texto si es el comentario de una transición (el cambio de
             status se queda en la bitácora). El motivo de un cambio
             administrativo no se borra (403), solo se edita.

    Lo puede tocar cualquiera del mismo lado que quien lo escribió (la
    autoría no importa), solo dentro de la ronda en curso: la raíz está
    en su turno y el comentario es posterior a la última vez que la raíz
    entró a su lado. Lo de rondas anteriores ya lo leyó la contraparte y
    se queda como quedó. El motivo de un cambio administrativo solo lo
    corrige una cuenta de administración.
    """
    permission_classes = [IsAuthenticated]

    def _get_editable_event(self, request, app_label, model_name, pk,
                            event_pk) -> FlowEvent:
        obj = self._get_flow_object(app_label, model_name, pk)
        self._check_ownership(request, obj)
        event = (FlowEvent.objects
                 .select_related('user')
                 .filter(content_type=self._get_content_type(obj),
                         object_id=obj.pk, pk=event_pk)
                 .first())
        if event is None or not event.comment:
            raise NotFound("Comentario no encontrado.")
        if get_user_flow_role(event.user) != get_user_flow_role(request.user):
            raise PermissionDenied(
                "Solo puedes modificar los comentarios de tu lado.")
        if not user_holds_root_turn(request.user, obj):
            raise PermissionDenied(
                "Ya no es tu turno en este envío; sus comentarios ya no se "
                "pueden modificar.")
        started = round_started_at(
            resolve_flow_root(obj), get_user_flow_role(request.user))
        if started is not None and event.created_at <= started:
            raise PermissionDenied(
                "Ese comentario es de una ronda anterior; ya no se puede "
                "modificar.")
        return event

    def patch(self, request, app_label, model_name, pk, event_pk):
        event = self._get_editable_event(
            request, app_label, model_name, pk, event_pk)
        if is_admin_event(event) and not request.user.is_admin:
            raise PermissionDenied(
                "Solo una cuenta de administración corrige el motivo de un "
                "cambio administrativo.")
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event.comment = serializer.validated_data['comment']
        event.save(update_fields=['comment'])
        return Response(
            FlowEventSerializer(event, context={'request': request}).data)

    def delete(self, request, app_label, model_name, pk, event_pk):
        event = self._get_editable_event(
            request, app_label, model_name, pk, event_pk)
        # Sin su motivo, el cambio administrativo quedaría como una
        # escritura fuera del grafo sin etiqueta en el timeline.
        if is_admin_event(event):
            raise PermissionDenied(
                "El motivo de un cambio administrativo no se borra; solo "
                "se puede corregir.")
        if event.to_status_id is None:
            event.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        event.comment = ''
        event.save(update_fields=['comment'])
        return Response(
            FlowEventSerializer(event, context={'request': request}).data)


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