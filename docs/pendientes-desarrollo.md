# PENDIENTES DE DESARROLLO - discorp DJANGO
## Análisis de funcionalidades faltantes vs Planificación Original

---

## 📊 **ESTADO ACTUAL IMPLEMENTADO**

### ✅ **YA IMPLEMENTADO (100%)**
- **Autenticación JWT**: Login, registro, refresh tokens, logout
- **Usuarios con roles múltiples**: Customer, Store, Delivery
- **Categorías jerárquicas**: Sistema completo con CRUD
- **Productos completos**: Con imágenes, reseñas, stock, descuentos
- **Sistema de órdenes**: Cart → Order → Estados → Entrega
- **Admin interface**: Para todas las entidades
- **API REST completa**: Swagger, filtros, búsqueda, paginación
- **CORS configurado**: Para frontend

---

## 🚧 **FUNCIONALIDADES PENDIENTES**

### 1. **TIENDAS/RESTAURANTES** (CRÍTICO - ALTA PRIORIDAD)
**Estado**: ❌ **NO IMPLEMENTADO**

**Necesario crear**:
- **App**: `apps/stores/`
- **Modelo Store**:
  ```python
  class Store(models.Model):
      owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stores")
      name = models.CharField(max_length=200)
      description = models.TextField(blank=True)
      address = models.TextField()
      latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
      longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
      phone = models.CharField(max_length=20, blank=True)
      email = models.EmailField(blank=True)
      logo = models.ImageField(upload_to='stores/logos/', blank=True, null=True)
      is_active = models.BooleanField(default=True)
      opening_hours = models.JSONField(default=dict, blank=True)
      delivery_radius = models.IntegerField(default=5000)  # metros
      minimum_order = models.DecimalField(max_digits=10, decimal_places=2, default=0)
      delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)
  ```

**API Endpoints necesarios**:
- `GET /api/stores/` - Listar tiendas activas
- `GET /api/stores/{id}/` - Detalle de tienda
- `GET /api/stores/{id}/products/` - Productos de la tienda
- `GET /api/stores/nearby/?lat=X&lng=Y` - Tiendas cercanas
- `POST /api/stores/` - Crear tienda (solo usuarios con rol store)
- `PUT/PATCH /api/stores/{id}/` - Actualizar tienda (solo owner)

**Relaciones a modificar**:
- **Product**: Agregar `store = models.ForeignKey(Store)`
- **Category**: Agregar `store = models.ForeignKey(Store)` (categorías por tienda)
- **Order**: Ya tiene relación con User, pero necesita Store

### 2. **GEOLOCALIZACIÓN Y DELIVERY ZONES** (ALTA PRIORIDAD)
**Estado**: ❌ **NO IMPLEMENTADO**

**Necesario crear**:
- **Modelo DeliveryZone**:
  ```python
  class DeliveryZone(models.Model):
      store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="delivery_zones")
      name = models.CharField(max_length=100)
      delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
      minimum_order = models.DecimalField(max_digits=10, decimal_places=2, default=0)
      estimated_time = models.IntegerField(default=30)  # minutos
      polygon_coordinates = models.JSONField(default=list)  # Coordenadas del polígono
  ```

- **Modelo DeliveryLocation** (ubicación en tiempo real de deliveries):
  ```python
  class DeliveryLocation(models.Model):
      delivery_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="delivery_location")
      latitude = models.DecimalField(max_digits=10, decimal_places=8)
      longitude = models.DecimalField(max_digits=11, decimal_places=8)
      is_online = models.BooleanField(default=False)
      current_order = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True, blank=True)
      last_update = models.DateTimeField(auto_now=True)
  ```

**API Endpoints necesarios**:
- `GET /api/stores/nearby/?lat=X&lng=Y&radius=5000` - Tiendas cercanas
- `POST /api/delivery/location/` - Actualizar ubicación del delivery
- `GET /api/delivery/available-orders/` - Órdenes disponibles para delivery
- `POST /api/orders/{id}/assign-delivery/` - Asignar delivery a orden

**Funciones necesarias**:
- Cálculo de distancia (fórmula haversine)
- Búsqueda de deliveries cercanos
- Asignación automática de deliveries

### 3. **NOTIFICACIONES PUSH** (MEDIA PRIORIDAD)
**Estado**: ❌ **NO IMPLEMENTADO**

**Necesario crear**:
- **App**: `apps/notifications/`
- **Modelo Notification**:
  ```python
  class Notification(models.Model):
      user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
      title = models.CharField(max_length=200)
      message = models.TextField()
      type = models.CharField(max_length=50, choices=[
          ('order', 'Order'),
          ('delivery', 'Delivery'),
          ('system', 'System'),
      ])
      data = models.JSONField(default=dict, blank=True)
      is_read = models.BooleanField(default=False)
      created_at = models.DateTimeField(auto_now_add=True)
  ```

**Integración necesaria**:
- **OneSignal** o **Firebase Push Notifications**
- Signals de Django para notificaciones automáticas
- WebSockets para notificaciones en tiempo real (Django Channels)

**API Endpoints necesarios**:
- `GET /api/notifications/` - Listar notificaciones del usuario
- `PATCH /api/notifications/{id}/read/` - Marcar como leída
- `POST /api/notifications/mark-all-read/` - Marcar todas como leídas

### 4. **SISTEMA DE PAGOS** (MEDIA PRIORIDAD)
**Estado**: ⚠️ **PARCIALMENTE IMPLEMENTADO**

**Actualmente en Order**:
- `payment_method` (texto libre)
- `payment_status` (pending, paid, failed)

**Necesario mejorar**:
- **Modelo Payment**:
  ```python
  class Payment(models.Model):
      order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
      payment_method = models.CharField(max_length=50, choices=[
          ('cash', 'Efectivo'),
          ('card', 'Tarjeta'),
          ('digital_wallet', 'Billetera Digital'),
      ])
      payment_gateway = models.CharField(max_length=50, blank=True)  # PayU, Stripe, etc.
      transaction_id = models.CharField(max_length=200, blank=True)
      amount = models.DecimalField(max_digits=10, decimal_places=2)
      status = models.CharField(max_length=50, choices=[
          ('pending', 'Pendiente'),
          ('processing', 'Procesando'),
          ('completed', 'Completado'),
          ('failed', 'Fallido'),
          ('refunded', 'Reembolsado'),
      ])
      gateway_response = models.JSONField(default=dict, blank=True)
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)
  ```

**Integraciones necesarias**:
- **PayU** (Colombia)
- **Stripe** (Internacional)
- **Mercado Pago** (Latinoamérica)

### 5. **REPORTES Y ANALYTICS** (BAJA PRIORIDAD)
**Estado**: ⚠️ **BÁSICO IMPLEMENTADO**

**Ya existe**:
- `GET /api/orders/stats/` (básico)
- `GET /api/products/stats/` (básico)

**Necesario expandir**:
- **Dashboard para tiendas**: Ventas, productos más vendidos, horarios pico
- **Dashboard para deliveries**: Entregas, ganancias, rutas
- **Dashboard para admin**: Métricas generales, usuarios activos, transacciones

**Modelos adicionales**:
```python
class SalesReport(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    date = models.DateField()
    total_orders = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
```

### 6. **SISTEMA DE RESEÑAS DE TIENDAS** (BAJA PRIORIDAD)
**Estado**: ❌ **NO IMPLEMENTADO**

**Ya existe**: Reseñas de productos
**Falta**: Reseñas de tiendas y deliveries

**Modelo necesario**:
```python
class StoreReview(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  # Solo si compró
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['store', 'user', 'order']
```

---

## 📅 **PRIORIZACIÓN SUGERIDA**

### **SPRINT 1 - CRÍTICO (2-3 semanas)**
1. ✅ **App Stores completa**
   - Modelo, API, Admin
   - Relaciones con productos y categorías
   - Búsqueda por geolocalización

2. ✅ **Modificar modelos existentes**
   - Product → agregar store_id
   - Category → agregar store_id (opcional: categorías globales vs por tienda)

### **SPRINT 2 - ALTA PRIORIDAD (2 semanas)**
1. ✅ **Sistema de geolocalización**
   - DeliveryZone, DeliveryLocation
   - APIs de búsqueda geográfica
   - Asignación de deliveries

2. ✅ **Notificaciones básicas**
   - Modelo Notification
   - Signals automáticos
   - API básica

### **SPRINT 3 - MEDIA PRIORIDAD (2 semanas)**
1. ✅ **Sistema de pagos**
   - Modelo Payment mejorado
   - Integración con PayU/Stripe
   - Webhooks de pagos

2. ✅ **Notificaciones push**
   - OneSignal/Firebase
   - WebSockets (opcional)

### **SPRINT 4 - BAJA PRIORIDAD (1-2 semanas)**
1. ✅ **Reportes avanzados**
2. ✅ **Reseñas de tiendas**
3. ✅ **Optimizaciones y pulimiento**

---

## 🎯 **PRÓXIMOS PASOS INMEDIATOS**

### **1. Crear app stores**
```bash
uv run ./manage.py startapp apps/stores
```

### **2. Implementar modelo Store**
- Crear modelo con todos los campos necesarios
- Migración
- Admin interface
- Serializers y ViewSets

### **3. Modificar modelos existentes**
- Agregar `store` a Product
- Decidir si Category es global o por tienda
- Crear migraciones

### **4. Actualizar Order workflow**
- Incluir información de tienda
- Cálculo de delivery fee por zona
- Asignación de delivery

---

## 📋 **CHECKLIST DE DESARROLLO**

### **App Stores**
- [ ] Crear app `apps/stores/`
- [ ] Modelo Store completo
- [ ] Migración inicial
- [ ] Admin interface
- [ ] Serializers (List, Detail, Create, Update)
- [ ] ViewSet con CRUD completo
- [ ] URLs y endpoints
- [ ] Tests unitarios
- [ ] Documentación Swagger

### **Geolocalización**
- [ ] Modelo DeliveryZone
- [ ] Modelo DeliveryLocation  
- [ ] Funciones de cálculo de distancia
- [ ] API de búsqueda geográfica
- [ ] Tests de geolocalización

### **Notificaciones**
- [ ] App `apps/notifications/`
- [ ] Modelo Notification
- [ ] Signals automáticos
- [ ] API básica
- [ ] Integración OneSignal/Firebase

### **Pagos**
- [ ] Modelo Payment mejorado
- [ ] Integración PayU
- [ ] Webhooks de pagos
- [ ] Tests de pagos

---

**📊 RESUMEN**: De las funcionalidades principales planificadas, tienes aproximadamente **70% implementado**. Las funcionalidades críticas faltantes son **Stores** y **Geolocalización**, que son fundamentales para el funcionamiento del sistema de delivery.

