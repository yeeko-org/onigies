"""
Topología del flujo: qué modelos participan, a qué grupo pertenecen y
cómo se resuelven padre e hijos.

Vive en código (no en BD) porque es estructural — no configuración — y
porque el vínculo AxisValue ↔ ObservableResponse no tiene FK: el padre
de un ObservableResponse es el AxisValue del mismo survey cuyo axis es
el del componente del observable.

ComponentValue no participa del flujo (solo guarda valores de
resultado).

Los modelos se referencian por label "app.modelname" (minúsculas, como
ContentType) y se resuelven con apps.get_model para evitar imports
circulares con answer / survey / example.
"""
from dataclasses import dataclass

from django.apps import apps
from django.db import models


@dataclass(frozen=True)
class FlowNode:
    """Configuración de un modelo participante del flujo."""
    group: str                        # bp / cp / gen
    parent_attr: str | None = None    # FK directo al padre, si existe
    children_attr: str | None = None  # related_name de los hijos


FLOW_MODELS: dict[str, FlowNode] = {
    "example.goodpracticepackage": FlowNode(
        group="bp", children_attr="good_practices"),
    "example.goodpractice": FlowNode(group="bp", parent_attr="package"),
    # AxisValue ↔ ObservableResponse no tienen FK entre sí: sus
    # accessors especiales están en get_parent / get_children.
    "survey.axisvalue": FlowNode(group="cp"),
    "answer.observableresponse": FlowNode(
        group="cp", children_attr="statuses"),
    "answer.groupresponse": FlowNode(
        group="cp", parent_attr="observable_response"),
    "survey.generalgroupresponse": FlowNode(group="gen"),
}


def model_label(obj_or_model) -> str:
    """Label "app.modelname" de una instancia o clase de modelo."""
    meta = obj_or_model._meta
    return f"{meta.app_label}.{meta.model_name}"


def node_for(obj_or_model) -> FlowNode | None:
    """FlowNode de un modelo participante, o None si no participa."""
    return FLOW_MODELS.get(model_label(obj_or_model))


def get_parent(obj: models.Model) -> models.Model | None:
    """Padre lógico de un objeto del flujo, o None si es raíz."""
    label = model_label(obj)
    if label == "answer.observableresponse":
        axis_value_cls = apps.get_model("survey", "AxisValue")
        return axis_value_cls.objects.filter(
            survey_id=obj.survey_id,
            axis_id=obj.observable.component.axis_id).first()
    node = FLOW_MODELS.get(label)
    if node and node.parent_attr:
        return getattr(obj, node.parent_attr)
    return None


def get_children(obj: models.Model) -> models.QuerySet | None:
    """Hijos lógicos de un objeto del flujo, o None si es hoja."""
    label = model_label(obj)
    if label == "survey.axisvalue":
        observable_response_cls = apps.get_model(
            "answer", "ObservableResponse")
        return observable_response_cls.objects.filter(
            survey_id=obj.survey_id,
            observable__component__axis_id=obj.axis_id)
    node = FLOW_MODELS.get(label)
    if node and node.children_attr:
        return getattr(obj, node.children_attr).all()
    return None
