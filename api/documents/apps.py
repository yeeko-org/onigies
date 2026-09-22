from django.apps import AppConfig


class DocumentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'documents'
    verbose_name = 'Documentos públicos'

    def ready(self) -> None:
        import documents.catalog_schema  # noqa: F401 — registra la colección
        return super().ready()
