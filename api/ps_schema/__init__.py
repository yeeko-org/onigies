"""Paquete ps_schema: metadata de colecciones, catálogos y grupos de filtro."""


def generate_serializer(
        model_cls: type, count_fields: dict | None = None) -> type:
    """
    Genera un ModelSerializer con fields='__all__'.
    Si se pasa count_fields, agrega un ReadOnlyField() por cada nombre de
    anotación para exponer las anotaciones del queryset en la respuesta.
    """
    from rest_framework import serializers
    meta = type('Meta', (), {'model': model_cls, 'fields': '__all__'})
    attrs: dict = {'Meta': meta}
    for ann_name in (count_fields or {}):
        attrs[ann_name] = serializers.ReadOnlyField()
    return type(
        f'{model_cls.__name__}AutoSerializer',
        (serializers.ModelSerializer,),
        attrs,
    )
