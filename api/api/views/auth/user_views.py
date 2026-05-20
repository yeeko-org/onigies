"""Endpoints para gestión de personas usuarias staff/revisoras.

Pensado para el panel de la superusuaria. No incluye creación (esa
va por el flujo de invitación) ni eliminación (se desactiva
alternando `is_active`).
"""

from api.mixins import MultiSerializerListRetrieveUpdateMix
from api.permissions import IsSuperuser
from api.views.auth.serializers import (
    UserListSerializer,
    UserPermissionsUpdateSerializer,
)
from ies.models import User


class UserViewSet(MultiSerializerListRetrieveUpdateMix):
    """list, retrieve y partial_update sobre personas sin institución.

    Solo accesible por superusuarias. No expone PUT: para edición
    parcial se usa PATCH.
    """

    http_method_names = ['get', 'patch', 'head', 'options']
    queryset = User.objects.filter(
        institution__isnull=True).order_by('-date_joined')
    permission_classes = [IsSuperuser]
    serializer_class = UserListSerializer
    action_serializers = {
        'list': UserListSerializer,
        'retrieve': UserListSerializer,
        'partial_update': UserPermissionsUpdateSerializer,
    }