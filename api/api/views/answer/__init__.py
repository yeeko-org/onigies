"""
ViewSets de la captura del cuestionario principal (flujo `cp`).

- `AxisValueViewSet` (colección `axis_value`): lectura del eje con su
  cuestionario y respuestas; la unidad de envío.
- `ObservableResponseViewSet` (`observable_response`): PATCH del
  booleano inicial, con la lógica de dominio de `answer.services`.
- `GroupResponseViewSet` (`group_response`): PATCH de las respuestas
  tipadas de un grupo completo; promueve a `cp_filling` en el primer
  guardado.

Ambos PATCH devuelven, además del objeto, el status de sus ancestros
tras la propagación (`observable_status`, `axis_status`): el cliente
no tiene que releer el observable ni el eje por cada guardado.

Las transiciones, comentarios y adjuntos van por los endpoints
genéricos de `flow` (`/flow/answer/<model>/<pk>/…`). Quién escribe
contenido: la IES dueña, con el status propio editable, la raíz en su
turno y la compuerta de respuesta abierta (`user_can_edit_flow_content`
+ `survey.cp_gate`); la revisión solo lee, como con los adjuntos.
"""
from django.db.models import Prefetch
from django_filters import CharFilter, FilterSet, NumberFilter
from rest_framework import mixins, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from answer.models import GroupResponse, ObservableResponse
from answer.services import InitValueError, set_init_value
from api.views.answer.serializers import (
    AxisValueFullSerializer, AxisValueSerializer,
    GroupResponseFullSerializer, ObservableResponseFullSerializer,
    ObservableResponseSerializer)
from api.views.common_views import BaseGenericViewSet
from flow.permissions import (
    IsFlowInstitutionOwnerOrReviewer, user_can_edit_flow_content)
from flow.services import assign_auto_status
from indicator.models import Sector
from survey.cp_gate import check_capture_open
from survey.models import AxisValue

FLOW_PREFETCH = ('flow_events__user', 'flow_events__attachments')


def group_responses_prefetch(prefix: str = '') -> Prefetch:
    """Grupos con sus respuestas tipadas y timeline, en el orden del
    bloque (`QuestionType.order`)."""
    queryset = GroupResponse.objects.select_related(
        'question_type').prefetch_related(
            'a_responses', 'b_responses', 'reach_responses__sectors',
            'plan_responses', 'special_responses', 'flow_attachments',
            *FLOW_PREFETCH).order_by('question_type__order')
    return Prefetch(f'{prefix}statuses', queryset=queryset)


def observable_responses_prefetch(prefix: str = '') -> Prefetch:
    """Observables del eje en el orden del instrumento, con instrumento,
    grupos y timeline resueltos."""
    queryset = ObservableResponse.objects.select_related(
        'observable__component').prefetch_related(
            'observable__aquestion_set', 'observable__bquestion_set',
            'observable__reachquestion_set__others_sectors',
            'observable__planquestion_set',
            'observable__specialquestion_set',
            group_responses_prefetch(), *FLOW_PREFETCH,
        ).order_by('observable__order')
    return Prefetch(f'{prefix}observable_responses', queryset=queryset)


class InstitutionScopedMixin:
    """Las revisoras ven todo; una IES solo lo de su institución."""
    survey_path = 'survey'

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_anonymous:
            return qs.none()
        if user.is_reviewer:
            return qs
        if user.institution_id:
            return qs.filter(**{
                f'{self.survey_path}__institution_id': user.institution_id})
        return qs.none()


class ContentWriteMixin:
    """403 con `code` cuando la persona usuaria no puede escribir el
    contenido del objeto hoy."""

    def check_content_write(self, obj, survey) -> None:
        user = self.request.user
        if user.is_reviewer:
            raise PermissionDenied({
                'detail': 'La revisión no captura respuestas de la IES.',
                'code': 'reviewer_read_only'})
        check_capture_open(user, survey)
        if not user_can_edit_flow_content(user, obj):
            raise PermissionDenied({
                'detail': 'No puedes editar esta respuesta en su estado '
                          'actual.',
                'code': 'not_editable'})


class AxisValueFilter(FilterSet):
    institution = NumberFilter(field_name='survey__institution')
    period = NumberFilter(field_name='survey__period')
    status = CharFilter(field_name='status')

    class Meta:
        model = AxisValue
        fields = {}


class AxisValueViewSet(InstitutionScopedMixin, BaseGenericViewSet):
    """Raíz del flujo cp, solo lectura (`http_method_names`): nace de
    `Institution.save` y su status lo mueve el motor."""
    permission_classes = [IsAuthenticated, IsFlowInstitutionOwnerOrReviewer]
    queryset = AxisValue.objects.all().select_related(
        'axis', 'survey__institution', 'survey__period', 'status')
    serializer_class = AxisValueSerializer
    search_fields = [
        'survey__institution__name', 'survey__institution__acronym']
    ordering_fields = [
        'id', 'axis__order', 'survey__period__year',
        'survey__institution__name', 'status__order', 'status__priority']
    ordering = ['survey__institution__name', 'axis__order']
    filterset_class = AxisValueFilter
    http_method_names = ['get', 'head', 'options']

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == 'retrieve':
            return qs.select_related('survey__general_package') \
                .prefetch_related(
                    observable_responses_prefetch(),
                    'survey__question_responses__general_question',
                    *FLOW_PREFETCH)
        return qs.prefetch_related(Prefetch(
            'observable_responses',
            queryset=ObservableResponse.objects.only(
                'id', 'status', 'axis_value')))

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AxisValueFullSerializer
        return self.serializer_class

    def get_serializer_context(self) -> dict:
        context = super().get_serializer_context()
        # Una consulta para todas las ReachQuestion estándar del eje.
        context['main_sectors'] = list(
            Sector.objects.filter(is_main=True).order_by('order', 'id'))
        return context


class ObservableResponseViewSet(InstitutionScopedMixin, ContentWriteMixin,
                                mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin, GenericViewSet):
    """PATCH `{value}`: la respuesta a la pregunta inicial."""
    permission_classes = [IsAuthenticated, IsFlowInstitutionOwnerOrReviewer]
    queryset = ObservableResponse.objects.all().select_related(
        'survey__period', 'survey__general_package', 'axis_value__status',
        'status')
    serializer_class = ObservableResponseSerializer
    http_method_names = ['get', 'patch', 'head', 'options']

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == 'retrieve':
            return self._with_detail(qs)
        return qs

    @staticmethod
    def _with_detail(qs):
        return qs.select_related('observable__component').prefetch_related(
            'observable__aquestion_set', 'observable__bquestion_set',
            'observable__reachquestion_set__others_sectors',
            'observable__planquestion_set',
            'observable__specialquestion_set',
            group_responses_prefetch(), *FLOW_PREFETCH)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ObservableResponseFullSerializer
        return self.serializer_class

    def get_serializer_context(self) -> dict:
        context = super().get_serializer_context()
        context['main_sectors'] = list(
            Sector.objects.filter(is_main=True).order_by('order', 'id'))
        return context

    def update(self, request, *args, **kwargs):
        """Guarda `value` y aplica su efecto sobre el flujo (dominio).

        No pasa por `check_content_write`: el observable en
        `cp_not_present` no es editable por status, pero la vuelta a
        «Sí» debe poder salir de ahí. `answer.services` verifica turno,
        compuerta y revisión activa por sí mismo.
        """
        obj = self.get_object()
        if request.user.is_reviewer:
            raise PermissionDenied({
                'detail': 'La revisión no responde por la IES.',
                'code': 'reviewer_read_only'})
        check_capture_open(request.user, obj.survey)
        serializer = self.get_serializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if 'value' not in serializer.validated_data:
            return Response(
                {'detail': 'Falta `value`.'},
                status=status.HTTP_400_BAD_REQUEST)
        try:
            set_init_value(
                request.user, obj, serializer.validated_data['value'])
        except InitValueError as exc:
            errors = exc.args[0]
            return Response(
                {'detail': errors[0] if len(errors) == 1 else errors},
                status=status.HTTP_400_BAD_REQUEST)
        obj = self._with_detail(self.get_queryset()).get(pk=obj.pk)
        data = ObservableResponseFullSerializer(
            obj, context=self.get_serializer_context()).data
        data['axis_status'] = obj.axis_value.status_id
        return Response(data)


class GroupResponseViewSet(InstitutionScopedMixin, ContentWriteMixin,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin, GenericViewSet):
    """PATCH con las respuestas tipadas del grupo; la respuesta trae el
    grupo completo (con `completion`) más el status del observable y
    del eje ya propagados."""
    permission_classes = [IsAuthenticated, IsFlowInstitutionOwnerOrReviewer]
    survey_path = 'observable_response__survey'
    queryset = GroupResponse.objects.all().select_related(
        'observable_response__survey__period',
        'observable_response__survey__general_package',
        'observable_response__axis_value__status',
        'observable_response__observable', 'status', 'question_type',
    ).prefetch_related(
        'a_responses', 'b_responses', 'reach_responses__sectors',
        'plan_responses', 'special_responses', 'flow_attachments',
        *FLOW_PREFETCH)
    serializer_class = GroupResponseFullSerializer
    http_method_names = ['get', 'patch', 'head', 'options']

    def retrieve(self, request, *args, **kwargs):
        group = self.get_object()
        return Response(self._payload(group))

    def update(self, request, *args, **kwargs):
        group = self.get_object()
        self.check_content_write(group, group.observable_response.survey)
        serializer = self.get_serializer(
            group, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        assign_auto_status(request.user, group)
        group = self.get_queryset().get(pk=group.pk)
        return Response(self._payload(group))

    def _payload(self, group: GroupResponse) -> dict:
        data = self.get_serializer(group).data
        observable_response = group.observable_response
        data['observable_status'] = observable_response.status_id
        data['axis_status'] = observable_response.axis_value.status_id
        return data
