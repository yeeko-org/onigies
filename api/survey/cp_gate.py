"""
Compuerta de respuesta del cuestionario principal (flujo `cp`).

Dos condiciones, ambas del lado del servidor (task-153 y adr-0007): el
periodo abrió las respuestas (`Period.cp_open_at` ya pasó) y la
información base de la IES quedó validada (su `GeneralPackage` en
`gen_finished`, que exige los cinco grupos en `gen_approved`). Mientras
falte una, la IES VE el cuestionario pero no captura: ni respuestas, ni
el booleano inicial, ni transiciones, ni adjuntos. Las instituciones de
prueba ignoran la fecha, como ignoran los plazos del periodo, pero no
la base validada: sin denominadores congelados tampoco capturan. La
revisión nunca captura, así que la compuerta no le aplica a sus
transiciones.
"""
from rest_framework import status as http_status
from rest_framework.exceptions import APIException

CP_NOT_OPEN = 'cp_not_open'
GEN_NOT_APPROVED = 'gen_not_approved'

MESSAGES = {
    CP_NOT_OPEN: 'El cuestionario aún no está abierto a respuestas.',
    GEN_NOT_APPROVED: 'La información base de tu institución todavía no '
                      'está validada; hasta entonces no puedes responder '
                      'el cuestionario.',
}

# El paquete de generales nunca queda en gen_approved (ese status es de
# los grupos): el cierre de la sección es gen_finished.
GEN_VALIDATED_STATUS = 'gen_finished'


def capture_state(survey) -> dict:
    """`{open, reason, open_at}` para que el frontend inhabilite la
    captura y explique por qué. `reason` es la primera causa que aplica,
    en el orden en que se destraban (primero la fecha, luego gen).
    `open_at` viaja tal cual aunque la IES de prueba no lo espere."""
    period = survey.period
    open_at = period.cp_open_at
    reason = None
    if not period.is_cp_open and not survey.is_test:
        reason = CP_NOT_OPEN
    else:
        package = getattr(survey, 'general_package', None)
        if package is None or package.status_id != GEN_VALIDATED_STATUS:
            reason = GEN_NOT_APPROVED
    return {
        'open': reason is None,
        'reason': reason,
        'open_at': open_at.isoformat() if open_at else None,
    }


def capture_lock_errors(user, survey) -> list[str]:
    """Mensajes del candado para una persona de la IES; vacío para la
    revisión (no captura) y con la compuerta abierta."""
    if user is not None and getattr(user, 'is_reviewer', False):
        return []
    state = capture_state(survey)
    if state['open']:
        return []
    return [MESSAGES[state['reason']]]


class CaptureClosed(APIException):
    """403 con `code` distinguible (`cp_not_open` / `gen_not_approved`)."""
    status_code = http_status.HTTP_403_FORBIDDEN

    def __init__(self, reason: str):
        super().__init__({'detail': MESSAGES[reason], 'code': reason})


def check_capture_open(user, survey) -> None:
    """Lanza `CaptureClosed` si la IES no puede capturar hoy."""
    if user is not None and getattr(user, 'is_reviewer', False):
        return
    state = capture_state(survey)
    if not state['open']:
        raise CaptureClosed(state['reason'])
