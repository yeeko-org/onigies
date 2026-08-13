from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters import FilterSet, NumberFilter
from api.views.common_views import BaseGenericViewSet
from flow.permissions import IsFlowInstitutionOwnerOrReviewer
from api.views.example.serializers import GoodPracticeFullSerializer, GoodPracticeSerializer, \
    FeatureSerializer, FeatureFullSerializer, FeatureOptionSerializer, FeatureGoodPracticeSerializer, \
    GoodPracticePackageFullSerializer, GoodPracticePackageSerializer
from example.models import GoodPractice, Feature, FeatureOption, FeatureGoodPractice, GoodPracticePackage
from flow.models import Status
from flow.services import execute_transition


class GoodPracticeViewSet(BaseGenericViewSet):

    queryset = GoodPractice.objects.all().prefetch_related(
        'flow_events__user', 'flow_events__attachments',
        'flow_attachments', 'feature_values__flow_attachments')
    serializer_class = GoodPracticeFullSerializer
    disable_protection = True

    def get_serializer_class(self):
        action_serializer = {
            'list': GoodPracticeSerializer,
        }
        return action_serializer.get(self.action, self.serializer_class)


class FeatureViewSet(BaseGenericViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer

    def get_serializer_class(self):
        # print("FeatureViewSet.get_serializer_class, action: ", self.action)
        action_serializer = {
            'retrieve': FeatureFullSerializer,
            'create': FeatureFullSerializer,
            'update': FeatureFullSerializer,
        }
        return action_serializer.get(self.action, self.serializer_class)


class FeatureOptionViewSet(BaseGenericViewSet):
    queryset = FeatureOption.objects.all()
    serializer_class = FeatureOptionSerializer


class FeatureGoodPracticeViewSet(BaseGenericViewSet):
    queryset = FeatureGoodPractice.objects.all().prefetch_related(
        'flow_attachments')
    serializer_class = FeatureGoodPracticeSerializer


class PackageFilter(FilterSet):

    institution = NumberFilter(field_name='survey__institution')
    period = NumberFilter(field_name='survey__period')

    class Meta:
        model = GoodPracticePackage
        fields = {}


class GoodPracticePackageViewSet(BaseGenericViewSet):
    permission_classes = [
        IsAuthenticated, IsFlowInstitutionOwnerOrReviewer]
    queryset = GoodPracticePackage.objects.all().prefetch_related(
        'good_practices',
        'flow_events__user', 'flow_events__attachments',
        'good_practices__flow_events__user',
        'good_practices__flow_events__attachments',
        'good_practices__flow_attachments',
        'good_practices__feature_values__flow_attachments')
    serializer_class = GoodPracticePackageFullSerializer
    search_fields = [
        'survey__institution__name', 'survey__institution__acronym']
    ordering_fields = [
        'id', 'survey__period__year', 'survey__institution__name',
        'status__order', 'status__priority'
    ]
    # Orden por defecto: más urgentes primero (mayor priority del status).
    ordering = ['-status__priority', 'id']
    # filterset_fields = ['survey__institution', 'survey__period']
    filterset_class = PackageFilter

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
            'list': GoodPracticePackageSerializer,
        }
        return action_serializer.get(self.action, self.serializer_class)

    # El envío a revisión lo ejecuta ahora el motor de flujo
    # (POST /flow/example/goodpracticepackage/{pk}/transitions/ con
    # bp_sent / bp_resent). La acción `send` vieja se jubiló: el front
    # llama al motor y `sent_at` lo fija el hook de GoodPracticePackage.save.

    @action(detail=True, methods=['post'])
    def discard(self, request, pk=None):
        """Cierra el módulo con la respuesta "No tengo buenas prácticas".

        Es una transición validada ``→ bp_discarded``: el motor verifica
        turno, ``next_statuses`` y ``valid_child_statuses`` (no se puede
        descartar si las prácticas no están en un status compatible) y
        propaga el descarte a las prácticas (``propagates_down``).
        """
        package = self.get_object()
        closed = package.survey.period.is_bp_submission_closed
        if closed and not package.survey.is_test:
            msg = 'El periodo ya cerró, no se puede modificar la respuesta.'
            return Response({'detail': msg}, status=400)
        try:
            execute_transition(
                request.user, package, Status.objects.get(name='bp_discarded'))
        except ValueError as exc:
            errors = exc.args[0]
            return Response(
                {'detail': errors[0] if len(errors) == 1 else errors},
                status=400)
        package.has_good_practices = False
        package.save(update_fields=['has_good_practices'])
        serializer = self.get_serializer(package)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def reopen(self, request, pk=None):
        """Reabre el módulo para que la IES vuelva a elegir respuesta.

        "Cambiar respuesta" llama aquí en ambos casos:
        - Desde "No" (``bp_discarded``): transición validada
          ``→ bp_draft`` (con ``valid_child_statuses``) que propaga a las
          prácticas.
        - Desde "Sí" (ya en ``bp_draft``): no hay cambio de status que
          revertir; solo se reabre la pregunta (``has_good_practices =
          None``) sin tocar el status ni las prácticas.
        """
        package = self.get_object()
        status = package.status
        if not status or status.role != 'ies':
            msg = 'No puedes reabrir el paquete en este estado.'
            return Response({'detail': msg}, status=400)
        closed = package.survey.period.is_bp_submission_closed
        if closed and not package.survey.is_test:
            msg = 'El periodo de registro ya cerró, no se puede reabrir.'
            return Response({'detail': msg}, status=400)
        if status.name != 'bp_draft':
            try:
                execute_transition(
                    request.user, package, Status.objects.get(name='bp_draft'))
            except ValueError as exc:
                errors = exc.args[0]
                return Response(
                    {'detail': errors[0] if len(errors) == 1 else errors},
                    status=400)
        package.has_good_practices = None
        package.save(update_fields=['has_good_practices'])
        serializer = self.get_serializer(package)
        return Response(serializer.data)
