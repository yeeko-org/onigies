"""
Reglas de dominio de la captura del cuestionario principal (`cp`).

La pregunta inicial de cada observable («¿cuenta con la medida?») decide
sola el destino de sus grupos: un «No» vale cero, es terminal y no se
revisa (`cp_not_present`); volver a «Sí» reabre la captura
(`cp_filling`). Ninguna de las dos es una transición del menú: las
ejecuta este módulo a través de `flow.services.assign_status_tree`.
"""
from django.db import transaction

from flow.models import Status
from flow.permissions import user_can_act_on_flow_object
from flow.services import (
    assign_auto_status, assign_status_tree, get_user_flow_role)
from survey.cp_gate import capture_lock_errors

NOT_PRESENT = 'cp_not_present'
FILLING = 'cp_filling'

# Un grupo en cualquiera de estos status ya pasó por la revisión o la
# está esperando: negar la medida borraría ese trabajo de una vez.
REVIEW_ACTIVE_STATUSES = frozenset({
    'cp_need_changes', 'cp_in_adjustment', 'cp_adjusted', 'cp_approved',
    'cp_partial', 'cp_partial_approved',
})

REVIEW_ACTIVE_MESSAGE = (
    'No puedes indicar que no cuentas con la medida: {count} de sus '
    'bloques ya están en revisión o revisados. Si necesitas cambiar la '
    'respuesta, solicita un reajuste del eje.')
NOT_IES_TURN_MESSAGE = (
    'El eje no está en turno de tu institución; no puedes cambiar la '
    'respuesta inicial ahora.')


class InitValueError(ValueError):
    """La respuesta inicial no se puede cambiar; `args[0]` es la lista
    de razones (mismo contrato que el motor)."""


def init_value_errors(user, observable_response, value) -> list[str]:
    """Por qué la persona usuaria no puede fijar `value` hoy."""
    if not user_can_act_on_flow_object(user, observable_response):
        return ['No tienes acceso a este observable.']
    if get_user_flow_role(user) != 'ies':
        return ['Solo la institución responde la pregunta inicial.']
    errors = capture_lock_errors(user, observable_response.survey)
    if errors:
        return errors
    axis_status = observable_response.axis_value.status
    if axis_status is None or axis_status.role != 'ies':
        return [NOT_IES_TURN_MESSAGE]
    if value is False and observable_response.value is not False:
        count = observable_response.statuses.filter(
            status_id__in=REVIEW_ACTIVE_STATUSES).count()
        if count:
            return [REVIEW_ACTIVE_MESSAGE.format(count=count)]
    return []


@transaction.atomic
def set_init_value(user, observable_response, value) -> list:
    """Guarda la respuesta a la pregunta inicial y mueve el árbol.

    - `False`: observable y todos sus grupos a `cp_not_present`; las
      respuestas tipadas capturadas se conservan por si la IES se
      arrepiente.
    - Salir de `False` (a `True` o a nulo): de vuelta a `cp_filling`.
    - `True` por primera vez: el observable arranca la captura
      (`assign_auto_status`, que sube al eje).

    El eje solo se promueve desde su reposo (`cp_pre_start`): un eje en
    corrección no cambia de status por esta vía.
    Devuelve los FlowEvent generados. Lanza `InitValueError`.
    """
    errors = init_value_errors(user, observable_response, value)
    if errors:
        raise InitValueError(errors)

    previous = observable_response.value
    observable_response.value = value
    observable_response.save(update_fields=['value'])
    events: list = []

    if value is False:
        if previous is not False:
            events += assign_status_tree(
                user, observable_response,
                Status.objects.get(name=NOT_PRESENT))
    elif previous is False:
        events += assign_status_tree(
            user, observable_response, Status.objects.get(name=FILLING))
    elif value is True:
        event = assign_auto_status(user, observable_response)
        if event is not None:
            events.append(event)

    event = assign_auto_status(user, observable_response.axis_value)
    if event is not None:
        events.append(event)
    return events
