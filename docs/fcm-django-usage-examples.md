# 🔔 FCM Django - Ejemplos de Uso

## 📋 Configuración Completada

✅ **fcm-django** está configurado correctamente según la [documentación oficial](https://fcm-django.readthedocs.io/en/latest/)

### Dependencias instaladas:
- `fcm-django>=2.0.0`
- `firebase-admin>=6.2.0`

### Configuración en `settings.py`:
```python
INSTALLED_APPS = [
    # ... otras apps
    "fcm_django",  # FCM Django para notificaciones push
    # ...
]

# Firebase Configuration con fcm-django
FIREBASE_APP = initialize_app()

# Configuración FCM Django
FCM_DJANGO_SETTINGS = {
    "DEFAULT_FIREBASE_APP": FIREBASE_APP,
    "APP_VERBOSE_NAME": "Discorp FCM",
    "ONE_DEVICE_PER_USER": False,
    "DELETE_INACTIVE_DEVICES": True,
}
```

### URLs configuradas:
```python
# En core/urls.py
path("api/v1/fcm/", include(fcm_router.urls)),
```

---

## 🚀 Endpoints Disponibles

### 1. Registrar Dispositivo
```bash
POST /api/v1/fcm/devices/
```

**Headers:**
```
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: application/json
```

**Body:**
```json
{
    "registration_id": "FIREBASE_TOKEN_DEL_DISPOSITIVO",
    "type": "android",
    "name": "Mi Teléfono Android"
}
```

### 2. Listar Dispositivos del Usuario
```bash
GET /api/v1/fcm/devices/
Authorization: Bearer YOUR_JWT_TOKEN
```

### 3. Actualizar Dispositivo
```bash
PUT /api/v1/fcm/devices/{id}/
Authorization: Bearer YOUR_JWT_TOKEN
```

---

## 📱 Enviar Notificaciones desde Django

### 1. Enviar a un Usuario Específico

```python
# En Django shell o en tus views
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification

# Obtener dispositivos del usuario
user_devices = FCMDevice.objects.filter(user=user, active=True)

# Crear mensaje
message = Message(
    notification=Notification(
        title="¡Hola desde Django!",
        body="Esta es una notificación de prueba",
        image="https://example.com/image.png"
    ),
    data={
        "type": "test",
        "action": "open_app",
        "extra_data": "valor_personalizado"
    }
)

# Enviar notificación
user_devices.send_message(message)
```

### 2. Enviar a Todos los Usuarios

```python
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification

# Obtener todos los dispositivos activos
all_devices = FCMDevice.objects.filter(active=True)

# Crear mensaje
message = Message(
    notification=Notification(
        title="🎉 Anuncio Importante",
        body="¡Nueva función disponible en la app!"
    ),
    data={
        "type": "announcement",
        "action": "open_features"
    }
)

# Enviar a todos
all_devices.send_message(message)
```

### 3. Enviar Solo Datos (Sin Notificación Visual)

```python
from firebase_admin.messaging import Message

# Solo datos, sin notificación visual
message = Message(
    data={
        "type": "silent_update",
        "new_data": "actualizar_cache",
        "timestamp": str(timezone.now())
    }
)

FCMDevice.objects.filter(user=user).send_message(message)
```

---

## 🔧 Ejemplos en Views de Django

### 1. View para Enviar Notificación

```python
# En tus views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification

class SendNotificationView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            # Obtener datos del request
            title = request.data.get('title')
            body = request.data.get('body')
            data = request.data.get('data', {})
            
            # Obtener dispositivos del usuario
            user_devices = FCMDevice.objects.filter(
                user=request.user, 
                active=True
            )
            
            if not user_devices.exists():
                return Response(
                    {"error": "No hay dispositivos registrados"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Crear mensaje
            message = Message(
                notification=Notification(title=title, body=body),
                data=data
            )
            
            # Enviar notificación
            user_devices.send_message(message)
            
            return Response({
                "message": f"Notificación enviada a {user_devices.count()} dispositivos"
            })
            
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
```

### 2. Notificación Automática al Crear Pedido

```python
# En tu view de crear pedido
from django.db.models.signals import post_save
from django.dispatch import receiver
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification

@receiver(post_save, sender=Order)
def send_order_notification(sender, instance, created, **kwargs):
    if created:
        # Notificar al usuario que hizo el pedido
        user_devices = FCMDevice.objects.filter(
            user=instance.user, 
            active=True
        )
        
        if user_devices.exists():
            message = Message(
                notification=Notification(
                    title="🍕 Pedido Confirmado",
                    body=f"Tu pedido #{instance.id} ha sido confirmado"
                ),
                data={
                    "type": "order_confirmed",
                    "order_id": str(instance.id),
                    "action": "open_order_details"
                }
            )
            
            user_devices.send_message(message)
```

---

## 🧪 Testing Manual

### 1. Django Shell

```bash
# Abrir Django shell
uv run ./manage.py shell

# En el shell de Python
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification
from django.contrib.auth import get_user_model

User = get_user_model()

# Crear un dispositivo de prueba (necesitas un token real de Firebase)
user = User.objects.first()
device = FCMDevice.objects.create(
    user=user,
    registration_id="TOKEN_REAL_DE_FIREBASE",
    type="android",
    name="Dispositivo de Prueba"
)

# Enviar notificación de prueba
message = Message(
    notification=Notification(
        title="🧪 Prueba desde Django",
        body="Si ves esto, ¡fcm-django funciona!"
    ),
    data={"test": "true"}
)

device.send_message(message)
```

### 2. Django Admin

1. Ve a `/admin/`
2. Busca la sección **FCM_DJANGO**
3. En **FCM devices** puedes:
   - Ver todos los dispositivos registrados
   - Seleccionar dispositivos y usar la acción "Send test message"
   - Enviar notificaciones de prueba masivas

### 3. API con cURL

```bash
# 1. Obtener JWT token
curl -X POST "http://localhost:8000/api/v1/auth/login/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "tu_usuario",
    "password": "tu_password"
  }'

# 2. Registrar dispositivo
curl -X POST "http://localhost:8000/api/v1/fcm/devices/" \
  -H "Authorization: Bearer TU_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "registration_id": "TOKEN_DE_FIREBASE",
    "type": "android",
    "name": "Mi Dispositivo"
  }'

# 3. Ver dispositivos registrados
curl -X GET "http://localhost:8000/api/v1/fcm/devices/" \
  -H "Authorization: Bearer TU_JWT_TOKEN"
```

---

## 🎯 Casos de Uso Comunes

### 1. Notificación de Nuevo Pedido

```python
def notify_new_order(order):
    user_devices = FCMDevice.objects.filter(user=order.user, active=True)
    
    message = Message(
        notification=Notification(
            title="🍕 Nuevo Pedido",
            body=f"Pedido #{order.id} de {order.restaurant.name}"
        ),
        data={
            "type": "new_order",
            "order_id": str(order.id),
            "restaurant_id": str(order.restaurant.id),
            "action": "open_order_details"
        }
    )
    
    user_devices.send_message(message)
```

### 2. Actualización de Estado

```python
def notify_order_status_change(order, new_status):
    status_messages = {
        'preparing': '👨‍🍳 Tu pedido se está preparando',
        'ready': '🎉 ¡Tu pedido está listo!',
        'delivered': '🚚 Pedido entregado'
    }
    
    user_devices = FCMDevice.objects.filter(user=order.user, active=True)
    
    message = Message(
        notification=Notification(
            title="Actualización de Pedido",
            body=status_messages.get(new_status, f"Estado: {new_status}")
        ),
        data={
            "type": "order_status_update",
            "order_id": str(order.id),
            "status": new_status,
            "action": "open_order_details"
        }
    )
    
    user_devices.send_message(message)
```

### 3. Promociones

```python
def send_promotion_notification(users_queryset, title, description, promo_code=None):
    # Obtener todos los dispositivos de los usuarios seleccionados
    devices = FCMDevice.objects.filter(
        user__in=users_queryset,
        active=True
    )
    
    data = {
        "type": "promotion",
        "action": "open_promotions"
    }
    
    if promo_code:
        data["promo_code"] = promo_code
    
    message = Message(
        notification=Notification(
            title=f"🎁 {title}",
            body=description
        ),
        data=data
    )
    
    devices.send_message(message)
```

---

## 📚 Recursos Adicionales

### Documentación Oficial
- [FCM Django Docs](https://fcm-django.readthedocs.io/en/latest/)
- [Firebase Admin SDK](https://firebase.google.com/docs/admin/setup)
- [Firebase Cloud Messaging](https://firebase.google.com/docs/cloud-messaging)

### Configuración Flutter
Para recibir las notificaciones en Flutter, necesitarás:
1. Configurar Firebase en tu app Flutter
2. Obtener el token FCM del dispositivo
3. Registrar el token usando el endpoint `/api/v1/fcm/devices/`
4. Manejar las notificaciones recibidas

¡Con esta configuración ya puedes enviar notificaciones push desde Django! 🚀
