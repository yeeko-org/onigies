from django.urls import include, path
from rest_framework import routers

from api.views.catalogs.all import CatalogsView
from ps_schema.registry import catalog_registry

router = routers.DefaultRouter()

# Catálogos (CatalogSchema) registrados desde el registry. Reemplaza los
# registros manuales previos (period, institution, feature, axis, ...).
# Agrega además /catalogs/a_option/ y /catalogs/question_type/ (antes no
# existían como endpoints CRUD).
catalog_registry.register_routes(router)


urlpatterns = [
    path("all/", CatalogsView.as_view(), name="catalogs_all"),
    path('', include(router.urls)),
]
