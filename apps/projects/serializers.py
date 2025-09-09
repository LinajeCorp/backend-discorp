from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Project
    """

    # Campos adicionales para mostrar valores legibles
    fase_display = serializers.CharField(source="get_fase_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    prioridad_display = serializers.CharField(
        source="get_prioridad_display", read_only=True
    )
    listo_para_ofrecer_display = serializers.CharField(
        source="get_listo_para_ofrecer_display", read_only=True
    )

    # Campos de colores para el frontend
    status_color = serializers.ReadOnlyField()
    prioridad_color = serializers.ReadOnlyField()

    class Meta:
        model = Project
        fields = [
            "id",
            "nombre",
            "fase",
            "fase_display",
            "objetivo",
            "status",
            "status_display",
            "status_color",
            "prioridad",
            "prioridad_display",
            "prioridad_color",
            "ultima_actualizacion",
            "listo_para_ofrecer",
            "listo_para_ofrecer_display",
            "fecha_creacion",
            "fecha_modificacion",
        ]
        read_only_fields = ["fecha_creacion", "fecha_modificacion"]


class ProjectCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para crear proyectos
    """

    class Meta:
        model = Project
        fields = [
            "nombre",
            "fase",
            "objetivo",
            "status",
            "prioridad",
            "ultima_actualizacion",
            "listo_para_ofrecer",
        ]

    def validate_nombre(self, value):
        """Validar que el nombre no esté vacío y sea único"""
        if not value.strip():
            raise serializers.ValidationError(
                "El nombre del proyecto no puede estar vacío."
            )
        return value.strip()

    def validate_objetivo(self, value):
        """Validar que el objetivo no esté vacío"""
        if not value.strip():
            raise serializers.ValidationError(
                "El objetivo del proyecto no puede estar vacío."
            )
        return value.strip()


class ProjectUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para actualizar proyectos
    """

    class Meta:
        model = Project
        fields = [
            "nombre",
            "fase",
            "objetivo",
            "status",
            "prioridad",
            "ultima_actualizacion",
            "listo_para_ofrecer",
        ]

    def validate_nombre(self, value):
        """Validar que el nombre no esté vacío"""
        if not value.strip():
            raise serializers.ValidationError(
                "El nombre del proyecto no puede estar vacío."
            )
        return value.strip()

    def validate_objetivo(self, value):
        """Validar que el objetivo no esté vacío"""
        if not value.strip():
            raise serializers.ValidationError(
                "El objetivo del proyecto no puede estar vacío."
            )
        return value.strip()


class ProjectListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar proyectos
    """

    fase_display = serializers.CharField(source="get_fase_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    prioridad_display = serializers.CharField(
        source="get_prioridad_display", read_only=True
    )
    listo_para_ofrecer_display = serializers.CharField(
        source="get_listo_para_ofrecer_display", read_only=True
    )
    status_color = serializers.ReadOnlyField()
    prioridad_color = serializers.ReadOnlyField()

    # Campo de objetivo corto para la lista
    objetivo_corto = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "nombre",
            "fase",
            "fase_display",
            "objetivo_corto",
            "status",
            "status_display",
            "status_color",
            "prioridad",
            "prioridad_display",
            "prioridad_color",
            "listo_para_ofrecer",
            "listo_para_ofrecer_display",
            "fecha_modificacion",
        ]

    def get_objetivo_corto(self, obj):
        """Retorna una versión corta del objetivo para la lista"""
        if len(obj.objetivo) <= 100:
            return obj.objetivo
        return obj.objetivo[:100] + "..."
