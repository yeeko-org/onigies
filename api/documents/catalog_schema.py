"""Declaración de colección de la app documents."""
from ps_schema.registry import collection_registry, CollectionSchema
from documents.models import PublicDocument
from api.views.documents import PublicDocumentViewSet


@collection_registry.register
class PublicDocumentSchema(CollectionSchema):
    model = PublicDocument
    level = "primary"
    viewset_class = PublicDocumentViewSet
    icon = "folder_open"
    color = "blue-grey"
    cat_params = {"init_display": True}
