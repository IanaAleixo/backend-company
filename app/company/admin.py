from re import search
from django.contrib import admin
from app.company.models import Company

@admin.register(Company)
class AdminCompany(admin.ModelAdmin):
    """Company"""

    list_display  = ("name", "cnpj", "address")
    list_filter = ("is_active",)
    search_fields = ("name",)
    ordering = ("name",)

