"""
Repara `sent_at` nulo en paquetes ya enviados (task-59).

El motor guardaba con `update_fields=['status']`, así que el hook de
`save()` que fija `sent_at` nunca se persistía. La fecha real es
recuperable del primer FlowEvent de envío, escrito en la misma
transacción que el cambio de status.

Idempotente: solo toca paquetes con `sent_at` nulo, y escribe con
`queryset.update()` para no disparar el hook de `save()` (que pondría
la fecha de hoy). Dry-run por omisión; `--apply` persiste.
"""
from argparse import ArgumentParser
from datetime import datetime

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db.models import Min

from example.models import GoodPracticePackage
from flow.models import FlowEvent
from survey.models import GeneralPackage

# (modelo, statuses de envío, status borrador)
TARGETS = (
    (GoodPracticePackage, ['bp_sent', 'bp_resent'], 'bp_draft'),
    (GeneralPackage, ['gen_sent', 'gen_resent'], 'gen_draft'),
)


class Command(BaseCommand):
    help = ("Recupera la fecha de envío (`sent_at`) de los paquetes bp "
            "y gen desde su primer FlowEvent de envío. Sin --apply "
            "solo reporta.")

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            '--apply', action='store_true',
            help="Persiste los cambios (por omisión solo simula).")

    def handle(self, *args, **options) -> None:
        apply_changes = options['apply']
        if not apply_changes:
            self.stdout.write(self.style.WARNING(
                "Modo simulación: no se escribirá nada. "
                "Usa --apply para persistir."))
        totals = {'reparados': 0, 'sin_evento': 0, 'con_fecha': 0}
        for model, sends, draft in TARGETS:
            counts = self.repair_model(model, sends, draft, apply_changes)
            for key, value in counts.items():
                totals[key] += value
        self.stdout.write(self.style.MIGRATE_HEADING("Totales"))
        self.stdout.write(
            f"  Reparados: {totals['reparados']}\n"
            f"  Sin evento de envío (no tocados): {totals['sin_evento']}\n"
            f"  Ya tenían fecha (intactos): {totals['con_fecha']}")

    def repair_model(self, model, sends: list[str], draft: str,
                     apply_changes: bool) -> dict[str, int]:
        """Repara un modelo y devuelve los conteos de la pasada."""
        self.stdout.write(self.style.MIGRATE_HEADING(model.__name__))
        first_send = self.first_send_dates(model, sends)
        with_date = model.objects.filter(sent_at__isnull=False).count()
        nulls = model.objects.filter(sent_at__isnull=True)
        repaired = 0
        orphans = []
        for package in nulls.order_by('pk'):
            sent_at = first_send.get(package.pk)
            if sent_at is None:
                # Los borradores nunca se enviaron: no son anomalía.
                if package.status_id not in (None, draft):
                    orphans.append(package)
                continue
            self.stdout.write(
                f"  id={package.pk} status={package.status_id} "
                f"→ sent_at={sent_at.isoformat()}")
            if apply_changes:
                model.objects.filter(pk=package.pk).update(sent_at=sent_at)
            repaired += 1
        if not repaired:
            self.stdout.write("  Sin paquetes por reparar.")
        for package in orphans:
            self.stdout.write(self.style.WARNING(
                f"  SIN EVENTO id={package.pk} "
                f"status={package.status_id}: requiere decisión manual, "
                f"no se tocó."))
        self.stdout.write(
            f"  Reparados: {repaired} | sin evento: {len(orphans)} | "
            f"ya con fecha: {with_date}")
        return {'reparados': repaired, 'sin_evento': len(orphans),
                'con_fecha': with_date}

    @staticmethod
    def first_send_dates(model, sends: list[str]) -> dict[int, datetime]:
        """Primer evento de envío por paquete: {object_id: created_at}."""
        content_type = ContentType.objects.get_for_model(model)
        return dict(
            FlowEvent.objects
            .filter(content_type=content_type, to_status_id__in=sends)
            .values('object_id')
            .annotate(first=Min('created_at'))
            .values_list('object_id', 'first'))
