"""
Topología padre-hijo del flujo.

Cada modelo participante hereda `FlowParticipant` y declara su FK al
padre en `flow_parent` (None si es raíz).

Jerarquías (todas FK reales):
    bp:   GoodPracticePackage → GoodPractice
    cp:   AxisValue → ObservableResponse → GroupResponse
    gen:  GeneralPackage → GeneralGroupResponse

ComponentValue no participa del flujo (solo guarda valores de
resultado).
"""
from functools import cache

from django.apps import apps
from django.db import models


class FlowParticipant:
    """
    Marca un modelo como participante del flujo.

    `flow_parent`: nombre del campo FK que apunta al padre lógico, o None
    si el modelo es raíz. Mixin sin campos: no genera migraciones.
    """
    flow_parent: str | None = None


def is_flow_participant(obj_or_model) -> bool:
    """True si el modelo (instancia o clase) participa del flujo."""
    model = obj_or_model if isinstance(obj_or_model, type) \
        else type(obj_or_model)
    return issubclass(model, FlowParticipant)


def get_parent(obj: models.Model) -> models.Model | None:
    """Padre lógico de un objeto del flujo, o None si es raíz."""
    parent_attr = getattr(obj, 'flow_parent', None)
    if parent_attr is None:
        return None
    return getattr(obj, parent_attr)


def get_children(obj: models.Model) -> models.QuerySet | None:
    """Hijos lógicos de un objeto del flujo, o None si es hoja."""
    accessor = _children_accessor(type(obj))
    if accessor is None:
        return None
    return getattr(obj, accessor).all()


@cache
def _children_accessor(parent_model: type) -> str | None:
    """
    related_name inverso del modelo hijo cuyo `flow_parent` apunta a
    parent_model, o None si parent_model es hoja.

    Cada padre del flujo tiene un único tipo de hijo (bp/cp/gen son
    cadenas lineales), así que el primer match es el único. Cacheado:
    la topología no cambia en runtime.
    """
    for child in apps.get_models():
        parent_attr = getattr(child, 'flow_parent', None)
        if parent_attr is None:          # no participa, o es raíz
            continue
        fk = child._meta.get_field(parent_attr)
        if fk.related_model is parent_model:
            return fk.remote_field.get_accessor_name()
    return None