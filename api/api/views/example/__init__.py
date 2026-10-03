from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters import FilterSet, NumberFilter
from api.views.common_views import BaseGenericViewSet
from api.views.answer import InstitutionScopedMixin
from flow.permissions import (
    IsFlowInstitutionOwnerOrReviewer, content_lock_errors,
    resolve_flow_root, user_can_act_on_flow_object,
    user_can_edit_flow_content)
from flow.registry import resolve_flow_owner
from api.views.example.serializers import GoodPracticeFullSerializer, GoodPracticeSerializer, \
    FeatureSerializer, FeatureFullSerializer, FeatureOptionSerializer, FeatureGoodPracticeSerializer, \
    GoodPracticePackageFullSerializer, GoodPracticePackageSerializer
from example.models import GoodPractice, Feature, FeatureOption, FeatureGoodPractice, GoodPracticePackage
from flow.models import Status
from flow.services import execute_transition


class PracticeContentWriteMixin:
    """La IES escribe el contenido de bp solo cuando la práctica es
    editable hoy (`user_can_edit_flow_content`: status propio editable y
    el envío en su turno); los criterios delegan en su práctica
    (`flow_delegate`).

    Hermano de `ContentWriteMixin` del cuestionario, que no se reusa: allá
    la revisión no escribe nada y manda la compuerta de respuesta de cp;
    aquí la revisión califica (los campos de revisión los filtra el
    serializer) y queda exenta del candado de contenido.

    El admin (`is_admin`) queda fuera de las tres reglas de la revisión:
    crea, borra y escribe contenido sin candado de turno.
    """
    not_editable_message = (
        'No puedes modificar esta buena práctica en su estado actual.')

    def check_content_write(self, obj) -> None:
        user = self.request.user
        if user.is_reviewer:
            return
        owner = resolve_flow_owner(obj)
        if user_can_edit_flow_content(user, owner):
            return
        errors = content_lock_errors(user, resolve_flow_root(owner))
        detail = errors[0] if len(errors) == 1 else (
            errors or self.not_editable_message)
        raise PermissionDenied({'detail': detail, 'code': 'not_editable'})

    def perform_update(self, serializer):
        self.check_content_write(serializer.instance)
        super().perform_update(serializer)

    def check_delete(self, obj) -> None:
        # La revisión está exenta del candado de contenido para calificar,
        # pero borrar no es calificar.
        user = self.request.user
        if user.is_reviewer and not user.is_admin:
            raise PermissionDenied(
                'La revisión no elimina buenas prácticas ni criterios; '
                'solo los califica.')
        self.check_content_write(obj)

    def perform_destroy(self, instance):
        self.check_delete(instance)
        super().perform_destroy(instance)

    @action(detail=True, methods=['delete'], url_path='confirm-delete')
    def confirm_delete(self, request, pk=None):
        # La acción de CustomDeleteMixin borra sin pasar por
        # perform_destroy; sin esto sería la puerta trasera del candado.
        self.check_delete(self.get_object())
        return super().confirm_delete(request, pk=pk)


class GoodPracticeViewSet(InstitutionScopedMixin, PracticeContentWriteMixin,
                          BaseGenericViewSet):
    permission_classes = [IsAuthenticated, IsFlowInstitutionOwnerOrReviewer]
    survey_path = 'package__survey'
    queryset = GoodPractice.objects.all().prefetch_related(
        'flow_events__user', 'flow_events__attachments',
        'flow_attachments', 'feature_values__flow_attachments')
    serializer_class = GoodPracticeFullSerializer
    # Cada práctica nace con sus criterios (GoodPractice.save), así que el
    # borrado protegido siempre respondería 400 con el reporte de
    # relacionados; la IES borra la práctica con sus criterios en cascada.
    disable_protection = True

    def _check_package(self, serializer) -> None:
        """El paquete viene en el cuerpo: sin esto una IES crearía o
        movería una práctica al envío de otra institución, o a un envío
        que ya no está en su turno de edición."""
        user = self.request.user
        package = serializer.validated_data.get('package')
        if package is None:
            return
        if not user_can_act_on_flow_object(user, package):
            raise PermissionDenied(
                'Solo puedes registrar prácticas en el envío de tu '
                'institución.')
        # Una práctica nueva nace en el default del grupo, que es de la
        # IES aun con el envío descartado; por eso se mira el envío.
        if not user.is_reviewer and not user_can_edit_flow_content(
                user, package):
            raise PermissionDenied({
                'detail': 'El envío no está en tu turno de edición; no '
                          'puedes agregarle buenas prácticas.',
                'code': 'not_editable'})

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_reviewer and not user.is_admin:
            raise PermissionDenied(
                'La revisión no registra buenas prácticas; solo califica '
                'las de la institución.')
        self._check_package(serializer)
        serializer.save()

    def perform_update(self, serializer):
        package = serializer.validated_data.get('package')
        if package is not None and package != serializer.instance.package:
            self._check_package(serializer)
        super().perform_update(serializer)

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


class FeatureGoodPracticeViewSet(InstitutionScopedMixin,
                                 PracticeContentWriteMixin,
                                 BaseGenericViewSet):
    permission_classes = [IsAuthenticated, IsFlowInstitutionOwnerOrReviewer]
    survey_path = 'good_practice__package__survey'
    queryset = FeatureGoodPractice.objects.all().prefetch_related(
        'flow_attachments')
    serializer_class = FeatureGoodPracticeSerializer

    def perform_create(self, serializer):
        """Los criterios nacen con la práctica (GoodPractice.save); el
        alta suelta solo cubre el respaldo de `FeatureList` para un
        criterio agregado al catálogo después. Solo la IES (sobre una
        práctica de su institución) o el admin."""
        user = self.request.user
        # A la revisión el serializer ya le descartó `good_practice`.
        good_practice = serializer.validated_data.get('good_practice')
        reviewer_only = user.is_reviewer and not user.is_admin
        if reviewer_only or not user_can_act_on_flow_object(
                user, good_practice):
            raise PermissionDenied(
                'Solo la institución dueña de la práctica puede agregarle '
                'criterios.')
        self.check_content_write(good_practice)
        serializer.save()


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
