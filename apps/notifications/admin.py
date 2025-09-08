from django.contrib import admin
from django.urls import path, reverse
from django.utils import timezone
from fcm_django.models import FCMDevice
from .models import NotificationHistory
from .admin_views import (
    send_notification_view,
    notification_history_view,
    GetUserDevicesView,
)


@admin.register(NotificationHistory)
class NotificationHistoryAdmin(admin.ModelAdmin):
    """
    Admin para el historial de notificaciones
    """

    list_display = [
        "title",
        "type_display",
        "target_display",
        "sent_by",
        "devices_count",
        "status_display",
        "created_at",
    ]
    list_filter = ["notification_type", "status", "created_at", "sent_by"]
    search_fields = ["title", "body", "target_user__username", "sent_by__username"]
    readonly_fields = [
        "sent_by",
        "devices_count",
        "status",
        "error_message",
        "created_at",
        "data_payload",
    ]
    ordering = ["-created_at"]

    def type_display(self, obj):
        return obj.type_badge

    type_display.short_description = "Tipo"
    type_display.allow_tags = True

    def status_display(self, obj):
        return obj.status_badge

    status_display.short_description = "Estado"
    status_display.allow_tags = True

    def target_display(self, obj):
        if obj.target_user:
            return f"👤 {obj.target_user.username}"
        elif obj.notification_type == "broadcast":
            return "📢 Todos los usuarios"
        return "❓ No especificado"

    target_display.short_description = "Destinatario"

    def has_add_permission(self, request):
        # Deshabilitamos agregar desde aquí, se hace desde la vista personalizada
        return False

    def has_change_permission(self, request, obj=None):
        # Solo lectura
        return False


class NotificationAdminSite(admin.AdminSite):
    """
    Sitio admin personalizado para notificaciones
    """

    site_header = "Panel de Notificaciones Push"
    site_title = "Notificaciones"
    index_title = "Gestión de Notificaciones"


# Crear una instancia del sitio personalizado
notification_admin_site = NotificationAdminSite(name="notification_admin")


class CustomNotificationAdmin:
    """
    Admin personalizado con vistas adicionales para notificaciones
    """

    def get_urls(self):
        """
        Agregar URLs personalizadas al admin
        """
        urls = super().get_urls() if hasattr(super(), "get_urls") else []
        custom_urls = [
            path(
                "send-notification/",
                self.admin_site.admin_view(send_notification_view),
                name="send_notification",
            ),
            path(
                "notification-history/",
                self.admin_site.admin_view(notification_history_view),
                name="notification_history",
            ),
            path(
                "ajax/user-devices/",
                GetUserDevicesView.as_view(),
                name="ajax_user_devices",
            ),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        """
        Vista personalizada para la lista de notificaciones
        """
        extra_context = extra_context or {}

        # Estadísticas rápidas
        total_notifications = NotificationHistory.objects.count()
        sent_today = NotificationHistory.objects.filter(
            created_at__date=timezone.now().date(), status="sent"
        ).count()
        total_devices = FCMDevice.objects.filter(active=True).count()

        extra_context.update(
            {
                "total_notifications": total_notifications,
                "sent_today": sent_today,
                "total_devices": total_devices,
                "send_notification_url": reverse("admin:send_notification"),
                "notification_history_url": reverse("admin:notification_history"),
            }
        )

        return super().changelist_view(request, extra_context)


# Aplicar el admin personalizado al modelo existente
admin.site.unregister(NotificationHistory)


@admin.register(NotificationHistory)
class EnhancedNotificationHistoryAdmin(
    CustomNotificationAdmin, NotificationHistoryAdmin
):
    """
    Admin mejorado que combina funcionalidad personalizada con el admin base
    """

    change_list_template = "admin/notifications/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "send-notification/",
                self.admin_site.admin_view(send_notification_view),
                name="send_notification",
            ),
            path(
                "notification-history/",
                self.admin_site.admin_view(notification_history_view),
                name="notification_history",
            ),
            path(
                "ajax/user-devices/",
                GetUserDevicesView.as_view(),
                name="ajax_user_devices",
            ),
        ]
        return custom_urls + urls


# Dejamos que fcm-django maneje su propio admin para FCMDevice
# El admin por defecto de fcm-django ya es bastante completo
