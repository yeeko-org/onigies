"""
Checkpoint de verificación del flujo (plan §9.4) — solo lectura.

Compara los conteos del flujo viejo (status_register / status_sending,
comentarios y adjuntos por modelo) contra los del nuevo (`status`,
FlowEvent, Attachment). No modifica datos: re-ejecutable en producción
antes de la fase de borrado (§8).
"""
from django.apps import apps
from django.core.management.base import BaseCommand
from django.db.models import Count

from flow.management.commands.migrate_flow_data import (
    MODEL_STATUS_MAPS, COMMENT_MODELS, COMMENT_FIELD_MODELS,
    ATTACHMENT_MODELS)
from flow.models import Status, FlowEvent, Attachment


class Command(BaseCommand):
    help = ("Compara conteos del flujo viejo vs el nuevo (solo "
            "lectura). Correr tras seed_flow y migrate_flow_data.")

    def handle(self, *args, **options) -> None:
        self.check_catalog()
        self.check_statuses()
        self.check_comments()
        self.check_attachments()

    def check_catalog(self) -> None:
        self.stdout.write(self.style.MIGRATE_HEADING("Catálogo Status"))
        rows = (Status.objects.values("group")
                .annotate(n=Count("pk")).order_by("group"))
        for row in rows:
            default = Status.objects.filter(
                group=row["group"], is_default=True).first()
            self.stdout.write(
                f"  {row['group']}: {row['n']} status "
                f"(default: {default.pk if default else 'FALTA'})")

    def check_statuses(self) -> None:
        self.stdout.write(self.style.MIGRATE_HEADING("Status por modelo"))
        for app_label, model_name, field, mapping in MODEL_STATUS_MAPS:
            model = apps.get_model(app_label, model_name)
            old = dict(
                model.objects.filter(**{f"{field}__isnull": False})
                .values_list(f"{field}_id")
                .annotate(n=Count("pk")))
            new = dict(
                model.objects.filter(status__isnull=False)
                .values_list("status_id").annotate(n=Count("pk")))
            self.stdout.write(f"  {model_name} ({field} → status):")
            for old_id, count in sorted(old.items()):
                new_id = mapping.get(old_id)
                migrated = new.get(new_id, 0) if new_id else 0
                mark = "ok" if new_id and migrated >= count else "REVISAR"
                self.stdout.write(
                    f"    {old_id}: {count} → "
                    f"{new_id or 'SIN MAPEO'}: {migrated}  [{mark}]")
            pending = model.objects.filter(
                **{f"{field}__isnull": False}, status__isnull=True).count()
            if pending:
                self.stdout.write(self.style.WARNING(
                    f"    {pending} registros con status viejo pero "
                    f"sin status nuevo"))

    def check_comments(self) -> None:
        self.stdout.write(self.style.MIGRATE_HEADING("Comentarios"))
        old_total = 0
        for app_label, model_name, _ in COMMENT_MODELS:
            count = apps.get_model(app_label, model_name).objects.count()
            old_total += count
            self.stdout.write(f"  {model_name}: {count}")
        for app_label, model_name in COMMENT_FIELD_MODELS:
            count = (apps.get_model(app_label, model_name).objects
                     .exclude(comments__isnull=True)
                     .exclude(comments="").count())
            old_total += count
            self.stdout.write(f"  {model_name}.comments: {count}")
        new_total = FlowEvent.objects.filter(
            from_status__isnull=True, to_status__isnull=True).count()
        mark = "ok" if new_total >= old_total else "REVISAR"
        self.stdout.write(
            f"  Total viejo: {old_total} → FlowEvent (comentarios "
            f"puros): {new_total}  [{mark}]")

    def check_attachments(self) -> None:
        self.stdout.write(self.style.MIGRATE_HEADING("Adjuntos"))
        old_total = 0
        for app_label, model_name, _ in ATTACHMENT_MODELS:
            count = apps.get_model(app_label, model_name).objects.count()
            old_total += count
            self.stdout.write(f"  {model_name}: {count}")
        evidence = apps.get_model("example", "Evidence")
        with_target = evidence.objects.filter(
            good_practice__isnull=False).count() + \
            evidence.objects.filter(
                good_practice__isnull=True,
                feature_good_practice__isnull=False).count()
        orphan = evidence.objects.count() - with_target
        old_total += with_target
        self.stdout.write(
            f"  Evidence: {with_target} con target"
            + (f" ({orphan} sin target, no migran)" if orphan else ""))
        new_total = Attachment.objects.count()
        mark = "ok" if new_total >= old_total else "REVISAR"
        self.stdout.write(
            f"  Total viejo: {old_total} → Attachment: {new_total}  "
            f"[{mark}]")
