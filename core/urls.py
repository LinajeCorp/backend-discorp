"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator

# FCM Django ViewSets
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

# Router para FCM Django
fcm_router = DefaultRouter()
fcm_router.register('devices', FCMDeviceAuthorizedViewSet, basename='fcm_device')


class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["http", "https"]
        return schema


# Schema view configuration for drf-yasg
schema_view = get_schema_view(
    openapi.Info(
        title="discorp API",
        default_version="v1",
        description="API REST para el sistema de delivery de comida discorp "
        "con usuarios multi-rol",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(
            name="Equipo de Desarrollo discorp", email="dev@discorp.com"
        ),
        license=openapi.License(name="MIT License"),
        schemes=["http", "https"],
    ),
    generator_class=BothHttpAndHttpsSchemaGenerator,
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # URL personalizada DEBE ir antes del admin
    path("admin/", admin.site.urls),
    # API URLs
    path("api/v1/", include("apps.users.urls")),
    path("api/v1/", include("apps.products.urls")),
    # FCM Django URLs para notificaciones
    path("api/v1/fcm/", include(fcm_router.urls)),
    # Endpoints personalizados para notificaciones
    path("api/v1/notifications/", include("apps.notifications.urls")),
    # drf-yasg Swagger/OpenAPI URLs
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
