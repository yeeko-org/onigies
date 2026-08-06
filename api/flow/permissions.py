"""
Control de pertenencia institucional para el motor de flujo.

Los seis modelos participantes cuelgan siempre de una institución a
través de la raíz de su jerarquía (GoodPracticePackage, AxisValue o
GeneralPackage), y las tres raíces tienen un FK `survey` cuyo
`institution` es la dueña. Subimos por el registry hasta la raíz y de
ahí resolvemos la institución.

Regla: las personas revisoras (is_reviewer) pueden actuar sobre
cualquier objeto; las personas de una IES solo sobre objetos de su
propia institución.
"""
from rest_framework.permissions import BasePermission

from flow.registry import get_parent


def resolve_flow_root(obj):
    """Raíz de la jerarquía del objeto (el paquete o el AxisValue)."""
    root = obj
    parent = get_parent(root)
    while parent is not None:
        root = parent
        parent = get_parent(root)
    return root


def resolve_flow_institution(obj):
    """Institución dueña de un objeto del flujo, o None si no se resuelve."""
    survey = getattr(resolve_flow_root(obj), 'survey', None)
    if survey is None:
        return None
    return getattr(survey, 'institution', None)


def user_can_act_on_flow_object(user, obj) -> bool:
    """True si la persona usuaria puede actuar sobre el objeto del flujo."""
    if not user or not user.is_authenticated:
        return False
    if user.is_reviewer:
        return True
    institution = resolve_flow_institution(obj)
    if institution is None:
        return False
    return user.institution_id == institution.pk


def user_can_edit_flow_content(user, obj) -> bool:
    """True si la persona usuaria puede editar HOY el contenido del objeto.

    Espejo servidor de `flowStore.canEditContent`: el status propio debe
    ser `content_editable` y el turno lo manda la RAÍZ de la jerarquía
    (una vez enviado el paquete, ningún descendiente es editable aunque
    su propio status siga siendo de la IES).
    """
    from flow.services import get_user_flow_role

    if not user_can_act_on_flow_object(user, obj):
        return False
    own_status = getattr(obj, 'status', None)
    if own_status is None or not own_status.content_editable:
        return False
    root_status = getattr(resolve_flow_root(obj), 'status', None)
    if root_status is None:
        return False
    return root_status.role == get_user_flow_role(user)


class IsFlowInstitutionOwnerOrReviewer(BasePermission):
    """Pertenencia institucional a nivel de objeto para los ViewSets de
    modelos participantes del flujo (p.ej. GoodPracticePackage).

    Las lecturas por lista se restringen en `get_queryset()` del ViewSet;
    aquí se cubre el acceso por objeto (retrieve y acciones detail).
    """

    def has_object_permission(self, request, view, obj) -> bool:
        return user_can_act_on_flow_object(request.user, obj)