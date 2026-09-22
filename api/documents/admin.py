from django.contrib import admin

from documents.models import PublicDocument


@admin.register(PublicDocument)
class PublicDocumentAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'slug', 'generator', 'is_published', 'order', 'updated_at']
    list_editable = ['is_published', 'order']
    search_fields = ['title', 'slug']
