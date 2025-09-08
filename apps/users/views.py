from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import get_user_model
from django.db import models

from .models import User
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    CustomTokenObtainPairSerializer,
    UserProfileSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión completa de usuarios venezolanos
    
    Proporciona operaciones CRUD para usuarios con campos personalizados
    para empresas en Venezuela (dirección, tipo de documento, documento).
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        """Seleccionar serializer según la acción"""
        if self.action == 'create':
            return UserRegistrationSerializer
        elif self.action == 'profile':
            return UserProfileSerializer
        return UserSerializer

    def get_permissions(self):
        """Permisos personalizados según la acción"""
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        
        return [permission() for permission in permission_classes]

    @swagger_auto_schema(
        operation_description="Obtener lista de usuarios registrados",
        manual_parameters=[
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Buscar por username, nombre, apellido o documento",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'tipo_documento',
                openapi.IN_QUERY,
                description="Filtrar por tipo de documento (V, E, P, J, G)",
                type=openapi.TYPE_STRING,
                enum=['V', 'E', 'P', 'J', 'G']
            ),
            openapi.Parameter(
                'is_active',
                openapi.IN_QUERY,
                description="Filtrar usuarios activos/inactivos",
                type=openapi.TYPE_BOOLEAN
            )
        ],
        responses={
            200: UserSerializer(many=True),
            401: "No autenticado"
        },
        tags=['Usuarios']
    )
    def list(self, request):
        """Listar usuarios con filtros opcionales"""
        queryset = self.get_queryset()
        
        # Filtros
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(username__icontains=search) |
                models.Q(first_name__icontains=search) |
                models.Q(last_name__icontains=search) |
                models.Q(documento__icontains=search)
            )
        
        tipo_documento = request.query_params.get('tipo_documento')
        if tipo_documento:
            queryset = queryset.filter(tipo_documento=tipo_documento)
            
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Registrar un nuevo usuario venezolano",
        request_body=UserRegistrationSerializer,
        responses={
            201: openapi.Response(
                description="Usuario creado exitosamente",
                schema=UserSerializer
            ),
            400: openapi.Response(
                description="Datos inválidos",
                examples={
                    "application/json": {
                        "username": ["Este campo es requerido"],
                        "password_confirm": ["Las contraseñas no coinciden"],
                        "documento": ["Este documento ya está registrado"]
                    }
                }
            )
        },
        tags=['Usuarios']
    )
    def create(self, request):
        """Crear un nuevo usuario con validación venezolana"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user_data = UserSerializer(user).data
            return Response(user_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Obtener detalles de un usuario específico",
        responses={
            200: UserSerializer,
            404: "Usuario no encontrado",
            401: "No autenticado"
        },
        tags=['Usuarios']
    )
    def retrieve(self, request, pk=None):
        """Obtener detalles de un usuario"""
        return super().retrieve(request, pk)

    @swagger_auto_schema(
        operation_description="Actualizar completamente un usuario",
        request_body=UserSerializer,
        responses={
            200: UserSerializer,
            400: "Datos inválidos",
            404: "Usuario no encontrado",
            403: "Sin permisos"
        },
        tags=['Usuarios']
    )
    def update(self, request, pk=None):
        """Actualizar usuario completo"""
        return super().update(request, pk)

    @swagger_auto_schema(
        operation_description="Actualizar parcialmente un usuario",
        request_body=UserSerializer,
        responses={
            200: UserSerializer,
            400: "Datos inválidos",
            404: "Usuario no encontrado",
            403: "Sin permisos"
        },
        tags=['Usuarios']
    )
    def partial_update(self, request, pk=None):
        """Actualizar usuario parcial"""
        return super().partial_update(request, pk)

    @swagger_auto_schema(
        operation_description="Eliminar un usuario",
        responses={
            204: "Usuario eliminado exitosamente",
            404: "Usuario no encontrado",
            403: "Sin permisos"
        },
        tags=['Usuarios']
    )
    def destroy(self, request, pk=None):
        """Eliminar usuario"""
        return super().destroy(request, pk)

    @swagger_auto_schema(
        method='get',
        operation_description="Obtener perfil del usuario autenticado",
        responses={
            200: UserProfileSerializer,
            401: "No autenticado"
        },
        tags=['Usuarios']
    )
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def profile(self, request):
        """Obtener perfil del usuario actual"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @swagger_auto_schema(
        method='patch',
        operation_description="Actualizar perfil del usuario autenticado",
        request_body=UserProfileSerializer,
        responses={
            200: UserProfileSerializer,
            400: "Datos inválidos",
            401: "No autenticado"
        },
        tags=['Usuarios']
    )
    @action(detail=False, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def update_profile(self, request):
        """Actualizar perfil del usuario actual"""
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Vista personalizada para obtener tokens JWT con información del usuario venezolano
    """
    serializer_class = CustomTokenObtainPairSerializer

    @swagger_auto_schema(
        operation_description="Autenticación JWT - Obtener tokens de acceso y refresh",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Nombre de usuario'
                ),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Contraseña del usuario'
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="Tokens JWT obtenidos exitosamente",
                examples={
                    "application/json": {
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "user": {
                            "id": 1,
                            "username": "usuario_ejemplo",
                            "email": "usuario@ejemplo.com",
                            "first_name": "Juan",
                            "last_name": "Pérez",
                            "documento_completo": "V-12345678",
                            "is_staff": False
                        }
                    }
                }
            ),
            401: openapi.Response(
                description="Credenciales inválidas",
                examples={
                    "application/json": {
                        "detail": "No active account found with the given credentials"
                    }
                }
            )
        },
        tags=['Autenticación']
    )
    def post(self, request, *args, **kwargs):
        """Autenticar usuario y obtener tokens JWT"""
        return super().post(request, *args, **kwargs)
