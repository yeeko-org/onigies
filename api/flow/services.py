"""
Motor de transiciones del flujo de validación.

API pública:
- get_available_transitions(user, obj) → QuerySet[Status]
- validate_transition(user, obj, target, comment) → list[str]
- execute_transition(user, obj, target, comment) → FlowEvent
- assign_auto_status(user, obj) → FlowEvent | None
"""
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import QuerySet

from flow.models import FlowEvent, Status
from flow.registry import get_children, get_parent, node_for


def get_user_flow_role(user) -> str | None:
    """'reviewer' para personal de revisión; 'ies' para institución."""
    if not user or not user.is_authenticated:
        return None
    return 'reviewer' if user.is_reviewer else 'ies'


def _ct(obj) -> ContentType:
    return ContentType.objects.get_for_model(obj)


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

    if target.requires_comment and not (comment and comment.strip()):
        errors.append(
            f"El status '{target.public_name}' requiere un comentario."
        )

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
    errors = validate_transition(user, obj, target, comment)
    if errors:
        raise ValueError(errors)

    event = FlowEvent.objects.create(
        content_type=_ct(obj),
        object_id=obj.pk,
        from_status=obj.status,
        to_status=target,
        user=user,
        comment=comment or None,
    )
    obj.status = target
    obj.save(update_fields=['status'])

    if target.propagates_up:
        parent = get_parent(obj)
        if parent is not None:
            _propagate_up(user, parent, target)
    if target.propagates_down:
        _propagate_down(user, obj, target)

    return event


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
    obj.save(update_fields=['status'])

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
        child.save(update_fields=['status'])
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
    Asigna el status auto_on_first_save cuando el objeto no tiene status.
    Llama desde la vista al guardar datos por primera vez.
    Devuelve el FlowEvent creado o None si no aplica.
    """
    if obj.status is not None:
        return None
    node = node_for(obj)
    if node is None:
        return None
    ct = _ct(obj)
    auto = Status.objects.filter(
        group=node.group,
        auto_on_first_save=True,
        applicable_models=ct,
    ).first()
    if auto is None:
        return None

    event = FlowEvent.objects.create(
        content_type=ct,
        object_id=obj.pk,
        from_status=None,
        to_status=auto,
        user=user,
    )
    obj.status = auto
    obj.save(update_fields=['status'])

    if auto.propagates_up:
        parent = get_parent(obj)
        if parent is not None:
            _propagate_up(user, parent, auto)

    return event