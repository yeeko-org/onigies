"""Compuerta de edición del cuestionario (`QuestionnaireSettings`)."""
from rest_framework.exceptions import PermissionDenied

from question.models import QuestionnaireSettings

CLOSED_MESSAGE = (
    "El cuestionario está cerrado a edición: solo se pueden modificar "
    "textos y ponderaciones.")

# DELETE también cubre la acción `confirm-delete` de CustomDeleteMixin.
GATED_METHODS = ('POST', 'DELETE')


class ContentGateMixin:
    """La compuerta va en `initial` y no en `http_method_names`: ese
    atributo se lee al construir la vista, una sola vez por proceso, y
    el interruptor cambia en caliente."""

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        if request.method in GATED_METHODS \
                and not QuestionnaireSettings.is_open():
            raise PermissionDenied(CLOSED_MESSAGE)


class SingleRowMixin:
    """Colección de una sola fila: ni se crea ni se borra."""

    http_method_names = ['get', 'put', 'patch', 'head', 'options']
