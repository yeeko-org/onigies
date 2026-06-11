"""Comando para sembrar el catálogo de status del flujo."""
from django.core.management.base import BaseCommand

from flow.seed import seed_flow


class Command(BaseCommand):
    help = ("Siembra el catálogo de Status del flujo de validación "
            "(idempotente; los M2M se reconstruyen).")

    def handle(self, *args, **options) -> None:
        counts = seed_flow()
        msg = (f"Status creados: {counts['created']}, "
               f"actualizados: {counts['updated']}.")
        self.stdout.write(self.style.SUCCESS(msg))
