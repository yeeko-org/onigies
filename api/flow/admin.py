"""Admin del motor de flujo: Status editable, bitácoras de lectura."""
from django.contrib import admin

from flow.models import Status, FlowEvent, Attachment


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = [
        "name", "group", "public_name", "role", "is_default",
        "is_public", "requires_comment", "propagates_up",
        "auto_on_first_save", "order", "color", "icon"]
    list_editable = ["order", "color", "icon", "is_public"]
    list_filter = ["group", "role"]
    search_fields = ["name", "public_name"]
    filter_horizontal = [
        "applicable_models", "next_statuses", "valid_child_statuses"]


@admin.register(FlowEvent)
class FlowEventAdmin(admin.ModelAdmin):
    """Solo lectura: el timeline es bitácora, no se edita a mano."""
    list_display = [
        "id", "target", "from_status", "to_status", "user",
        "comment", "created_at"]
    list_filter = ["to_status", "content_type"]
    date_hierarchy = "created_at"

    def has_add_permission(self, request) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    """Lectura y borrado; los adjuntos se crean desde la API."""
    list_display = [
        "id", "target", "file", "event", "uploaded_by", "created_at"]
    list_filter = ["content_type"]

    def has_add_permission(self, request) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False
