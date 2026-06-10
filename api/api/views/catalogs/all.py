from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from ies.models import StatusControl
from ps_schema.models import LEVEL_CHOICES
from ps_schema.registry import catalog_registry, collection_registry
from api.views.catalogs.serializers import StatusControlSerializer


class CatalogsView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        catalogs = {
            "status_control": StatusControlSerializer(
                StatusControl.objects.all(), many=True).data,
            "levels": [
                {"key_name": k, "name": v} for k, v in LEVEL_CHOICES],
            "collections": (
                collection_registry.get_collections_data()
                + catalog_registry.get_collections_data()
            ),
            "filter_groups": list(catalog_registry.iter_filter_group_data()),
        }
        # Dump de catálogos por snake_name (institution, period, axis, ...).
        catalogs.update(catalog_registry.get_catalog_dump())
        if not request.user.is_authenticated:
            catalogs["institution"] = []
        return Response(catalogs)
