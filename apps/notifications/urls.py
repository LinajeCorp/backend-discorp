from django.urls import path
from .views import (
    SendTestNotificationView,
    SendNotificationToUserView,
    SendBroadcastView
)

urlpatterns = [
    # Endpoint para pruebas (usuarios autenticados)
    path('test/', SendTestNotificationView.as_view(), name='send_test_notification'),
    
    # Endpoints para admins
    path('send-to-user/', SendNotificationToUserView.as_view(), name='send_to_user'),
    path('broadcast/', SendBroadcastView.as_view(), name='send_broadcast'),
]
