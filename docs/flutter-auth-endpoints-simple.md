# 🔐 Endpoints de Autenticación - Flutter Integration

## 📍 Base URL
```
https://backend-discrop-production.up.railway.app/api/v1/
```

---

## 🚀 **1. REGISTRO DE USUARIO**

### **Endpoint:**
```
POST /api/v1/users/
```

### **Headers:**
```json
{
  "Content-Type": "application/json"
}
```

### **Body (JSON a enviar):**
```json
{
  "username": "juan_perez",
  "email": "juan@ejemplo.com",
  "password": "mipassword123",
  "password_confirm": "mipassword123",
  "first_name": "Juan",
  "last_name": "Pérez",
  "direccion": "Av. Libertador, Caracas, Venezuela",
  "tipo_documento": "V",
  "documento": "12345678"
}
```

### **Respuesta Exitosa (201):**
```json
{
  "id": 1,
  "username": "juan_perez",
  "email": "juan@ejemplo.com",
  "first_name": "Juan",
  "last_name": "Pérez",
  "direccion": "Av. Libertador, Caracas, Venezuela",
  "tipo_documento": "V",
  "documento": "12345678",
  "documento_completo": "V-12345678",
  "is_active": true,
  "date_joined": "2025-09-08T17:30:00Z"
}
```

### **Respuesta de Error (400):**
```json
{
  "username": ["Este nombre de usuario ya existe"],
  "email": ["Ingrese un email válido"],
  "password_confirm": ["Las contraseñas no coinciden"],
  "documento": ["Este documento ya está registrado"]
}
```

---

## 🔑 **2. LOGIN (Obtener Tokens)**

### **Endpoint:**
```
POST /api/v1/auth/login/
```

### **Headers:**
```json
{
  "Content-Type": "application/json"
}
```

### **Body (JSON a enviar):**
```json
{
  "username": "juan_perez",
  "password": "mipassword123"
}
```

### **Respuesta Exitosa (200):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjMwNTg5...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYzMDY3...",
  "user": {
    "id": 1,
    "username": "juan_perez",
    "email": "juan@ejemplo.com",
    "first_name": "Juan",
    "last_name": "Pérez",
    "documento_completo": "V-12345678",
    "is_staff": false
  }
}
```

### **Respuesta de Error (401):**
```json
{
  "detail": "No active account found with the given credentials"
}
```

---

## 🔄 **3. RENOVAR TOKEN**

### **Endpoint:**
```
POST /api/v1/auth/refresh/
```

### **Headers:**
```json
{
  "Content-Type": "application/json"
}
```

### **Body (JSON a enviar):**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYzMDY3..."
}
```

### **Respuesta Exitosa (200):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjMwNTg5..."
}
```

---

## 👤 **4. OBTENER PERFIL DEL USUARIO**

### **Endpoint:**
```
GET /api/v1/users/profile/
```

### **Headers:**
```json
{
  "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "Content-Type": "application/json"
}
```

### **Body:**
```
No requiere body
```

### **Respuesta Exitosa (200):**
```json
{
  "id": 1,
  "username": "juan_perez",
  "email": "juan@ejemplo.com",
  "first_name": "Juan",
  "last_name": "Pérez",
  "full_name": "Juan Pérez",
  "direccion": "Av. Libertador, Caracas, Venezuela",
  "tipo_documento": "V",
  "documento": "12345678",
  "documento_completo": "V-12345678",
  "is_active": true,
  "is_staff": false,
  "date_joined": "2025-09-08T17:30:00Z",
  "last_login": "2025-09-08T18:15:00Z"
}
```

---

## ⚙️ **5. ACTUALIZAR PERFIL**

### **Endpoint:**
```
PATCH /api/v1/users/update_profile/
```

### **Headers:**
```json
{
  "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "Content-Type": "application/json"
}
```

### **Body (JSON a enviar - solo los campos a actualizar):**
```json
{
  "first_name": "Juan Carlos",
  "last_name": "Pérez González",
  "direccion": "Nueva dirección en Venezuela",
  "email": "nuevo_email@ejemplo.com"
}
```

### **Respuesta Exitosa (200):**
```json
{
  "id": 1,
  "username": "juan_perez",
  "email": "nuevo_email@ejemplo.com",
  "first_name": "Juan Carlos",
  "last_name": "Pérez González",
  "full_name": "Juan Carlos Pérez González",
  "direccion": "Nueva dirección en Venezuela",
  "tipo_documento": "V",
  "documento": "12345678",
  "documento_completo": "V-12345678",
  "is_active": true,
  "is_staff": false,
  "date_joined": "2025-09-08T17:30:00Z",
  "last_login": "2025-09-08T18:15:00Z"
}
```

---

## 📋 **Campos Obligatorios**

### **Para Registro:**
- ✅ `username` (único)
- ✅ `email` (válido)
- ✅ `password` (mínimo 8 caracteres)
- ✅ `password_confirm` (debe coincidir con password)
- ✅ `first_name`
- ✅ `last_name`
- ✅ `direccion`
- ✅ `tipo_documento` (V, E, P, J, G)
- ✅ `documento` (solo números)

### **Para Login:**
- ✅ `username`
- ✅ `password`

---

## 🏷️ **Tipos de Documento Válidos:**
- **V** = Cédula de Identidad Venezolana
- **E** = Extranjero
- **P** = Pasaporte
- **J** = RIF Jurídico (Empresas)
- **G** = RIF Gubernamental

---

## ⚠️ **Códigos de Estado HTTP:**
- **200** = Éxito
- **201** = Creado exitosamente
- **400** = Datos inválidos
- **401** = No autorizado / Credenciales incorrectas
- **404** = No encontrado
- **500** = Error del servidor

---

## 💾 **Qué Guardar en Flutter:**
```dart
// Después del login exitoso, guarda:
String accessToken = response['access'];
String refreshToken = response['refresh'];
Map<String, dynamic> userData = response['user'];

// Usar accessToken en headers para requests autenticados:
// Authorization: Bearer $accessToken
```

**¡Eso es todo lo que necesitas para integrar la autenticación!** 🚀
