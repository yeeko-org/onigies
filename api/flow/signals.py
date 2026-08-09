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

Aquí vive también el borrado del archivo físico de los adjuntos, por el
mismo motivo de ruta única: ver `delete_attachment_file`.
"""
import logging

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_delete, post_save
from django.dispatch import Signal

from flow.registry import is_flow_participant

logger = logging.getLogger(__name__)

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


def delete_attachment_file(sender, instance, **kwargs) -> None:
    """Borra el archivo del storage al borrarse el registro del adjunto.

    Va en `post_delete` y no en `Attachment.delete()` porque los targets
    declaran `GenericRelation`: al borrar el target, el colector de
    Django borra sus adjuntos por queryset y nunca pasa por el método
    del modelo. Registrar este receptor además desactiva el fast-delete
    del colector, así que la señal también llega en esa cascada.
    """
    if not instance.file:
        return
    try:
        instance.file.delete(save=False)
    except Exception:
        # El archivo puede faltar o el storage fallar (S3 intermitente,
        # datos migrados sin archivo): el registro ya se borró y la
        # petición no debe caer por un huérfano en disco.
        logger.warning(
            "No se pudo borrar el archivo del adjunto %s (%s)",
            instance.pk, instance.file.name, exc_info=True)


def connect_flow_signals() -> None:
    """Conecta las señales del flujo a sus modelos."""
    from flow.models import Attachment

    for model in apps.get_models():
        if not is_flow_participant(model):
            continue
        post_save.connect(
            assign_default_status,
            sender=model,
            dispatch_uid=f'flow_default_status_{model._meta.label}',
        )
    post_delete.connect(
        delete_attachment_file,
        sender=Attachment,
        dispatch_uid='flow_attachment_file_delete',
    )