"""
Re-guarda todas las Institutions para disparar la creación idempotente
de las estructuras eager de `Institution.save` (surveys, axis_values,
packages y el GeneralPackage del flujo gen).

Útil tras agregar nuevas estructuras eager al save —p.ej. al sumar el
módulo cp— para backfillear los datos ya existentes. Idempotente: todo
el save usa get_or_create, así que correrlo varias veces es seguro.
"""
from django.core.management.base import BaseCommand

from ies.models import Institution


class Command(BaseCommand):
    help = "Re-guarda todas las Institutions (backfill de estructuras eager)."

    def handle(self, *args, **options):
        qs = Institution.objects.all()
        total = qs.count()
        for i, institution in enumerate(qs.iterator(), start=1):
            institution.save()
            self.stdout.write(f"  [{i}/{total}] {institution.acronym}")
        self.stdout.write(self.style.SUCCESS(
            f"Re-guardadas {total} instituciones."))