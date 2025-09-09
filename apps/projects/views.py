from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Project
from .serializers import (
    ProjectSerializer, 
    ProjectCreateSerializer, 
    ProjectUpdateSerializer,
    ProjectListSerializer
)


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar proyectos de la empresa
    
    Permite realizar operaciones CRUD sobre los proyectos y
    proporciona filtros y búsqueda avanzada.
    """
    
    queryset = Project.objects.all()
    permission_classes = [AllowAny]  # Temporal para testing
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['fase', 'status', 'prioridad', 'listo_para_ofrecer']
    search_fields = ['nombre', 'objetivo', 'ultima_actualizacion']
    ordering_fields = ['nombre', 'fecha_creacion', 'fecha_modificacion']
    ordering = ['nombre']
    
    def get_serializer_class(self):
        """Retorna el serializer apropiado según la acción"""
        if self.action == 'list':
            return ProjectListSerializer
        elif self.action == 'create':
            return ProjectCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ProjectUpdateSerializer
        return ProjectSerializer
    
    @swagger_auto_schema(
        operation_description="Obtener lista de todos los proyectos",
        manual_parameters=[
            openapi.Parameter(
                'fase', 
                openapi.IN_QUERY,
                description="Filtrar por fase (ejecucion, completado, pausado)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'status', 
                openapi.IN_QUERY,
                description="Filtrar por status (en_curso, en_seguimiento, pausado)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'prioridad', 
                openapi.IN_QUERY,
                description="Filtrar por prioridad (normal, alta, baja)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'listo_para_ofrecer', 
                openapi.IN_QUERY,
                description="Filtrar por disponibilidad (si, no)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'search', 
                openapi.IN_QUERY,
                description="Buscar en nombre, objetivo o última actualización",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'ordering', 
                openapi.IN_QUERY,
                description="Ordenar por campo (nombre, fecha_creacion, fecha_modificacion)",
                type=openapi.TYPE_STRING
            ),
        ],
        responses={200: ProjectListSerializer(many=True)},
        tags=['Proyectos']
    )
    def list(self, request, *args, **kwargs):
        """Listar todos los proyectos con filtros y búsqueda"""
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Obtener detalles de un proyecto específico",
        responses={
            200: ProjectSerializer,
            404: "Proyecto no encontrado"
        },
        tags=['Proyectos']
    )
    def retrieve(self, request, *args, **kwargs):
        """Obtener detalles de un proyecto específico"""
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Crear un nuevo proyecto",
        request_body=ProjectCreateSerializer,
        responses={
            201: ProjectSerializer,
            400: "Datos inválidos"
        },
        tags=['Proyectos']
    )
    def create(self, request, *args, **kwargs):
        """Crear un nuevo proyecto"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualizar completamente un proyecto",
        request_body=ProjectUpdateSerializer,
        responses={
            200: ProjectSerializer,
            400: "Datos inválidos",
            404: "Proyecto no encontrado"
        },
        tags=['Proyectos']
    )
    def update(self, request, *args, **kwargs):
        """Actualizar completamente un proyecto"""
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualizar parcialmente un proyecto",
        request_body=ProjectUpdateSerializer,
        responses={
            200: ProjectSerializer,
            400: "Datos inválidos",
            404: "Proyecto no encontrado"
        },
        tags=['Proyectos']
    )
    def partial_update(self, request, *args, **kwargs):
        """Actualizar parcialmente un proyecto"""
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Eliminar un proyecto",
        responses={
            204: "Proyecto eliminado exitosamente",
            404: "Proyecto no encontrado"
        },
        tags=['Proyectos']
    )
    def destroy(self, request, *args, **kwargs):
        """Eliminar un proyecto"""
        return super().destroy(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Obtener estadísticas de proyectos",
        responses={
            200: openapi.Response(
                description="Estadísticas de proyectos",
                examples={
                    "application/json": {
                        "total_proyectos": 12,
                        "por_fase": {
                            "ejecucion": 5,
                            "completado": 6,
                            "pausado": 1
                        },
                        "por_status": {
                            "en_curso": 4,
                            "en_seguimiento": 6,
                            "pausado": 2
                        },
                        "por_prioridad": {
                            "normal": 8,
                            "alta": 4,
                            "baja": 0
                        },
                        "listos_para_ofrecer": 5,
                        "no_listos_para_ofrecer": 7
                    }
                }
            )
        },
        tags=['Proyectos']
    )
    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """Obtener estadísticas generales de proyectos"""
        total_proyectos = Project.objects.count()
        
        # Estadísticas por fase
        por_fase = {}
        for fase_value, fase_label in Project.FASE_CHOICES:
            por_fase[fase_value] = Project.objects.filter(fase=fase_value).count()
        
        # Estadísticas por status
        por_status = {}
        for status_value, status_label in Project.STATUS_CHOICES:
            por_status[status_value] = Project.objects.filter(status=status_value).count()
        
        # Estadísticas por prioridad
        por_prioridad = {}
        for prioridad_value, prioridad_label in Project.PRIORIDAD_CHOICES:
            por_prioridad[prioridad_value] = Project.objects.filter(prioridad=prioridad_value).count()
        
        # Estadísticas de disponibilidad
        listos_para_ofrecer = Project.objects.filter(listo_para_ofrecer='si').count()
        no_listos_para_ofrecer = Project.objects.filter(listo_para_ofrecer='no').count()
        
        estadisticas = {
            'total_proyectos': total_proyectos,
            'por_fase': por_fase,
            'por_status': por_status,
            'por_prioridad': por_prioridad,
            'listos_para_ofrecer': listos_para_ofrecer,
            'no_listos_para_ofrecer': no_listos_para_ofrecer,
        }
        
        return Response(estadisticas, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Obtener solo proyectos listos para ofrecer",
        responses={200: ProjectListSerializer(many=True)},
        tags=['Proyectos']
    )
    @action(detail=False, methods=['get'])
    def listos_para_ofrecer(self, request):
        """Obtener solo los proyectos que están listos para ofrecer"""
        proyectos = self.get_queryset().filter(listo_para_ofrecer='si')
        serializer = ProjectListSerializer(proyectos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
