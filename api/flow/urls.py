"""URLs del motor de flujo de validación."""
from django.urls import path
from rest_framework.routers import DefaultRouter

from flow.attachment_views import (
    FlowAttachmentDetailView, FlowAttachmentDownloadView, FlowAttachmentView)
from flow.views import (
    FlowAdminTransitionView, FlowEventDetailView, FlowEventView,
    FlowTransitionView, StatusViewSet)

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
    path(
        f'{_obj}/events/<int:event_pk>/',
        FlowEventDetailView.as_view(),
        name='flow-event-detail',
    ),
    path(
        f'{_obj}/admin-transitions/',
        FlowAdminTransitionView.as_view(),
        name='flow-admin-transitions',
    ),
    path(
        f'{_obj}/attachments/',
        FlowAttachmentView.as_view(),
        name='flow-attachments',
    ),
    path(
        f'{_obj}/attachments/<int:attachment_id>/',
        FlowAttachmentDetailView.as_view(),
        name='flow-attachment-detail',
    ),
    path(
        f'{_obj}/attachments/<int:attachment_id>/download/',
        FlowAttachmentDownloadView.as_view(),
        name='flow-attachment-download',
    ),
]
