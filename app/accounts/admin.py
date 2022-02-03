from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from app.accounts.models import Admin, Customer, Manager
from app.accounts.forms import RequestCPF

@admin.register(Admin)
class AdminAdmin(UserAdmin):
    """Admin"""

    list_display = ("id", "email", "name")
    list_filter = ("is_active", "is_staff", "groups")
    search_fields = ("email",)
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
    )
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),)

@admin.register(Customer)
class AdminCustomer(UserAdmin):
    """Customer"""

    list_display = ("id", "email", "name")
    list_filter = ("is_active",)
    search_fields = ("email",)
    ordering = ("email",)

    def formfield_for_foreignkey(self, db_field,  request, **kwargs):
        user = request.user
        if user.type == 2:
            kwargs['queryset'] = Manager.objects.filter(id=user.id)
        elif user.type == 0:
            kwargs['queryset'] = Manager.objects.filter(type=2)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        user = request.user
        if user.type == 2:
            return super().get_queryset(request).filter(manager=user.id)
        else:
            return super().get_queryset(request)

    fieldsets = (
        (None, {"fields": ("name", "cpf", "email", "password", "manager",)}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    
                )
            },
        ),
    )
    form = RequestCPF
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("name", "cpf", "email", "password1", "password2", "manager")}),)

@admin.register(Manager)
class AdminManager(UserAdmin):
    """Manager"""

    list_display = ("id", "email", "name")
    list_filter = ("is_active",)
    search_fields = ("email",)
    ordering = ("email",)

    def get_queryset(self, request):
        user = request.user
        return super().get_queryset(request).filter(id=user.id)


    fieldsets = (
        (None, {"fields": ("name", "cpf", "email", "password")}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    
                )
            },
        ),
    )
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("name", "cpf", "email", "password1", "password2")}),)
