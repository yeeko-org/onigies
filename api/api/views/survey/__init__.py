from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.permissions import IsInstitutionOwnerOrSuperuser
from api.views.common_views import BaseGenericViewSet
from survey.models import Survey
from api.views.survey.serializers import SurveySerializer


class SurveyViewSet(BaseGenericViewSet):
    """Survey CRUD. Reads are scoped to the user's institution except
    for reviewers/staff/superusers, who read all. Writes (PATCH/PUT/
    DELETE) require ownership of the matching institution or
    superuser. POST is superuser-only.
    """
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [IsAuthenticated, IsInstitutionOwnerOrSuperuser]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_anonymous:
            return qs.none()
        if user.is_reviewer:
            return qs
        if user.institution_id:
            return qs.filter(institution_id=user.institution_id)
        return qs.none()

