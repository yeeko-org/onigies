from django.contrib.admin import register, ModelAdmin
from .models import Survey

@register(Survey)
class SurveyAdmin(ModelAdmin):
    list_display = ('institution', 'period')
    list_filter = ('period',)
    search_fields = ('institution__name', 'period__year')
    filter_horizontal = ('instances', 'sectors_legacy')