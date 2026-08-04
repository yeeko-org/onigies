from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import health_check
from api.views.auth.login_views import UserLoginAPIView
from api.views.auth.invitation_views import InvitationTokenViewSet
from api.views.auth.user_views import UserViewSet
from api.views.auth.recovery_views import (
    PasswordRecoveryRequestView,
    PasswordRecoveryValidateView,
    PasswordRecoveryConfirmView,
)

from .views.ps_schemas import CollectionViewSet
from .views.example import EvidenceViewSet
from api.views.ies import InstitutionViewSet
from ps_schema.registry import collection_registry
# from api.views.stop import StationViewSet
# from api.views.report import StairReportViewSet, AscertainableViewSet

router = DefaultRouter()

# router.register(r'station', StationViewSet, basename='station')
# router.register(r'stair_report', StairReportViewSet, basename='stair_report')
# router.register(
#     r'^stair_report/(?P<stair_report_id>[-\d]+)/evidence_image',
#     AscertainableViewSet,
#     basename='stair_report_evidence_image'
# )
# )
router.register(r'collection', CollectionViewSet, basename='collection')
router.register(r'evidence', EvidenceViewSet, basename='evidence')
router.register(r'invitation', InvitationTokenViewSet, basename='invitation')
router.register(r'user', UserViewSet, basename='user')
router.register(r'institution', InstitutionViewSet, basename='institution')

# Colecciones primary (CollectionSchema): good_practice_package, good_practice,
# feature_good_practice, survey, general_package. Reemplaza sus registros
# manuales de arriba (DRF rechaza un basename duplicado).
collection_registry.register_routes(router)

urlpatterns = [
    # path('login/', obtain_auth_token, name='api-login'),
    path('health/', health_check, name='health_check'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path(
        'password-recovery/',
        PasswordRecoveryRequestView.as_view(),
        name='password_recovery_request',
    ),
    path(
        'password-recovery/<uuid:key>/',
        PasswordRecoveryValidateView.as_view(),
        name='password_recovery_validate',
    ),
    path(
        'password-recovery/<uuid:key>/confirm/',
        PasswordRecoveryConfirmView.as_view(),
        name='password_recovery_confirm',
    ),
    path('catalogs/', include('api.views.catalogs.urls')),
    path('flow/', include('flow.urls')),
    # path('space_time/', include('api.views.space_time.urls')),
    path('', include(router.urls)),
]
