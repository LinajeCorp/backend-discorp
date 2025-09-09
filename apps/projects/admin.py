from django.contrib import admin
from django.utils.html import format_html
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo Project
    """

    list_display = [
        "nombre",
        "fase_display",
        "objetivo_corto",
        "status_display",
        "prioridad_display",
        "listo_para_ofrecer_display",
        "fecha_modificacion",
    ]

    list_filter = [
        "fase",
        "status",
        "prioridad",
        "listo_para_ofrecer",
        "fecha_creacion",
    ]

    search_fields = ["nombre", "objetivo", "ultima_actualizacion"]

    readonly_fields = ["fecha_creacion", "fecha_modificacion"]

    fieldsets = (
        ("Información básica", {"fields": ("nombre", "fase", "objetivo")}),
        (
            "Estado del proyecto",
            {"fields": ("status", "prioridad", "listo_para_ofrecer")},
        ),
        ("Seguimiento", {"fields": ("ultima_actualizacion",)}),
        (
            "Auditoría",
            {
                "fields": ("fecha_creacion", "fecha_modificacion"),
                "classes": ("collapse",),
            },
        ),
    )

    def objetivo_corto(self, obj):
        """Muestra una versión corta del objetivo"""
        return obj.objetivo[:100] + "..." if len(obj.objetivo) > 100 else obj.objetivo

    objetivo_corto.short_description = "Objetivo"

    def fase_display(self, obj):
        """Muestra la fase con colores"""
        colors = {
            "ejecucion": "#ffc107",  # Amarillo
            "completado": "#28a745",  # Verde
            "pausado": "#6c757d",  # Gris
        }
        color = colors.get(obj.fase, "#6c757d")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 6px; '
            'border-radius: 3px; font-size: 11px; font-weight: bold;">{}</span>',
            color,
            obj.get_fase_display().upper(),
        )

    fase_display.short_description = "Fase"

    def status_display(self, obj):
        """Muestra el status con colores"""
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 6px; '
            'border-radius: 3px; font-size: 11px; font-weight: bold;">{}</span>',
            obj.status_color,
            obj.get_status_display(),
        )

    status_display.short_description = "Status"

    def prioridad_display(self, obj):
        """Muestra la prioridad con colores"""
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 6px; '
            'border-radius: 3px; font-size: 11px; font-weight: bold;">{}</span>',
            obj.prioridad_color,
            obj.get_prioridad_display(),
        )

    prioridad_display.short_description = "Prioridad"

    def listo_para_ofrecer_display(self, obj):
        """Muestra si está listo para ofrecer con colores"""
        color = "#28a745" if obj.listo_para_ofrecer == "si" else "#dc3545"
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 6px; '
            'border-radius: 3px; font-size: 11px; font-weight: bold;">{}</span>',
            color,
            obj.get_listo_para_ofrecer_display(),
        )

    listo_para_ofrecer_display.short_description = "¿Listo para ofrecer?"
