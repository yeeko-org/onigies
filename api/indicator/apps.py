from django.apps import AppConfig


class IndicatorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'indicator'

    def ready(self):
        import indicator.catalog_schema  # noqa: F401 — registra catálogos
