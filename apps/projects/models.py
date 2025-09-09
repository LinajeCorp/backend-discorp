from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Project(models.Model):
    """
    Modelo para gestionar proyectos/productos de la empresa
    """
    
    # Choices para los campos
    FASE_CHOICES = [
        ('ejecucion', 'Ejecución'),
        ('completado', 'Completado'),
        ('pausado', 'Pausado'),
    ]
    
    STATUS_CHOICES = [
        ('en_curso', 'EN CURSO'),
        ('en_seguimiento', 'EN SEGUIMIENTO'),
        ('pausado', 'PAUSADO'),
    ]
    
    PRIORIDAD_CHOICES = [
        ('normal', 'NORMAL'),
        ('alta', 'ALTA'),
        ('baja', 'BAJA'),
    ]
    
    LISTO_OFRECER_CHOICES = [
        ('si', 'SI'),
        ('no', 'NO'),
    ]
    
    # Campos del modelo
    nombre = models.CharField(
        max_length=200,
        verbose_name="Producto/Solución",
        help_text="Nombre del proyecto o producto"
    )
    
    fase = models.CharField(
        max_length=20,
        choices=FASE_CHOICES,
        default='ejecucion',
        verbose_name="Fase",
        help_text="Fase actual del proyecto"
    )
    
    objetivo = models.TextField(
        verbose_name="Objetivo",
        help_text="Descripción detallada del objetivo del proyecto"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='en_curso',
        verbose_name="Status",
        help_text="Estado actual del proyecto"
    )
    
    prioridad = models.CharField(
        max_length=10,
        choices=PRIORIDAD_CHOICES,
        default='normal',
        verbose_name="Prioridad",
        help_text="Nivel de prioridad del proyecto"
    )
    
    ultima_actualizacion = models.TextField(
        verbose_name="Última actualización",
        help_text="Descripción de la última actualización del proyecto"
    )
    
    listo_para_ofrecer = models.CharField(
        max_length=5,
        choices=LISTO_OFRECER_CHOICES,
        default='no',
        verbose_name="¿Listo para ofrecer?",
        help_text="Indica si el proyecto está listo para ser ofrecido"
    )
    
    # Campos de auditoría
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    
    fecha_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de modificación"
    )
    
    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} - {self.get_fase_display()}"
    
    @property
    def status_color(self):
        """Retorna el color asociado al status para el frontend"""
        colors = {
            'en_curso': '#007bff',        # Azul
            'en_seguimiento': '#28a745',  # Verde
            'pausado': '#6c757d',         # Gris
        }
        return colors.get(self.status, '#6c757d')
    
    @property
    def prioridad_color(self):
        """Retorna el color asociado a la prioridad para el frontend"""
        colors = {
            'alta': '#dc3545',      # Rojo
            'normal': '#28a745',    # Verde
            'baja': '#ffc107',      # Amarillo
        }
        return colors.get(self.prioridad, '#28a745')
