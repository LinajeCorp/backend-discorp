from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class NotificationHistory(models.Model):
    """
    Modelo para guardar el historial de notificaciones enviadas
    """
    NOTIFICATION_TYPES = [
        ('test', 'Prueba'),
        ('user', 'Usuario Específico'),
        ('broadcast', 'Broadcast'),
        ('admin', 'Administrador'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('sent', 'Enviado'),
        ('failed', 'Fallido'),
    ]

    title = models.CharField(max_length=255, verbose_name="Título")
    body = models.TextField(verbose_name="Mensaje")
    notification_type = models.CharField(
        max_length=20, 
        choices=NOTIFICATION_TYPES, 
        verbose_name="Tipo"
    )
    target_user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Usuario Destino",
        help_text="Dejar vacío para broadcast"
    )
    sent_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications_sent',
        verbose_name="Enviado por"
    )
    devices_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Dispositivos alcanzados"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Estado"
    )
    error_message = models.TextField(
        blank=True,
        verbose_name="Mensaje de Error"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha de Envío"
    )
    data_payload = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Datos Adicionales"
    )

    class Meta:
        verbose_name = "Historial de Notificación"
        verbose_name_plural = "Historial de Notificaciones"
        ordering = ['-created_at']

    def __str__(self):
        if self.target_user:
            return f"{self.title} → {self.target_user.username}"
        elif self.notification_type == 'broadcast':
            return f"{self.title} → Todos los usuarios"
        return self.title

    @property
    def status_badge(self):
        """Retorna un badge HTML para el estado"""
        colors = {
            'pending': '#ffc107',
            'sent': '#28a745',
            'failed': '#dc3545'
        }
        return f'<span style="color: {colors.get(self.status, "#6c757d")}">{self.get_status_display()}</span>'

    @property
    def type_badge(self):
        """Retorna un badge HTML para el tipo"""
        icons = {
            'test': '🧪',
            'user': '👤',
            'broadcast': '📢',
            'admin': '👨‍💼'
        }
        return f'{icons.get(self.notification_type, "📱")} {self.get_notification_type_display()}'