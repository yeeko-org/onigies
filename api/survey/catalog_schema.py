"""
Declaraciones de colección de la app survey.

Dos colecciones primary: el Survey (contenedor del cuestionario, cuyo
detalle anida el paquete de generales) y el GeneralPackage (raíz del
flujo `gen`, espejo de GoodPracticePackage). Ninguna se crea a mano: las
dos nacen de `Institution.save`, por eso `hide_create`.
"""
from ps_schema.registry import (
    collection_registry, CollectionSchema, FilterRef)
from survey.models import GeneralPackage, Survey
from api.views.survey import GeneralPackageViewSet, SurveyViewSet


@collection_registry.register
class SurveySchema(CollectionSchema):
    model = Survey
    level = "primary"
    name = "Cuestionario de las IES"
    plural_name = "Cuestionarios de las IES"
    viewset_class = SurveyViewSet
    open_insertion = False
    all_filters = [FilterRef("periods"), FilterRef("institutions")]
    cat_params = {"init_display": True, "hide_create": True}


@collection_registry.register
class GeneralPackageSchema(CollectionSchema):
    model = GeneralPackage
    level = "primary"
    name = "Envío de preguntas generales"
    plural_name = "Envíos de preguntas generales"
    viewset_class = GeneralPackageViewSet
    open_insertion = False
    all_filters = [FilterRef("periods"), FilterRef("institutions")]
    cat_params = {"init_display": True, "hide_create": True}
