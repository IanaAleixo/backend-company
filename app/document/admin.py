from django.contrib import admin
from app.document.models import Upload

@admin.register(Upload)
class AdminUpload(admin.ModelAdmin):
    """Upload"""

    list_display  = ("title", "document", "customer")
    search_fields = ("title",)
    ordering = ("title",)
