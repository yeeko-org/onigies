from django.apps import AppConfig


class FlowConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'flow'
    verbose_name = 'Flujo de validación'

    def ready(self):
        from flow.signals import connect_flow_signals
        from flow.notifications import connect_notification_signals
        connect_flow_signals()
        connect_notification_signals()
