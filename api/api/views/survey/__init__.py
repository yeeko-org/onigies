"""ViewSets de la app survey: Survey y el paquete de generales (`gen`)."""
from django.db.models import Prefetch
from django_filters import FilterSet, NumberFilter
from rest_framework.permissions import IsAuthenticated

from api.permissions import IsInstitutionOwnerOrSuperuser
from api.views.common_views import BaseGenericViewSet
from api.views.survey.general_serializers import (
    GeneralPackageFullSerializer, GeneralPackageSerializer)
from api.views.survey.serializers import (
    SurveyFullSerializer, SurveyListSerializer, SurveySerializer)
from flow.permissions import IsFlowInstitutionOwnerOrReviewer
from survey.models import GeneralGroupResponse, GeneralPackage, Survey


def group_responses_prefetch(prefix: str = '') -> Prefetch:
    """Hijos del paquete gen con catálogo y timeline resueltos, en el
    orden del instrumento (`GeneralGroup.order`)."""
    queryset = GeneralGroupResponse.objects.select_related(
        'general_group').prefetch_related(
            'flow_events__user', 'flow_events__attachments').order_by(
                'general_group__order')
    return Prefetch(
        f'{prefix}general_group_responses', queryset=queryset)


def brief_group_responses_prefetch(prefix: str = '') -> Prefetch:
    """Variante mínima para listas: solo lo que necesita el conteo por
    status, sin catálogo ni timeline."""
    queryset = GeneralGroupResponse.objects.only(
        'id', 'status', 'general_package')
    return Prefetch(
        f'{prefix}general_group_responses', queryset=queryset)


class SurveyViewSet(BaseGenericViewSet):
    """Survey CRUD. Reads are scoped to the user's institution except
    for reviewers/staff/superusers, who read all. Writes (PATCH/PUT/
    DELETE) require ownership of the matching institution or
    superuser. POST is superuser-only.

    The PATCH carries the whole content of the `gen` section: the scalar
    columns, the `sectors` M2M and the nested `population_quantities`.
    """
    queryset = Survey.objects.all().select_related(
        'institution', 'period').prefetch_related(
            'population_quantities', 'sectors', 'instances')
    serializer_class = SurveySerializer
    permission_classes = [IsAuthenticated, IsInstitutionOwnerOrSuperuser]
    search_fields = ['institution__name', 'institution__acronym']
    ordering_fields = ['id', 'period__year', 'institution__name']
    ordering = ['-period__year', 'institution__name']
    filterset_fields = ['institution', 'period']

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_anonymous:
            return qs.none()
        if self.action == 'retrieve':
            qs = qs.select_related('general_package').prefetch_related(
                group_responses_prefetch('general_package__'),
                'general_package__flow_events__user',
                'general_package__flow_events__attachments')
        elif self.action == 'list':
            # El renglón colapsado solo pinta status y avance: dos
            # queries fijas para toda la página, no una por survey.
            qs = qs.select_related('general_package').prefetch_related(
                brief_group_responses_prefetch('general_package__'))
        if user.is_reviewer:
            return qs
        if user.institution_id:
            return qs.filter(institution_id=user.institution_id)
        return qs.none()

    def get_serializer_class(self):
        action_serializer = {
            'list': SurveyListSerializer,
            'retrieve': SurveyFullSerializer,
        }
        return action_serializer.get(self.action, self.serializer_class)


class GeneralPackageFilter(FilterSet):

    institution = NumberFilter(field_name='survey__institution')
    period = NumberFilter(field_name='survey__period')

    class Meta:
        model = GeneralPackage
        fields = {}


class GeneralPackageViewSet(BaseGenericViewSet):
    """Raíz del flujo `gen`. Espejo de GoodPracticePackageViewSet."""
    permission_classes = [
        IsAuthenticated, IsFlowInstitutionOwnerOrReviewer]
    queryset = GeneralPackage.objects.all().select_related(
        'survey__institution', 'survey__period').prefetch_related(
            group_responses_prefetch(),
            'flow_events__user', 'flow_events__attachments')
    serializer_class = GeneralPackageFullSerializer
    search_fields = [
        'survey__institution__name', 'survey__institution__acronym']
    ordering_fields = [
        'id', 'survey__period__year', 'survey__institution__name',
        'status__order', 'status__priority',
    ]
    # Orden por defecto: más urgentes primero (mayor priority del status).
    ordering = ['-status__priority', 'id']
    filterset_class = GeneralPackageFilter

    def get_queryset(self):
        """Las revisoras ven todos los paquetes; una IES solo los de su
        propia institución (evita fugas por lista)."""
        qs = super().get_queryset()
        user = self.request.user
        if user.is_anonymous:
            return qs.none()
        if user.is_reviewer:
            return qs
        if user.institution_id:
            return qs.filter(survey__institution_id=user.institution_id)
        return qs.none()

    def get_serializer_class(self):
        action_serializer = {
            'list': GeneralPackageSerializer,
        }
        return action_serializer.get(self.action, self.serializer_class)
