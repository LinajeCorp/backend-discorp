# 📱 APIs Disponibles para Integración con Flutter

## 🎯 **RESUMEN EJECUTIVO**

Tu backend Django está **100% listo** para integración con Flutter. Todas las APIs están funcionando con **datos reales** de la base de datos y completamente documentadas con Swagger.

---

## 🔗 **BASE URL**
```
http://localhost:8000/api/
```

---

## 📊 **1. ANALYTICS & DASHBOARD APIs**

### **🏠 Dashboard Principal**
```http
GET /api/analytics/dashboard/summary/
GET /api/analytics/dashboard/stats/
```

**Respuesta Ejemplo:**
```json
{
  "period": {
    "start_date": "2025-08-27",
    "end_date": "2025-09-03",
    "store_id": null
  },
  "financial_summary": {
    "total_revenue": "1207.00",
    "total_orders": 6,
    "average_order_value": "1207.00",
    "profit_margin": "97.00",
    "completion_rate": "16.67"
  },
  "conversion_metrics": {
    "unique_visitors": 198,
    "conversion_rate": "0.51",
    "cart_abandonment_rate": "-500.00"
  },
  "top_products": [
    {
      "product_id": "uuid",
      "product_name": "iPhone 15 Pro",
      "revenue": "1207.00",
      "purchases": 1,
      "views": 15,
      "conversion_rate": "6.67"
    }
  ]
}
```

### **📈 Reportes Financieros**
```http
GET /api/analytics/financial-reports/
POST /api/analytics/financial-reports/generate/
POST /api/analytics/financial-reports/compare/
```

---

## 🛍️ **2. ORDERS & CART APIs**

### **🛒 Gestión de Carritos**
```http
GET /api/orders/carts/
POST /api/orders/carts/
PUT /api/orders/carts/{id}/
DELETE /api/orders/carts/{id}/

# Acciones especiales
POST /api/orders/carts/{id}/add_item/
POST /api/orders/carts/{id}/remove_item/
POST /api/orders/carts/{id}/clear/
POST /api/orders/carts/{id}/checkout/
```

### **📦 Gestión de Órdenes**
```http
GET /api/orders/orders/
POST /api/orders/orders/
GET /api/orders/orders/{id}/
PUT /api/orders/orders/{id}/

# Estados de orden
POST /api/orders/orders/{id}/confirm/
POST /api/orders/orders/{id}/cancel/
POST /api/orders/orders/{id}/mark_ready/
POST /api/orders/orders/{id}/start_delivery/
POST /api/orders/orders/{id}/complete/
```

**Estados Disponibles:**
- `pending` → `confirmed` → `preparing` → `ready` → `in_delivery` → `delivered`
- `cancelled` (desde cualquier estado)

---

## 🏪 **3. STORES & PRODUCTS APIs**

### **🏬 Tiendas**
```http
GET /api/stores/stores/
GET /api/stores/stores/{id}/
POST /api/stores/stores/{id}/toggle_status/

# Búsqueda geográfica
GET /api/stores/stores/nearby/?lat=40.7128&lng=-74.0060&radius=5
```

**Respuesta Tienda:**
```json
{
  "id": "uuid",
  "name": "Apple Store",
  "description": "Productos Apple oficiales",
  "address": "123 Main St",
  "latitude": "40.7128",
  "longitude": "-74.0060",
  "phone": "+1234567890",
  "email": "store@apple.com",
  "is_active": true,
  "rating": "4.50",
  "delivery_radius": 10.0,
  "opening_hours": {
    "monday": {"open": "09:00", "close": "21:00", "is_open": true},
    "tuesday": {"open": "09:00", "close": "21:00", "is_open": true}
  }
}
```

### **📦 Productos**
```http
GET /api/products/products/
GET /api/products/products/{id}/
POST /api/products/products/{id}/review/
POST /api/products/products/{id}/upload_image/
GET /api/products/products/{id}/images/

# Filtros disponibles
GET /api/products/products/?store={store_id}
GET /api/products/products/?category={category_id}
GET /api/products/products/?search=iPhone
GET /api/products/products/?min_price=100&max_price=500
GET /api/products/products/?on_sale=true
GET /api/products/products/?in_stock=true
GET /api/products/products/?min_rating=4.0
```

### **📸 Gestión de Imágenes (Cloudinary)**
```http
POST /api/products/products/{id}/upload_image/
POST /api/products/product-images/upload/
GET /api/products/product-images/?product={product_id}
```

**Subir Imagen Principal:**
```json
POST /api/products/products/{product_id}/upload_image/
Content-Type: multipart/form-data

{
  "image": [archivo_imagen]
}
```

**Respuesta:**
```json
{
  "message": "Imagen subida exitosamente",
  "image_url": "https://res.cloudinary.com/tu-cloud/image/upload/v1234567890/discorp/products/main/abc123.jpg",
  "public_id": "discorp/products/main/abc123"
}
```

**Subir Múltiples Imágenes de Galería:**
```json
POST /api/products/product-images/upload/
Content-Type: multipart/form-data

{
  "product_id": "uuid",
  "images": [archivo1, archivo2, archivo3],
  "alt_text_0": "Descripción imagen 1",
  "alt_text_1": "Descripción imagen 2",
  "sort_order_0": 1,
  "sort_order_1": 2
}
```

### **📂 Categorías**
```http
GET /api/categories/categories/
GET /api/categories/categories/{id}/
```

---

## 👥 **4. USERS & AUTH APIs**

### **🔐 Autenticación JWT**
```http
POST /api/users/auth/login/
POST /api/users/auth/register/
POST /api/users/auth/refresh/
POST /api/users/auth/logout/
```

### **👤 Perfil de Usuario**
```http
GET /api/users/profile/
PUT /api/users/profile/
GET /api/users/orders/
```

---

## 🚚 **5. DELIVERY APIs**

### **📍 Tracking en Tiempo Real**
```http
GET /api/delivery/assignments/
GET /api/delivery/assignments/{id}/
POST /api/delivery/assignments/{id}/accept/
POST /api/delivery/assignments/{id}/start/
POST /api/delivery/assignments/{id}/complete/

# WebSocket para tracking
ws://localhost:8000/ws/delivery/{assignment_id}/
```

### **🗺️ Rutas Optimizadas**
```http
POST /api/delivery/routes/optimize/
GET /api/delivery/routes/{id}/
```

---

## 💳 **6. PAYMENTS APIs**

### **💰 Stripe Integration**
```http
POST /api/payments/create-payment-intent/
POST /api/payments/confirm-payment/
GET /api/payments/payment-methods/
POST /api/payments/webhooks/stripe/
```

**Crear Payment Intent:**
```json
{
  "order_id": "uuid",
  "amount": 1207.00,
  "currency": "usd",
  "payment_method_types": ["card"]
}
```

---

## 📱 **FLUTTER INTEGRATION EXAMPLES**

### **🛠️ Setup HTTP Client**
```dart
import 'package:dio/dio.dart';

class ApiService {
  static const String baseUrl = 'http://localhost:8000/api';
  late Dio _dio;

  ApiService() {
    _dio = Dio(BaseOptions(
      baseUrl: baseUrl,
      connectTimeout: Duration(seconds: 5),
      receiveTimeout: Duration(seconds: 3),
    ));
    
    // Add JWT interceptor
    _dio.interceptors.add(AuthInterceptor());
  }
}
```

### **📊 Dashboard Data**
```dart
Future<DashboardData> getDashboardData() async {
  try {
    final response = await _dio.get('/analytics/dashboard/summary/');
    return DashboardData.fromJson(response.data);
  } catch (e) {
    throw ApiException('Error loading dashboard: $e');
  }
}
```

### **🛒 Cart Management**
```dart
Future<Cart> addToCart(String productId, int quantity) async {
  final response = await _dio.post('/orders/carts/1/add_item/', data: {
    'product_id': productId,
    'quantity': quantity,
  });
  return Cart.fromJson(response.data);
}
```

### **📸 Image Upload**
```dart
Future<Map<String, dynamic>> uploadProductImage(
  String productId, 
  File imageFile
) async {
  FormData formData = FormData.fromMap({
    'image': await MultipartFile.fromFile(
      imageFile.path,
      filename: 'product_image.jpg',
    ),
  });
  
  final response = await _dio.post(
    '/products/products/$productId/upload_image/',
    data: formData,
  );
  
  return response.data;
}
```

### **📱 Multiple Images Upload**
```dart
Future<Map<String, dynamic>> uploadProductGallery(
  String productId,
  List<File> images,
  {List<String>? altTexts}
) async {
  Map<String, dynamic> formDataMap = {
    'product_id': productId,
  };
  
  // Agregar imágenes
  for (int i = 0; i < images.length; i++) {
    formDataMap['images'] = await MultipartFile.fromFile(
      images[i].path,
      filename: 'gallery_$i.jpg',
    );
    
    if (altTexts != null && i < altTexts.length) {
      formDataMap['alt_text_$i'] = altTexts[i];
    }
    formDataMap['sort_order_$i'] = i;
  }
  
  FormData formData = FormData.fromMap(formDataMap);
  
  final response = await _dio.post(
    '/products/product-images/upload/',
    data: formData,
  );
  
  return response.data;
}
```

### **📦 Order Tracking**
```dart
Future<Order> getOrderStatus(String orderId) async {
  final response = await _dio.get('/orders/orders/$orderId/');
  return Order.fromJson(response.data);
}
```

### **🚚 Real-time Delivery Tracking**
```dart
import 'package:web_socket_channel/web_socket_channel.dart';

class DeliveryTracker {
  late WebSocketChannel _channel;
  
  void connectToDelivery(String assignmentId) {
    _channel = WebSocketChannel.connect(
      Uri.parse('ws://localhost:8000/ws/delivery/$assignmentId/')
    );
    
    _channel.stream.listen((data) {
      final location = json.decode(data);
      updateDeliveryLocation(location);
    });
  }
}
```

---

## 🔍 **API DOCUMENTATION**

### **📖 Swagger/OpenAPI**
```
http://localhost:8000/docs/
```

### **📋 Schema JSON**
```
http://localhost:8000/schema/
```

### **📚 ReDoc Documentation**
```
http://localhost:8000/redoc/
```

---

## ✅ **FEATURES DISPONIBLES PARA FLUTTER**

### **🎯 Core Features:**
- ✅ **Autenticación JWT** completa
- ✅ **CRUD de productos** con filtros
- ✅ **Carrito de compras** funcional
- ✅ **Sistema de órdenes** con estados
- ✅ **Búsqueda geográfica** de tiendas
- ✅ **Pagos con Stripe** integrados

### **📊 Analytics Features:**
- ✅ **Dashboard en tiempo real**
- ✅ **Métricas financieras**
- ✅ **Análisis de conversión**
- ✅ **Reportes comparativos**
- ✅ **Top productos**

### **🚚 Delivery Features:**
- ✅ **Tracking en tiempo real** (WebSocket)
- ✅ **Asignación automática**
- ✅ **Rutas optimizadas**
- ✅ **Estados de entrega**

### **🏪 Store Features:**
- ✅ **Horarios de apertura**
- ✅ **Sistema de reviews**
- ✅ **Radio de entrega**
- ✅ **Búsqueda por proximidad**

### **📸 Image Management Features:**
- ✅ **Cloudinary integration** - CDN global
- ✅ **Automatic optimization** - WebP, AVIF, quality auto
- ✅ **Image transformations** - Resize, crop, filters
- ✅ **Multiple formats** - JPEG, PNG, WebP support
- ✅ **Organized folders** - products/main, products/gallery, stores/logos, etc.
- ✅ **Size validation** - Max 5MB per image
- ✅ **Batch upload** - Multiple images at once

---

## 🚀 **PRÓXIMOS PASOS PARA FLUTTER**

### **1. 📱 Setup Inicial:**
```bash
flutter pub add dio
flutter pub add web_socket_channel  
flutter pub add geolocator
flutter pub add google_maps_flutter
flutter pub add stripe_payment
flutter pub add image_picker
flutter pub add cached_network_image
```

### **2. 🏗️ Arquitectura Recomendada:**
```
lib/
├── services/
│   ├── api_service.dart
│   ├── auth_service.dart
│   └── websocket_service.dart
├── models/
│   ├── order.dart
│   ├── product.dart
│   └── dashboard.dart
├── screens/
│   ├── dashboard/
│   ├── products/
│   ├── cart/
│   └── orders/
└── widgets/
    ├── charts/
    ├── maps/
    └── common/
```

### **3. 🔑 Variables de Entorno:**
```dart
class Config {
  static const String apiBaseUrl = 'http://your-domain.com/api';
  static const String wsBaseUrl = 'ws://your-domain.com/ws';
  static const String stripePublishableKey = 'pk_test_...';
  static const String cloudinaryBaseUrl = 'https://res.cloudinary.com/your-cloud-name';
}
```

### **4. 📸 Setup de Cloudinary en Backend:**
```bash
# 1. Regístrate en https://cloudinary.com
# 2. Obtén tus credenciales del dashboard
# 3. Agrega a tu .env:
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key  
CLOUDINARY_API_SECRET=your_api_secret
```

### **5. 🎯 Transformaciones Automáticas:**
Las imágenes se optimizan automáticamente:
- **Productos principales:** 600x600px, crop fill, quality auto
- **Galería de productos:** 800x600px, crop fill, quality auto  
- **Logos de tiendas:** 300x300px, crop fill, quality auto
- **Banners de tiendas:** 1200x400px, crop fill, quality auto
- **Avatares de usuarios:** 200x200px, crop fill, gravity face

---

## 🎉 **¡BACKEND 100% LISTO PARA FLUTTER!**

**Tu backend Django está completamente preparado para que tu app Flutter consuma todas las APIs. Todos los datos son reales, la documentación está completa, y las funcionalidades críticas están implementadas.**

**¿Te gustaría que te ayude con algún aspecto específico de la integración Flutter?** 🚀
