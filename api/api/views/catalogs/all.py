from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from ies.models import StatusControl, User
from flow.models import ROLE_CHOICES
from ps_schema.models import LEVEL_CHOICES
from ps_schema.registry import catalog_registry, collection_registry
from api.views.catalogs.serializers import StatusControlSerializer
from api.views.auth.serializers import UserProfileSerializer


class CatalogsView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        catalogs = {
            "status_control": StatusControlSerializer(
                StatusControl.objects.all(), many=True).data,
            "levels": [
                {"key_name": k, "name": v} for k, v in LEVEL_CHOICES],
            "flow_roles": dict(ROLE_CHOICES),
            "collections": (
                collection_registry.get_collections_data()
                + catalog_registry.get_collections_data()
            ),
            "filter_groups": list(catalog_registry.iter_filter_group_data()),
        }
        # Dump de catálogos por snake_name (institution, period, axis, ...).
        catalogs.update(catalog_registry.get_catalog_dump())
        if request.user.is_authenticated:
            reviewer_users = User.objects.filter(reviewer=True)
            if request.user.institution:
                ies_users = User.objects.filter(
                    institution=request.user.institution)
            else:
                ies_users = User.objects.filter(institution__isnull=False)
            all_users = (reviewer_users | ies_users).distinct()
            catalogs["user"] = UserProfileSerializer(
                all_users, many=True).data
        else:
            catalogs["institution"] = []
        return Response(catalogs)
