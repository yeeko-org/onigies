"""
Asignación automática del status inicial a los participantes del flujo.

Por qué una señal y no una vista/serializer: los participantes se crean
por rutas dispares y sin una vista única de creación —creación eager en
`Institution.save`, cascada en `GoodPractice.save`, y los endpoints de
captura del cuestionario que aún no existen en el rewrite—. Una señal
`post_save` es el único punto que cubre todas las rutas y garantiza el
invariante del que depende `validate_transition`: ningún participante
queda con `status=NULL` (validate_transition rechaza objetos sin status).

El status inicial es el default del grupo (`is_default=True`) resuelto
por el ContentType del objeto. No se crea `FlowEvent`: es el estado
inicial, no una transición, y no hay persona usuaria que lo ejecute
(mismo criterio que `Institution.save`, que fija `status_id` directo sin
evento). La promoción al status `auto_on_first_save` (`cp_filling`) sí es
una transición con persona usuaria: la ejecuta la vista de captura vía
`assign_auto_status`, no esta señal.
"""
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import Signal

from flow.registry import is_flow_participant

# Emitida por execute_transition tras una transición MANUAL (no por la
# propagación up/down). kwargs: user, obj, from_status, target, comment.
# La escucha flow.notifications para avisar a la IES por correo.
transition_executed = Signal()


def assign_default_status(sender, instance, created, **kwargs) -> None:
    """Asigna el default del grupo al crear un participante sin status."""
    if not created or instance.status_id is not None:
        return
    from flow.models import Status

    ct = ContentType.objects.get_for_model(sender)
    default = Status.objects.filter(
        is_default=True, applicable_models=ct).first()
    if default is None:
        return
    instance.status_id = default.name
    # update_fields evita reescribir el resto; created ya es False en la
    # reentrada de post_save, así que la guarda de arriba corta la
    # recursión.
    instance.save(update_fields=['status'])


def connect_flow_signals() -> None:
    """Conecta `assign_default_status` a cada modelo participante."""
    for model in apps.get_models():
        if not is_flow_participant(model):
            continue
        post_save.connect(
            assign_default_status,
            sender=model,
            dispatch_uid=f'flow_default_status_{model._meta.label}',
        )