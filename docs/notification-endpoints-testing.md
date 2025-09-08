# 🔔 Endpoints de Notificaciones - Guía de Pruebas

## 📋 Endpoints Creados

### ✅ Configuración Completada:
- **fcm-django** configurado y funcionando
- **Firebase** conectado correctamente
- **Endpoints personalizados** para pruebas creados

---

## 🚀 Endpoints Disponibles

### 1. **Notificación de Prueba** (Usuario Autenticado)
```
POST /api/v1/notifications/test/
```

**Descripción:** Envía una notificación de prueba a todos los dispositivos del usuario autenticado.

**Headers:**
```
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: application/json
```

**Body (ejemplo):**
```json
{
    "title": "🧪 Mi Prueba",
    "body": "Esta es una notificación de prueba",
    "data": {
        "type": "test",
        "action": "open_app",
        "custom_data": "valor_personalizado"
    }
}
```

**Respuesta exitosa:**
```json
{
    "success": true,
    "message": "Notificación enviada a 2 dispositivos",
    "devices_count": 2
}
```

---

### 2. **Enviar a Usuario Específico** (Solo Admins)
```
POST /api/v1/notifications/send-to-user/
```

**Descripción:** Los administradores pueden enviar notificaciones a usuarios específicos.

**Headers:**
```
Authorization: Bearer ADMIN_JWT_TOKEN
Content-Type: application/json
```

**Body (ejemplo):**
```json
{
    "username": "usuario_destino",
    "title": "📢 Mensaje del Admin",
    "body": "Te enviamos esta notificación importante",
    "data": {
        "type": "admin_message",
        "action": "open_notifications"
    }
}
```

**O usando user_id:**
```json
{
    "user_id": 123,
    "title": "📢 Mensaje del Admin",
    "body": "Te enviamos esta notificación importante"
}
```

---

### 3. **Broadcast** (Solo Admins)
```
POST /api/v1/notifications/broadcast/
```

**Descripción:** Envía notificación a todos los usuarios con dispositivos activos.

**Headers:**
```
Authorization: Bearer ADMIN_JWT_TOKEN
Content-Type: application/json
```

**Body (ejemplo):**
```json
{
    "title": "🎉 Anuncio General",
    "body": "¡Nueva funcionalidad disponible en la app!",
    "data": {
        "type": "broadcast",
        "action": "open_features",
        "version": "2.0"
    }
}
```

---

## 🧪 Cómo Probar

### 1. **Registrar un Dispositivo Primero**

Antes de enviar notificaciones, necesitas registrar un dispositivo:

```bash
# 1. Obtener JWT Token
curl -X POST "http://localhost:8000/api/v1/auth/login/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "tu_usuario",
    "password": "tu_password"
  }'

# 2. Registrar dispositivo (necesitas un token FCM real de Firebase)
curl -X POST "http://localhost:8000/api/v1/fcm/devices/" \
  -H "Authorization: Bearer TU_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "registration_id": "TOKEN_FCM_DE_FIREBASE",
    "type": "android",
    "name": "Mi Dispositivo de Prueba"
  }'
```

### 2. **Enviar Notificación de Prueba**

```bash
curl -X POST "http://localhost:8000/api/v1/notifications/test/" \
  -H "Authorization: Bearer TU_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "🧪 Prueba desde cURL",
    "body": "Si ves esto, ¡funciona perfectamente!",
    "data": {
      "type": "curl_test",
      "action": "celebrate"
    }
  }'
```

### 3. **Probar desde Django Shell**

```python
# Abrir shell
uv run ./manage.py shell

# En Python
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification
from django.contrib.auth import get_user_model

User = get_user_model()

# Verificar dispositivos registrados
devices = FCMDevice.objects.all()
print(f"Dispositivos registrados: {devices.count()}")

for device in devices:
    print(f"- {device.user.username}: {device.type} ({device.name})")

# Enviar prueba manual
if devices.exists():
    message = Message(
        notification=Notification(
            title="🧪 Prueba desde Shell",
            body="Enviado directamente desde Django shell"
        ),
        data={"source": "django_shell"}
    )
    
    devices.send_message(message)
    print("¡Notificación enviada!")
```

---

## 🎯 Testing con Swagger UI

1. Ve a: `http://localhost:8000/docs/`
2. Busca la sección **"Notificaciones"**
3. Haz clic en **"Try it out"** en cualquier endpoint
4. Rellena los campos y ejecuta

**Los endpoints aparecerán documentados automáticamente en Swagger** gracias a los decoradores `@swagger_auto_schema`.

---

## 📱 ¿Cómo Obtener un Token FCM Real?

### Para Testing Rápido:
1. **Usa Firebase Console:**
   - Ve a tu proyecto Firebase
   - Cloud Messaging → Send test message
   - Agrega un token de prueba

2. **Desde una App Flutter:**
   ```dart
   import 'package:firebase_messaging/firebase_messaging.dart';
   
   // Obtener token
   String? token = await FirebaseMessaging.instance.getToken();
   print('FCM Token: $token');
   ```

3. **Desde JavaScript (Web):**
   ```javascript
   import { getMessaging, getToken } from "firebase/messaging";
   
   const messaging = getMessaging();
   getToken(messaging, { vapidKey: 'TU_VAPID_KEY' }).then((currentToken) => {
     console.log('FCM Token:', currentToken);
   });
   ```

---

## 🔍 Debugging

### Verificar Configuración:
```bash
# Verificar que Firebase esté configurado
uv run ./manage.py shell -c "
from fcm_django.models import FCMDevice
print('FCM Django funcionando:', FCMDevice.objects.count() >= 0)
"
```

### Ver Logs:
```bash
# Ejecutar servidor con logs detallados
uv run ./manage.py runserver --verbosity=2
```

### Errores Comunes:

1. **"Authentication credentials were not provided"**
   - Necesitas estar autenticado con JWT
   - Incluye el header `Authorization: Bearer TOKEN`

2. **"No tienes dispositivos registrados"**
   - Primero registra un dispositivo en `/api/v1/fcm/devices/`
   - Necesitas un token FCM real de Firebase

3. **"Error enviando notificación"**
   - Verifica que Firebase esté configurado correctamente
   - Revisa que el token FCM sea válido

---

## 🚀 Próximos Pasos

Una vez que tengas las notificaciones funcionando:

1. **Integra en tu Flutter App:**
   - Configura Firebase en Flutter
   - Registra el token FCM automáticamente
   - Maneja las notificaciones recibidas

2. **Automatiza Notificaciones:**
   - Conecta con signals de Django
   - Envía notificaciones automáticas en eventos (nuevo pedido, etc.)

3. **Personaliza por Usuario:**
   - Segmenta usuarios
   - Envía notificaciones basadas en preferencias

**¡Tu sistema de notificaciones push está listo para usar!** 🎉
