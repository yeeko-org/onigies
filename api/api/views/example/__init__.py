from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django_filters import FilterSet, CharFilter, NumberFilter
from api.views.action_file import ActionFileMixin
from api.views.common_views import BaseGenericViewSet
from api.views.example.serializers import GoodPracticeFullSerializer, GoodPracticeSerializer, EvidenceSerializer, \
    FeatureSerializer, FeatureFullSerializer, FeatureOptionSerializer, FeatureGoodPracticeSerializer, \
    GoodPracticePackageFullSerializer, GoodPracticePackageSerializer
from example.models import GoodPractice, Feature, FeatureOption, FeatureGoodPractice, GoodPracticePackage, Evidence


class GoodPracticeViewSet(BaseGenericViewSet, ActionFileMixin):

    queryset = GoodPractice.objects.all()
    serializer_class = GoodPracticeFullSerializer
    action_add_file_param = 'good_practice'
    disable_protection = True

    def get_serializer_class(self):
        action_serializer = {
            'list': GoodPracticeSerializer,
            'add_file': EvidenceSerializer,
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


class FeatureGoodPracticeViewSet(BaseGenericViewSet, ActionFileMixin):
    queryset = FeatureGoodPractice.objects.all()
    serializer_class = FeatureGoodPracticeSerializer
    action_add_file_param = 'feature_good_practice'

    def get_serializer_class(self):
        action_serializer = {
            'add_file': EvidenceSerializer,
        }
        return action_serializer.get(self.action, self.serializer_class)


class PackageFilter(FilterSet):

    institution = NumberFilter(field_name='survey__institution')
    period = NumberFilter(field_name='survey__period')

    class Meta:
        model = GoodPracticePackage
        fields = {}


class GoodPracticePackageViewSet(BaseGenericViewSet):
    queryset = GoodPracticePackage.objects.all()\
        .prefetch_related('good_practices')
    serializer_class = GoodPracticePackageFullSerializer
    search_fields = [
        'survey__institution__name', 'survey__institution__acronym']
    ordering_fields = [
        'id', 'survey__period__year', 'survey__institution__name']
    # filterset_fields = ['survey__institution', 'survey__period']
    filterset_class = PackageFilter

    def get_serializer_class(self):
        action_serializer = {
            'list': GoodPracticePackageSerializer,
        }
        return action_serializer.get(self.action, self.serializer_class)

    @action(detail=True, methods=['post'])
    def send(self, request, pk=None):
        """Envía el paquete de buenas prácticas a revisión.

        En el primer envío valida que todas las prácticas estén
        en status ``ready_to_send``. En re-envíos posteriores
        (cuando hubo ajustes) sólo transita el status del paquete
        y de sus prácticas no-finales.
        """
        from django.utils import timezone
        good_practice_package = self.get_object()
        has_sent = good_practice_package.sent_at is not None

        if not has_sent:
            practices = good_practice_package.good_practices.all()
            if not practices.exists():
                msg = ('Debes agregar al menos una buena práctica '
                       'antes de enviar el paquete.')
                return Response({'detail': msg}, status=400)
            pending = practices.exclude(status_sending_id='ready_to_send')
            if pending.exists():
                msg = ('Todas las buenas prácticas deben estar en '
                       '"Lista para enviar" antes de enviar el paquete.')
                return Response({'detail': msg,}, status=400)
        status_sending = "created" if not has_sent else "need_new_checking"
        good_practice_package.status_sending_id = status_sending
        if not has_sent:
            good_practice_package.sent_at = timezone.now()
        good_practice_package.save()
        pending_good_practices = good_practice_package.good_practices\
            .filter(status_sending__is_final=False)
        for good_practice in pending_good_practices:
            good_practice.status_sending_id = status_sending
            good_practice.save()
        serializer = self.get_serializer(good_practice_package)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def discard(self, request, pk=None):
        """Cierra el paquete con la respuesta "No tengo buenas prácticas".

        Sólo permitido si el estado actual pertenece al rol ``ies``
        (es decir, el paquete está bajo control de la institución) y si
        el periodo de buenas prácticas sigue abierto.
        """
        package = self.get_object()
        status = package.status_sending
        if not status or status.role != 'ies':
            msg = 'No puedes descartar el paquete en este estado.'
            return Response({'detail': msg}, status=400)
        if package.survey.period.good_practices_published:
            msg = 'El periodo ya cerró, no se puede modificar la respuesta.'
            return Response({'detail': msg}, status=400)
        package.has_good_practices = False
        package.status_sending_id = 'discarded'
        package.save()
        serializer = self.get_serializer(package)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def reopen(self, request, pk=None):
        """Reabre un paquete previamente descartado.

        Sólo permitido si el paquete está en estado ``discarded`` y si
        el periodo de buenas prácticas sigue abierto. Vuelve el paquete
        a estado ``draft`` con ``has_good_practices = None`` para que la
        institución pueda responder de nuevo.
        """
        package = self.get_object()
        if package.status_sending_id != 'discarded':
            msg = 'No se pueden reabrir paquetes que no estén "descartados".'
            return Response({'detail': msg}, status=400)
        if package.survey.period.good_practices_published:
            msg = 'El periodo de registro ya cerró, no se puede reabrir.'
            return Response({'detail': msg}, status=400)
        package.has_good_practices = None
        package.status_sending_id = 'draft'
        package.save()
        serializer = self.get_serializer(package)
        return Response(serializer.data)


class EvidenceViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Evidence.objects.all()
    serializer_class = EvidenceSerializer
