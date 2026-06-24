from django.apps import AppConfig
import sys

class ExampleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'example'
    verbose_name = 'Buenas Prácticas'

    def ready(self) -> None:
        import example.catalog_schema  # noqa: F401 — registra catálogos
        from .initial_data import InitFeatures

        _ready = super().ready()
        if "migrate_initial_data" in sys.argv:
            print("Cargando datos iniciales de Ejemplo...")
            InitFeatures()
            print("Datos iniciales cargados.")
        return _ready
