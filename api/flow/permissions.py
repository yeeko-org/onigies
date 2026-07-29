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


def resolve_flow_institution(obj):
    """Institución dueña de un objeto del flujo, o None si no se resuelve."""
    root = obj
    parent = get_parent(root)
    while parent is not None:
        root = parent
        parent = get_parent(root)
    survey = getattr(root, 'survey', None)
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


class IsFlowInstitutionOwnerOrReviewer(BasePermission):
    """Pertenencia institucional a nivel de objeto para los ViewSets de
    modelos participantes del flujo (p.ej. GoodPracticePackage).

    Las lecturas por lista se restringen en `get_queryset()` del ViewSet;
    aquí se cubre el acceso por objeto (retrieve y acciones detail).
    """

    def has_object_permission(self, request, view, obj) -> bool:
        return user_can_act_on_flow_object(request.user, obj)