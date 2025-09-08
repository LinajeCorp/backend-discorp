from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import UserViewSet, CustomTokenObtainPairView

# Router para el ViewSet de usuarios
router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    # URLs del router (CRUD de usuarios)
    path('', include(router.urls)),
    
    # URLs de autenticación JWT
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
