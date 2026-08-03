"""
Notificaciones por correo cuando el flujo devuelve el turno a la IES.

Alcance (S5, docs/records/2026-07-03-auditoria-y-mejoras-del-flujo.md): solo se
notifica a la institución —a sus usuarios activos—, nunca a las
revisoras, y solo sobre los objetos raíz del flujo (GoodPracticePackage,
GeneralPackage, AxisValue). Las decisiones por hijo y los envíos a
revisión no generan correo.

Se dispara desde `flow.signals.transition_executed`, que emite
`execute_transition` únicamente en la transición manual (no en la
propagación): así se notifica solo el objeto que la persona transicionó,
no los hijos/padres propagados.
"""
import logging

from django.conf import settings
from django.db import transaction
from django.template.loader import render_to_string

from email_send.service import send_simple_email
from flow.registry import get_parent, is_flow_participant
from flow.signals import transition_executed

logger = logging.getLogger(__name__)

_TEMPLATE = 'email/flow_notification.html'
_GROUP_NOUN = {"bp": "Buenas prácticas", "gen": "Preguntas generales"}


def _should_notify(obj, from_status, target) -> bool:
    """
    True si esta transición debe notificar a la IES.

    Condiciones (todas sobre el objeto raíz): que el turno vuelva a la
    institución (`role` pasa a 'ies') o que llegue a un status final
    (`role=None`, sin transiciones siguientes).
    """
    if not is_flow_participant(obj) or get_parent(obj) is not None:
        return False  # solo raíces
    if target.role is None:
        return True  # status final
    return target.role == "ies" and (
        from_status is None or from_status.role != "ies")


def _recipients(obj) -> list[str]:
    """Correos de los usuarios activos de la institución del objeto."""
    institution = obj.survey.institution
    return list(
        institution.users
        .filter(is_active=True)
        .exclude(email="")
        .exclude(email__isnull=True)
        .values_list("email", flat=True)
    )


def _object_label(obj, group: str) -> str:
    """Etiqueta legible del objeto raíz para el cuerpo del correo."""
    if group == "cp":
        name = getattr(getattr(obj, "axis", None), "name", None)
        return f"el eje «{name}»" if name else "el eje en revisión"
    if group == "gen":
        return "tus preguntas generales"
    return "tus buenas prácticas"


def _subject(obj, target) -> str:
    if target.group == "cp":
        name = getattr(getattr(obj, "axis", None), "name", None)
        noun = f"Eje «{name}»" if name else "Eje"
    else:
        noun = _GROUP_NOUN.get(target.group, "Participación")
    return f"ONIGIES — {noun}: {target.public_name}"


def _build_context(obj, target, comment) -> dict:
    base = (settings.FRONTEND_SITE_URL or "").rstrip("/")
    return {
        "institution": obj.survey.institution,
        "object_label": _object_label(obj, target.group),
        "state": target.public_name,
        "guidance": target.hint,
        "comment": comment or None,
        "destination_url": f"{base}/respuestas/{obj.survey.period_id}",
        "cta_label": "Ir a mis respuestas",
    }


def on_transition_executed(
    sender, user, obj, from_status, target, comment=None, **kwargs
) -> None:
    """Receptor de `transition_executed`: programa el correo a la IES."""
    try:
        _schedule_notification(user, obj, from_status, target, comment)
    except Exception:
        # La notificación es best-effort: un fallo aquí (dentro de la
        # transacción de la transición) nunca debe revertir el cambio de
        # status ni romper la respuesta de la vista.
        logger.exception(
            "Fallo al programar la notificación de flujo para %s", obj)


def _schedule_notification(user, obj, from_status, target, comment) -> None:
    if not _should_notify(obj, from_status, target):
        return
    recipients = _recipients(obj)
    if not recipients:
        return

    subject = _subject(obj, target)
    context = _build_context(obj, target, comment)

    # Se envía tras el commit: si SMTP falla, la transición no se
    # revierte y no se notifica una transición que luego hizo rollback.
    def _send() -> None:
        try:
            html = render_to_string(_TEMPLATE, context)
        except Exception:
            logger.exception(
                "No se pudo renderizar la notificación de flujo para %s",
                obj,
            )
            return
        for email in recipients:
            send_simple_email(email, subject, html, user=user)

    transaction.on_commit(_send)


def connect_notification_signals() -> None:
    """Conecta el receptor de notificaciones (llamado en AppConfig.ready)."""
    transition_executed.connect(
        on_transition_executed,
        dispatch_uid="flow_transition_notification",
    )
