from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    """
    Usuario personalizado para empresa venezolana con campos adicionales
    """

    # Tipos de documento válidos en Venezuela
    TIPO_DOCUMENTO_CHOICES = [
        ('V', 'Cédula de Identidad Venezolana'),
        ('E', 'Cédula de Extranjero'),
        ('P', 'Pasaporte'),
        ('J', 'RIF Jurídico'),
        ('G', 'RIF Gubernamental'),
    ]

    # Campos adicionales
    direccion = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Dirección",
        help_text="Dirección completa del usuario"
    )

    tipo_documento = models.CharField(
        max_length=1,
        choices=TIPO_DOCUMENTO_CHOICES,
        blank=True,
        null=True,
        verbose_name="Tipo de Documento",
        help_text="Tipo de documento de identificación"
    )

    documento = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Número de Documento",
        help_text="Número de cédula, pasaporte o RIF"
    )

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        constraints = [
            models.UniqueConstraint(
                fields=['tipo_documento', 'documento'],
                condition=models.Q(
                    tipo_documento__isnull=False,
                    documento__isnull=False
                ),
                name='unique_documento_per_tipo'
            )
        ]

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    @property
    def documento_completo(self):
        """Retorna el documento con su tipo (ej: V-12345678)"""
        if self.tipo_documento and self.documento:
            return f"{self.tipo_documento}-{self.documento}"
        return None

    def save(self, *args, **kwargs):
        """Override del método save para validaciones adicionales"""
        # Limpiar espacios en el documento
        if self.documento:
            self.documento = self.documento.replace(' ', '').replace('-', '')

        super().save(*args, **kwargs)
