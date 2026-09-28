from django.db.models import ProtectedError, RestrictedError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler, set_rollback

DELETE_BLOCKED_MSG = (
    "No se puede eliminar: hay registros que dependen de este elemento "
    "({})."
)


def _blocking_models(exc) -> str:
    if isinstance(exc, ProtectedError):
        objects = exc.protected_objects
    else:
        objects = exc.restricted_objects
    names = {str(obj._meta.verbose_name_plural) for obj in objects}
    return ", ".join(sorted(names))


def api_exception_handler(exc, context):
    """DRF's handler, plus a 409 for deletes blocked by PROTECT/RESTRICT.

    Covers every delete path at once (`confirm-delete`, plain ModelViewSet
    destroys, APIViews) instead of a try/except per view; the Collector
    raises before any row is deleted, so nothing is left half-done.
    """
    if isinstance(exc, (ProtectedError, RestrictedError)):
        set_rollback()
        detail = DELETE_BLOCKED_MSG.format(_blocking_models(exc))
        return Response({"detail": detail}, status=status.HTTP_409_CONFLICT)
    return exception_handler(exc, context)
