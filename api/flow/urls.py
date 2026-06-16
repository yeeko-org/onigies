"""URLs del motor de flujo de validación."""
from django.urls import path
from rest_framework.routers import DefaultRouter

from flow.views import FlowEventView, FlowTransitionView, StatusViewSet

router = DefaultRouter()
router.register(r'statuses', StatusViewSet, basename='flow-status')

_obj = '<str:app_label>/<str:model_name>/<int:pk>'

urlpatterns = router.urls + [
    path(
        f'{_obj}/transitions/',
        FlowTransitionView.as_view(),
        name='flow-transitions',
    ),
    path(
        f'{_obj}/events/',
        FlowEventView.as_view(),
        name='flow-events',
    ),
]