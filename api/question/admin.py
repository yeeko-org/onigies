from django.contrib import admin

from question.models import QuestionnaireSettings


@admin.register(QuestionnaireSettings)
class QuestionnaireSettingsAdmin(admin.ModelAdmin):
    """Única vía para reabrir el cuestionario: la API solo cierra."""
    list_display = ["__str__", "content_open", "seeded_at"]

    def has_add_permission(self, request) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False
