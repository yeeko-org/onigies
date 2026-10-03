"""
Motor de transiciones del flujo de validación.

API pública:
- get_available_transitions(user, obj) → QuerySet[Status]
- validate_transition(user, obj, target, comment) → list[str]
- execute_transition(user, obj, target, comment) → FlowEvent
- admin_target_names(group) → list[str]
- validate_admin_transition(user, obj, target, comment) → list[str]
- execute_admin_transition(user, obj, target, comment) → FlowEvent
- assign_auto_status(user, obj) → FlowEvent | None
- assign_status_tree(user, obj, status) → list[FlowEvent]
"""
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import Q, QuerySet

from flow.models import FlowEvent, Status
from flow.registry import get_children, get_parent, is_flow_participant
from flow.signals import transition_executed


def get_user_flow_role(user) -> str | None:
    """'reviewer' para personal de revisión; 'ies' para institución."""
    if not user or not user.is_authenticated:
        return None
    return 'reviewer' if user.is_reviewer else 'ies'


def _ct(obj) -> ContentType:
    return ContentType.objects.get_for_model(obj)


def _save_status(obj) -> None:
    """Persiste el nuevo status con un `save()` completo, a propósito.

    Con `update_fields=['status']` se descartaba en silencio todo lo que
    el `save()` del modelo derivara del status —así se perdía `sent_at`
    en los paquetes bp y gen—. El motor no puede saber qué campos toca
    cada hook, así que guarda la fila entera y cualquier hook futuro
    funciona sin registrar nada aquí. Es seguro: en `execute_transition`
    la fila viene releída bajo `select_for_update()` y la propagación
    corre dentro de esa misma transacción.
    """
    obj.save()


def _check_children_rule(obj, target: Status) -> str | None:
    """
    Verifica que todos los hijos de obj estén en uno de los
    valid_child_statuses de target. Devuelve mensaje de error o None.
    """
    valid_ids = set(target.valid_child_statuses.values_list('name', flat=True))
    if not valid_ids:
        return None
    children = get_children(obj)
    if children is None:
        return None
    bad = children.exclude(status_id__in=valid_ids).count()
    if bad:
        return (
            f"{bad} elemento(s) aún no están en el status "
            "requerido para este cambio."
        )
    return None


def validate_transition(
    user,
    obj,
    target: Status,
    comment: str | None = None,
) -> list[str]:
    """
    Valida una transición sin ejecutarla.
    Devuelve lista de mensajes de error (vacía = válida).
    """
    errors: list[str] = []
    current: Status | None = obj.status

    if current is None:
        errors.append("El objeto no tiene status asignado.")
        return errors

    if not current.next_statuses.filter(name=target.name).exists():
        errors.append(
            f"La transición de '{current.public_name}' a "
            f"'{target.public_name}' no está permitida."
        )
        return errors

    ct = _ct(obj)
    if not target.applicable_models.filter(id=ct.id).exists():
        errors.append(
            f"'{target.public_name}' no aplica a este tipo de objeto."
        )

    required_role = current.role
    if required_role:
        user_role = get_user_flow_role(user)
        if user_role != required_role:
            role_label = {
                "reviewer": "las revisoras",
                "ies": "las instituciones",
            }.get(required_role, required_role)
            errors.append(
                f"Este cambio solo lo pueden ejecutar {role_label}."
            )

    child_error = _check_children_rule(obj, target)
    if child_error:
        errors.append(child_error)

    if target.comment_type == "required" and not (comment and comment.strip()):
        errors.append(
            f"El status '{target.public_name}' requiere un comentario."
        )

    # Gancho de reglas propias del modelo (duck typing): el motor se
    # mantiene genérico; cada participante puede vetar la transición sin
    # que flow conozca su dominio (p.ej. periodo cerrado en el envío bp).
    hook = getattr(obj, 'validate_flow_transition', None)
    if callable(hook):
        errors.extend(hook(user, target))

    return errors


@transaction.atomic
def execute_transition(
    user,
    obj,
    target: Status,
    comment: str | None = None,
) -> FlowEvent:
    """
    Valida y ejecuta una transición. Guarda el FlowEvent y actualiza
    obj.status. Si target.propagates_up, propaga al padre.

    Lanza ValueError con lista de errores si la transición no es válida.
    """
    # TOCTOU: la vista leyó `obj` sin lock. Re-obtenemos la fila con
    # select_for_update() dentro de la transacción para serializar
    # transiciones concurrentes (usamos type(obj) por el modelo dinámico
    # del GenericForeignKey).
    locked = type(obj).objects.select_for_update().get(pk=obj.pk)

    errors = validate_transition(user, locked, target, comment)
    if errors:
        raise ValueError(errors)
    return _apply_transition(user, obj, locked, target, comment)


def _apply_transition(user, obj, locked, target: Status,
                      comment: str | None) -> FlowEvent:
    """Efectos de una transición ya validada, compartidos por la normal y
    la válvula de admin: evento, status, propagación y señal."""
    from_status = locked.status
    event = FlowEvent.objects.create(
        content_type=_ct(locked),
        object_id=locked.pk,
        from_status=from_status,
        to_status=target,
        user=user,
        comment=comment or None,
    )
    locked.status = target
    _save_status(locked)

    if target.propagates_up:
        parent = get_parent(locked)
        if parent is not None:
            _propagate_up(user, parent, target)
    if target.propagates_down:
        _propagate_down(user, locked, target)

    # La instancia de la vista debe reflejar el nuevo status (se
    # reserializa tras el retorno).
    obj.status = locked.status

    # Notificaciones (flow.notifications): solo la transición manual, no
    # la propagación. El receptor programa el envío con on_commit.
    transition_executed.send(
        sender=type(locked), user=user, obj=locked,
        from_status=from_status, target=target, comment=comment,
    )
    return event


def admin_target_names(group: str) -> list[str]:
    """Destinos de la válvula de admin en un grupo (adr-0023): lo que la
    revisión establece —destinos de las transiciones que salen de un
    status de rol reviewer— más los propios status de rol reviewer, que
    sirven para deshacer y devolverle el turno a la revisión. Se deriva
    del grafo sembrado; ningún nombre va escrito aquí. Orden del
    catálogo (`group`, `order`).
    """
    reviewer = Status.objects.filter(group=group, role='reviewer')
    return list(
        Status.objects
        .filter(group=group)
        .filter(Q(role='reviewer') | Q(previous_statuses__in=reviewer))
        .distinct()
        .order_by('order', 'name')
        .values_list('name', flat=True)
    )


def is_admin_event(event: FlowEvent) -> bool:
    """True si el evento es un cambio administrativo (adr-0023): un
    cambio de status fuera de `from_status.next_statuses` que lleva
    comentario. No hay bandera en el evento; el comentario es lo que lo
    separa de las escrituras fuera del grafo de `assign_status_tree` y
    de las propagaciones, que nunca llevan uno. Espejo de
    `flowStore.isAdminEvent`.
    """
    if not (event.from_status_id and event.to_status_id and event.comment):
        return False
    return not event.from_status.next_statuses.filter(
        name=event.to_status_id).exists()


def validate_admin_transition(
    user,
    obj,
    target: Status,
    comment: str | None = None,
) -> list[str]:
    """Valida la válvula de admin (adr-0023) sin ejecutarla.

    Salta el rol del status propio y `next_statuses` —terminales
    incluidos— y rechaza los destinos legales, que van por el menú;
    conserva la regla de hijos, el comentario obligatorio y
    el gancho del modelo. El permiso `is_admin` lo resuelve la vista. Los
    `root_turn_errors` del gancho no pueden dispararse aquí: exigimos la
    raíz en rol reviewer antes de llamarlo.
    """
    from flow.permissions import resolve_flow_root

    current: Status | None = obj.status
    if current is None:
        return ["El objeto no tiene status asignado."]

    root = resolve_flow_root(obj)
    if root is obj:
        return ["El cambio administrativo solo aplica a elementos dentro "
                "de un envío, nunca al envío mismo."]
    root_status = getattr(root, 'status', None)
    if root_status is None or root_status.role != 'reviewer':
        return ["El cambio administrativo solo es posible mientras el "
                "envío esté del lado de la revisión."]

    if (target.group != current.group
            or target.name not in admin_target_names(current.group)):
        return [f"'{target.public_name}' no es un destino válido para un "
                "cambio administrativo."]
    if target.name == current.name:
        return [f"El objeto ya está en '{target.public_name}'."]
    # Un destino legal hecho por la válvula quedaría en el timeline como
    # transición normal (`is_admin_event` lo deriva de «fuera del grafo»).
    if current.next_statuses.filter(name=target.name).exists():
        return [f"'{target.public_name}' es una transición normal; usa el "
                "menú de estatus."]

    errors: list[str] = []
    if not target.applicable_models.filter(id=_ct(obj).id).exists():
        errors.append(
            f"'{target.public_name}' no aplica a este tipo de objeto.")

    child_error = _check_children_rule(obj, target)
    if child_error:
        errors.append(child_error)

    if not (comment and comment.strip()):
        errors.append("El cambio administrativo requiere un comentario.")

    hook = getattr(obj, 'validate_flow_transition', None)
    if callable(hook):
        errors.extend(hook(user, target))
    return errors


@transaction.atomic
def execute_admin_transition(
    user,
    obj,
    target: Status,
    comment: str | None = None,
) -> FlowEvent:
    """Válvula de admin (adr-0023): valida con
    `validate_admin_transition` y aplica los mismos efectos que
    `execute_transition`. Lanza ValueError con la lista de errores."""
    locked = type(obj).objects.select_for_update().get(pk=obj.pk)
    errors = validate_admin_transition(user, locked, target, comment)
    if errors:
        raise ValueError(errors)
    return _apply_transition(user, obj, locked, target, comment)


def _propagate_up(user, obj, status: Status) -> None:
    """
    Propaga status al padre sin pasar por validación manual.
    La propagación es automática: no requiere comentario ni rol.
    Se detiene si status no aplica al tipo del objeto, o si el objeto
    ya tiene ese status (evita bucles en auto-loops del seed).
    """
    ct = _ct(obj)
    if not status.applicable_models.filter(id=ct.id).exists():
        return
    if obj.status_id == status.name:
        return

    FlowEvent.objects.create(
        content_type=ct,
        object_id=obj.pk,
        from_status=obj.status,
        to_status=status,
        user=user,
    )
    obj.status = status
    _save_status(obj)

    if status.propagates_up:
        parent = get_parent(obj)
        if parent is not None:
            _propagate_up(user, parent, status)


def _propagate_down(user, parent, status: Status) -> None:
    """
    Propaga status a todos los descendientes de parent (recursivo) sin
    validación. Salta hijos donde status no aplica o que ya lo tienen
    (mismo criterio que _propagate_up). La jerarquía bp es de 2 niveles;
    ningún status cp/gen usa propagates_down, así que no recursar en un
    hijo ya en el status no deja nietos sin propagar en la práctica.
    """
    children = get_children(parent)
    if children is None:
        return
    for child in children:
        ct = _ct(child)
        if not status.applicable_models.filter(id=ct.id).exists():
            continue
        if child.status_id == status.name:
            continue
        FlowEvent.objects.create(
            content_type=ct,
            object_id=child.pk,
            from_status=child.status,
            to_status=status,
            user=user,
        )
        child.status = status
        _save_status(child)
        _propagate_down(user, child, status)


def get_available_transitions(user, obj) -> QuerySet:
    """
    Status a los que el usuario puede mover obj desde su status actual.
    Filtra por rol del usuario y aplicabilidad al tipo del objeto.
    """
    current: Status | None = obj.status
    if current is None or current.role is None:
        return Status.objects.none()
    if get_user_flow_role(user) != current.role:
        return Status.objects.none()
    ct = _ct(obj)
    return current.next_statuses.filter(applicable_models=ct)


def assign_auto_status(user, obj) -> FlowEvent | None:
    """
    Promueve el objeto al status `auto_on_first_save` de su grupo
    (p.ej. `cp_filling`) la primera vez que la IES guarda captura.

    La debe llamar la vista/serializer de captura con la persona usuaria
    que guarda. Solo actúa desde el estado de reposo inicial —sin status
    o en el default del grupo (`is_default`)— para no revertir objetos ya
    avanzados en el flujo. Devuelve el FlowEvent creado o None si no
    aplica (sin status auto para el tipo, o ya promovido/avanzado).
    """
    if not is_flow_participant(obj):
        return None
    ct = _ct(obj)
    auto = Status.objects.filter(
        auto_on_first_save=True,
        applicable_models=ct,
    ).first()
    if auto is None:
        return None

    current: Status | None = obj.status
    if current is not None and not current.is_default:
        return None
    if current is not None and current.name == auto.name:
        return None

    event = FlowEvent.objects.create(
        content_type=ct,
        object_id=obj.pk,
        from_status=current,
        to_status=auto,
        user=user,
    )
    obj.status = auto
    _save_status(obj)

    if auto.propagates_up:
        parent = get_parent(obj)
        if parent is not None:
            _propagate_up(user, parent, auto)

    return event

@transaction.atomic
def assign_status_tree(user, obj, status: Status,
                       comment: str | None = None) -> list[FlowEvent]:
    """
    Fija `status` en `obj` y en TODOS sus descendientes, sin validar
    rol, `next_statuses` ni regla de hijos, registrando un FlowEvent por
    cada objeto que cambia. No propaga hacia arriba ni emite
    `transition_executed`.

    Es la puerta del dominio, no del menú de transiciones: la usa
    `answer.services` cuando la respuesta a la pregunta inicial de un
    observable decide por sí sola el destino de sus grupos
    (`cp_not_present` y la vuelta a `cp_filling`). A diferencia de
    `_propagate_down`, recursa siempre —un hijo que ya tiene el status
    puede tener nietos que no—.
    """
    locked = type(obj).objects.select_for_update().get(pk=obj.pk)
    events: list[FlowEvent] = []
    _force_status(user, locked, status, comment, events)
    obj.status = locked.status
    return events


def _force_status(user, obj, status: Status, comment, events: list) -> None:
    ct = _ct(obj)
    if (status.applicable_models.filter(id=ct.id).exists()
            and obj.status_id != status.name):
        events.append(FlowEvent.objects.create(
            content_type=ct,
            object_id=obj.pk,
            from_status=obj.status,
            to_status=status,
            user=user,
            comment=comment or None,
        ))
        obj.status = status
        _save_status(obj)
    children = get_children(obj)
    if children is None:
        return
    for child in children.select_related('status'):
        _force_status(user, child, status, None, events)
