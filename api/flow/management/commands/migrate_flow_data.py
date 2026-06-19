"""
Migra los datos del flujo viejo al nuevo (idempotente, re-ejecutable).

1. Status: copia status_register / status_sending al campo `status`
   nuevo según el mapeo (modelo, id viejo) → id nuevo del plan
   (ies/flux_rules/PLAN_flujo_validacion.md §6). Los ids viejos sin
   mapeo se reportan sin migrarse.
2. Comentarios: ObservableComment, GroupComment, GeneralGroupComment y
   los TextField `comments` de example → FlowEvent (comentario puro).
3. Adjuntos: GroupAttachment, GeneralGroupAttachment, Evidence →
   Attachment (mismo path de archivo; no se recopia el archivo físico).

Requiere haber corrido antes `migrate` y `seed_flow`.
"""
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from flow.models import FlowEvent, Attachment

CP_MAP = {
    "pre_start": "cp_pre_start",
    "filling": "cp_filling",
    "sent": "cp_sent",
    "need_changes": "cp_need_changes",
    "approved": "cp_approved",
    "requires_new_checking": "cp_in_review",
}
# El grupo general usaba los ids del flujo register viejo; `sent` y
# `requires_new_checking` no tienen equivalente exacto en el flujo gen
# (un solo nivel) — ambos caen en gen_completed (en espera de revisión).
GEN_MAP = {
    "pre_start": "gen_pre_start",
    "filling": "gen_filling",
    "sent": "gen_completed",
    "need_changes": "gen_need_changes",
    "approved": "gen_approved",
    "requires_new_checking": "gen_completed",
}
# G = GoodPractice. `created`/`in_review` ⇒ la práctica viajó con el envío del
# paquete: completada y a la espera de revisión (bp_completed).
GOOD_PRACTICE_MAP = {
    "draft": "bp_draft",
    "ready_to_send": "bp_completed",
    "created": "bp_completed",
    "in_review": "bp_completed",
    "needs_adjustments": "bp_need_changes",
    "ready_to_resend": "bp_adjusted",
    "need_new_checking": "bp_adjusted",
    "accepted": "bp_for_ruling",
    "discarded": "bp_rejected",
}
# P = GoodPracticePackage. `ready_to_send`/`ready_to_resend` ⇒ "listo pero no
# enviado" (vuelve a bp_draft). El envío real lo marcan `created`/`in_review`.
PACKAGE_MAP = {
    "draft": "bp_draft",
    "ready_to_send": "bp_draft",
    "created": "bp_sent",
    "in_review": "bp_sent",
    "needs_adjustments": "bp_need_changes",
    "ready_to_resend": "bp_draft",
    "need_new_checking": "bp_resent",
    "accepted": "bp_finished",
    "discarded": "bp_finished",
}

# (app, modelo, campo viejo, mapeo)
MODEL_STATUS_MAPS = [
    ("example", "GoodPractice", "status_sending", GOOD_PRACTICE_MAP),
    ("example", "GoodPracticePackage", "status_sending", PACKAGE_MAP),
    ("survey", "AxisValue", "status_register", CP_MAP),
    ("answer", "ObservableResponse", "status_register", CP_MAP),
    ("answer", "GroupResponse", "status_register", CP_MAP),
    ("survey", "GeneralGroupResponse", "status_register", GEN_MAP),
]

# (app, modelo de comentario, FK al target)
COMMENT_MODELS = [
    ("answer", "ObservableComment", "observable_response"),
    ("answer", "GroupComment", "group_response"),
    ("survey", "GeneralGroupComment", "general_group_response"),
]

# (app, modelo con TextField comments)
COMMENT_FIELD_MODELS = [
    ("example", "GoodPracticePackage"),
    ("example", "GoodPractice"),
    ("example", "FeatureGoodPractice"),
]

# (app, modelo de adjunto, FK al target)
ATTACHMENT_MODELS = [
    ("answer", "GroupAttachment", "group_response"),
    ("survey", "GeneralGroupAttachment", "general_group_response"),
]


class Command(BaseCommand):
    help = ("Copia status, comentarios y adjuntos del flujo viejo a "
            "flow (idempotente). Correr tras migrate y seed_flow.")

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--comments-user",
            help="Username que firmará los FlowEvent creados desde los "
                 "TextField comments (default: primer superusuario)")

    def handle(self, *args, **options) -> None:
        user_model = apps.get_model("ies", "User")
        username = options.get("comments_user")
        if username:
            comments_user = user_model.objects.filter(
                username=username).first()
            if not comments_user:
                raise CommandError(f"No existe el usuario '{username}'")
        else:
            comments_user = user_model.objects.filter(
                is_superuser=True).order_by("pk").first()
            if not comments_user:
                raise CommandError(
                    "No hay superusuario; usa --comments-user")

        with transaction.atomic():
            self.migrate_statuses()
            self.reconcile_bp_children()
            self.migrate_comments()
            self.migrate_comment_fields(comments_user)
            self.migrate_attachments()
            self.migrate_evidences()
        self.stdout.write(self.style.SUCCESS("Migración completa."))

    # ------------------------------------------------------------------
    def migrate_statuses(self) -> None:
        for app_label, model_name, field, mapping in MODEL_STATUS_MAPS:
            model = apps.get_model(app_label, model_name)
            total = 0
            for old_id, new_id in mapping.items():
                updated = model.objects.filter(
                    **{f"{field}_id": old_id}).update(status_id=new_id)
                total += updated
            unmapped = (
                model.objects
                .filter(**{f"{field}__isnull": False})
                .exclude(**{f"{field}_id__in": mapping})
                .values_list(f"{field}_id", flat=True).distinct())
            self.stdout.write(f"{model_name}: {total} status migrados")
            for old_id in unmapped:
                self.stdout.write(self.style.WARNING(
                    f"  {model_name}: id viejo sin mapeo '{old_id}' "
                    f"(no migrado, decidir manualmente)"))

    def reconcile_bp_children(self) -> None:
        """Red de seguridad de la regla padre-hijo: una práctica de un paquete
        ya enviado no puede seguir en bp_draft. Autorrepara el hueco que deja
        el default='bp_draft' del modelo cuando un id viejo no se mapeó."""
        good_practice = apps.get_model("example", "GoodPractice")
        fixed = (good_practice.objects
                 .filter(package__status_id__in=["bp_sent", "bp_resent"],
                         status_id="bp_draft")
                 .update(status_id="bp_completed"))
        self.stdout.write(
            f"Reconciliación: {fixed} prácticas bp_draft → bp_completed "
            f"(paquete enviado)")

    # ------------------------------------------------------------------
    def _create_event(self, target, user, text, created_at) -> bool:
        """Crea un FlowEvent-comentario si no existe; respeta la fecha
        original (auto_now_add obliga a fijarla con update)."""
        ct = ContentType.objects.get_for_model(target)
        event, created = FlowEvent.objects.get_or_create(
            content_type=ct, object_id=target.pk, user=user,
            comment=text, from_status=None, to_status=None)
        if created and created_at:
            FlowEvent.objects.filter(pk=event.pk).update(
                created_at=created_at)
        return created

    def migrate_comments(self) -> None:
        for app_label, model_name, target_attr in COMMENT_MODELS:
            model = apps.get_model(app_label, model_name)
            count = 0
            for old in model.objects.select_related(target_attr, "user"):
                target = getattr(old, target_attr)
                if self._create_event(
                        target, old.user, old.text, old.created_at):
                    count += 1
            self.stdout.write(
                f"{model_name}: {count} comentarios → FlowEvent")

    def migrate_comment_fields(self, comments_user) -> None:
        for app_label, model_name in COMMENT_FIELD_MODELS:
            model = apps.get_model(app_label, model_name)
            count = 0
            rows = model.objects.exclude(
                comments__isnull=True).exclude(comments="")
            for obj in rows:
                if self._create_event(
                        obj, comments_user, obj.comments, None):
                    count += 1
            self.stdout.write(
                f"{model_name}.comments: {count} → FlowEvent")

    # ------------------------------------------------------------------
    def _create_attachment(self, target, file_name) -> bool:
        ct = ContentType.objects.get_for_model(target)
        _, created = Attachment.objects.get_or_create(
            content_type=ct, object_id=target.pk, file=file_name)
        return created

    def migrate_attachments(self) -> None:
        for app_label, model_name, target_attr in ATTACHMENT_MODELS:
            model = apps.get_model(app_label, model_name)
            count = 0
            for old in model.objects.select_related(target_attr):
                target = getattr(old, target_attr)
                if self._create_attachment(target, old.file.name):
                    count += 1
            self.stdout.write(
                f"{model_name}: {count} adjuntos → Attachment")

    def migrate_evidences(self) -> None:
        evidence_model = apps.get_model("example", "Evidence")
        count = 0
        skipped = 0
        rows = evidence_model.objects.select_related(
            "good_practice", "feature_good_practice")
        for old in rows:
            target = old.good_practice or old.feature_good_practice
            if target is None:
                skipped += 1
                continue
            if self._create_attachment(target, old.file.name):
                count += 1
        self.stdout.write(f"Evidence: {count} adjuntos → Attachment")
        if skipped:
            self.stdout.write(self.style.WARNING(
                f"  Evidence: {skipped} sin target (no migradas)"))
