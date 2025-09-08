from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Administración personalizada para el modelo User con campos venezolanos
    """

    # Campos que se muestran en la lista de usuarios
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'tipo_documento',
        'documento',
        'is_staff',
        'is_active',
        'date_joined'
    )

    # Campos por los que se puede buscar
    search_fields = (
        'username',
        'first_name',
        'last_name',
        'email',
        'documento'
    )

    # Filtros laterales
    list_filter = (
        'is_staff',
        'is_superuser',
        'is_active',
        'tipo_documento',
        'date_joined'
    )

    # Organización de campos en el formulario de edición
    fieldsets = BaseUserAdmin.fieldsets + (
        (_('Información Venezolana'), {
            'fields': ('direccion', 'tipo_documento', 'documento'),
            'classes': ('wide',),
        }),
    )

    # Campos para el formulario de creación de usuario
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (_('Información Venezolana'), {
            'fields': ('direccion', 'tipo_documento', 'documento'),
            'classes': ('wide',),
        }),
    )

    # Campos de solo lectura
    readonly_fields = ('date_joined', 'last_login')

    def get_queryset(self, request):
        """Optimizar consultas con select_related si es necesario"""
        return super().get_queryset(request)
