# Sistema de Órdenes - discorp

## Descripción General

El sistema de órdenes de discorp es un módulo completo que gestiona todo el flujo desde que un usuario agrega productos a su carrito hasta que recibe su pedido. Implementa un sistema de estados robusto, gestión automática de inventario y roles diferenciados para usuarios.

## Arquitectura del Sistema

### Modelos Principales

#### 1. Order (Orden)
```python
# Modelo principal que representa una orden completa
class Order(models.Model):
    # Campos únicos de identificación
    id = UUIDField()                    # ID único UUID
    order_number = CharField()          # Número legible (ORD-YYYYMMDD-XXXX)
    
    # Relaciones con usuarios
    customer = ForeignKey(User)         # Cliente que realiza la orden
    delivery_person = ForeignKey(User)  # Repartidor asignado
    
    # Estados y fechas
    status = CharField(choices=STATUS_CHOICES)  # Estado actual
    created_at = DateTimeField()               # Fecha de creación
    confirmed_at = DateTimeField()             # Fecha de confirmación
    delivered_at = DateTimeField()             # Fecha de entrega
    
    # Información de entrega
    delivery_address = TextField()      # Dirección completa
    delivery_phone = CharField()        # Teléfono de contacto
    delivery_notes = TextField()        # Instrucciones especiales
    
    # Información de pago
    payment_method = CharField()        # Método de pago elegido
    is_paid = BooleanField()           # Estado del pago
    
    # Totales calculados
    subtotal = DecimalField()          # Suma de productos
    delivery_fee = DecimalField()      # Costo de envío
    discount_amount = DecimalField()   # Descuentos aplicados
    total = DecimalField()             # Total final
```

#### 2. OrderItem (Item de Orden)
```python
# Representa cada producto dentro de una orden
class OrderItem(models.Model):
    order = ForeignKey(Order)          # Orden a la que pertenece
    product = ForeignKey(Product)      # Producto referenciado
    
    # Cantidad y precios
    quantity = PositiveIntegerField()  # Cantidad solicitada
    unit_price = DecimalField()        # Precio unitario al momento de la orden
    subtotal = DecimalField()          # Cantidad × Precio unitario
    
    # Snapshot del producto (datos históricos)
    product_name = CharField()         # Nombre del producto
    product_description = TextField()  # Descripción del producto
```

#### 3. Cart (Carrito)
```python
# Carrito de compras temporal del usuario
class Cart(models.Model):
    user = OneToOneField(User)         # Usuario propietario del carrito
    created_at = DateTimeField()       # Fecha de creación
    updated_at = DateTimeField()       # Última actualización
```

#### 4. CartItem (Item del Carrito)
```python
# Productos en el carrito antes de convertirse en orden
class CartItem(models.Model):
    cart = ForeignKey(Cart)            # Carrito al que pertenece
    product = ForeignKey(Product)      # Producto en el carrito
    quantity = PositiveIntegerField()  # Cantidad deseada
```

### Estados de Órdenes

El sistema implementa un flujo de estados controlado:

```
pending → confirmed → preparing → ready → in_delivery → delivered
   ↓           ↓
cancelled   cancelled
```

#### Descripción de Estados

1. **pending**: Orden creada, esperando confirmación del usuario
2. **confirmed**: Orden confirmada y pagada, lista para preparar
3. **preparing**: Restaurante está preparando la orden
4. **ready**: Orden lista para ser recogida por el repartidor
5. **in_delivery**: Repartidor ha recogido la orden y está en camino
6. **delivered**: Orden entregada exitosamente al cliente
7. **cancelled**: Orden cancelada (posible desde pending/confirmed)

#### Transiciones Permitidas

```python
VALID_TRANSITIONS = {
    'pending': ['confirmed', 'cancelled'],
    'confirmed': ['preparing', 'cancelled'],
    'preparing': ['ready'],
    'ready': ['in_delivery'],
    'in_delivery': ['delivered'],
    'delivered': [],  # Estado final
    'cancelled': []   # Estado final
}
```

## API Endpoints

### Órdenes (`/api/orders/`)

#### Listar Órdenes
```http
GET /api/orders/
Authorization: Bearer <token>

# Filtros disponibles
GET /api/orders/?status=confirmed
GET /api/orders/?payment_method=card
GET /api/orders/?is_paid=true
GET /api/orders/?ordering=-created_at
```

**Respuesta:**
```json
{
  "count": 25,
  "next": "http://api/orders/?page=2",
  "previous": null,
  "results": [
    {
      "id": "uuid-here",
      "order_number": "ORD-20241201-1234",
      "customer_name": "Juan Pérez",
      "status": "confirmed",
      "status_display": "Confirmada",
      "total": "45.99",
      "items_count": 3,
      "created_at": "2024-12-01T10:30:00Z"
    }
  ]
}
```

#### Crear Orden Directa
```http
POST /api/orders/
Content-Type: application/json
Authorization: Bearer <token>

{
  "delivery_address": "Calle Principal 123, Colonia Centro",
  "delivery_phone": "555-1234",
  "delivery_notes": "Timbre rojo, segundo piso",
  "payment_method": "card",
  "delivery_fee": "5.00",
  "discount_amount": "2.00",
  "items": [
    {
      "product": 1,
      "quantity": 2
    },
    {
      "product": 3,
      "quantity": 1
    }
  ]
}
```

#### Confirmar Orden
```http
POST /api/orders/{id}/confirm/
Authorization: Bearer <token>
```

#### Cancelar Orden
```http
POST /api/orders/{id}/cancel/
Authorization: Bearer <token>
```

#### Estadísticas (Solo Staff)
```http
GET /api/orders/stats/
Authorization: Bearer <staff-token>
```

**Respuesta:**
```json
{
  "total_orders": 150,
  "pending_orders": 5,
  "confirmed_orders": 12,
  "preparing_orders": 8,
  "ready_orders": 3,
  "in_delivery_orders": 7,
  "delivered_orders": 115,
  "cancelled_orders": 0,
  "total_revenue": "15750.50",
  "average_order_value": "45.30",
  "orders_today": 8,
  "revenue_today": "320.75"
}
```

### Carrito (`/api/cart/`)

#### Ver Carrito
```http
GET /api/cart/
Authorization: Bearer <token>
```

**Respuesta:**
```json
{
  "id": 1,
  "user": 1,
  "items_count": 4,
  "total": "67.50",
  "items": [
    {
      "id": 1,
      "product": {
        "id": 1,
        "name": "Hamburguesa Clásica",
        "price": "15.99",
        "image": "url-to-image"
      },
      "quantity": 2,
      "subtotal": "31.98"
    }
  ],
  "created_at": "2024-12-01T09:00:00Z",
  "updated_at": "2024-12-01T10:15:00Z"
}
```

#### Agregar Producto al Carrito
```http
POST /api/cart/add_item/
Content-Type: application/json
Authorization: Bearer <token>

{
  "product": 1,
  "quantity": 2
}
```

#### Limpiar Carrito
```http
DELETE /api/cart/clear/
Authorization: Bearer <token>
```

#### Checkout (Convertir Carrito a Orden)
```http
POST /api/cart/checkout/
Content-Type: application/json
Authorization: Bearer <token>

{
  "delivery_address": "Calle Principal 123",
  "delivery_phone": "555-1234",
  "delivery_notes": "Casa azul",
  "payment_method": "cash",
  "delivery_fee": "5.00",
  "discount_amount": "0.00"
}
```

## Lógica de Negocio

### Gestión de Stock

#### Al Crear Orden
1. Se verifica disponibilidad del producto (`product.is_available`)
2. Se valida stock suficiente (`product.stock >= quantity`)
3. Se reduce el stock automáticamente (`product.stock -= quantity`)
4. Se guarda un snapshot del producto en `OrderItem`

#### Al Cancelar Orden
1. Se verifica que la orden pueda cancelarse (`order.can_be_cancelled`)
2. Se restaura el stock de cada producto (`product.stock += quantity`)
3. Se cambia el estado a 'cancelled'

### Cálculo de Totales

Los totales se calculan automáticamente:

```python
# En OrderItem.save()
self.subtotal = self.quantity * self.unit_price

# En Order.calculate_totals()
self.subtotal = sum(item.subtotal for item in self.items.all())
self.total = self.subtotal + self.delivery_fee - self.discount_amount
```

### Generación de Números de Orden

```python
def generate_order_number(self):
    """
    Genera número único formato: ORD-YYYYMMDD-XXXX
    Ejemplo: ORD-20241201-1234
    """
    date_part = timezone.now().strftime('%Y%m%d')
    random_part = ''.join(random.choices(string.digits, k=4))
    return f"ORD-{date_part}-{random_part}"
```

## Permisos y Roles

### Cliente (Usuario Regular)
- ✅ Ver sus propias órdenes
- ✅ Crear órdenes
- ✅ Confirmar/cancelar órdenes propias
- ✅ Gestionar su carrito
- ❌ Ver órdenes de otros usuarios
- ❌ Cambiar estados de órdenes

### Delivery (Repartidor)
- ✅ Ver órdenes asignadas a él
- ✅ Ver órdenes listas para asignar (`status='ready'`)
- ✅ Cambiar estados: `ready → in_delivery → delivered`
- ❌ Ver todas las órdenes
- ❌ Cambiar otros estados

### Staff (Administrador)
- ✅ Ver todas las órdenes
- ✅ Cambiar cualquier estado
- ✅ Asignar repartidores
- ✅ Ver estadísticas
- ✅ Gestión completa

## Validaciones Implementadas

### En Serializers
```python
# Validación de stock
def validate(self, data):
    product = data['product']
    quantity = data['quantity']
    
    if product.manage_stock and product.stock < quantity:
        raise ValidationError(f'Stock insuficiente. Disponible: {product.stock}')
    
    return data

# Validación de transiciones de estado
def validate_status(self, value):
    current_status = self.instance.status
    
    if value not in VALID_TRANSITIONS.get(current_status, []):
        raise ValidationError(f'No se puede cambiar de {current_status} a {value}')
    
    return value
```

### En Modelos
```python
# Propiedades de validación
@property
def can_be_cancelled(self):
    return self.status in ['pending', 'confirmed']

@property
def can_be_confirmed(self):
    return self.status == 'pending' and self.items.exists()
```

## Casos de Uso Principales

### 1. Flujo de Carrito a Orden
```python
# 1. Usuario agrega productos al carrito
POST /api/cart/add_item/ {"product": 1, "quantity": 2}
POST /api/cart/add_item/ {"product": 3, "quantity": 1}

# 2. Usuario revisa su carrito
GET /api/cart/

# 3. Usuario hace checkout
POST /api/cart/checkout/ {
    "delivery_address": "...",
    "payment_method": "card"
}

# 4. Sistema crea orden en estado 'pending'
# 5. Usuario confirma orden
POST /api/orders/{id}/confirm/

# 6. Orden pasa a 'confirmed' y se procesa
```

### 2. Gestión de Estados por Staff
```python
# Staff ve órdenes confirmadas
GET /api/orders/?status=confirmed

# Staff cambia a preparando
PATCH /api/orders/{id}/update_status/ {"status": "preparing"}

# Staff marca como lista
PATCH /api/orders/{id}/update_status/ {"status": "ready"}

# Delivery toma la orden
PATCH /api/orders/{id}/update_status/ {"status": "in_delivery"}

# Delivery marca como entregada
PATCH /api/orders/{id}/update_status/ {"status": "delivered"}
```

### 3. Cancelación y Restauración de Stock
```python
# Usuario cancela orden
POST /api/orders/{id}/cancel/

# Sistema automáticamente:
# 1. Verifica que se pueda cancelar
# 2. Restaura stock de productos
# 3. Cambia estado a 'cancelled'
```

## Optimizaciones Implementadas

### Consultas de Base de Datos
```python
# En ViewSets - consultas optimizadas
queryset = Order.objects.select_related(
    'customer', 'delivery_person'
).prefetch_related('items__product')

# Evita N+1 queries al acceder a relaciones
```

### Índices de Base de Datos
```python
class Meta:
    indexes = [
        models.Index(fields=['status', 'created_at']),
        models.Index(fields=['customer', 'status']),
        models.Index(fields=['delivery_person', 'status']),
        models.Index(fields=['order_number']),
    ]
```

### Campos Calculados
```python
# Propiedades que se calculan dinámicamente
@property
def items_count(self):
    return self.items.aggregate(total=Sum('quantity'))['total'] or 0

@property
def total(self):
    return sum(item.subtotal for item in self.items.all())
```

## Testing

### Cobertura de Tests
- **11 tests** implementados
- **Modelos**: Validación de propiedades y métodos
- **API**: Endpoints y permisos
- **Integración**: Flujos completos
- **Validaciones**: Estados y transiciones

### Ejemplos de Tests
```python
def test_order_totals_calculation(self):
    """Prueba el cálculo automático de totales"""
    order = Order.objects.create(...)
    OrderItem.objects.create(order=order, quantity=2, unit_price=15.99)
    
    expected_subtotal = Decimal('31.98')
    self.assertEqual(order.subtotal, expected_subtotal)

def test_complete_order_flow(self):
    """Prueba el flujo completo carrito → orden → entrega"""
    # 1. Agregar al carrito
    # 2. Hacer checkout
    # 3. Confirmar orden
    # 4. Verificar estado final
```

## Consideraciones de Seguridad

### Autenticación
- Todos los endpoints requieren autenticación JWT
- Tokens incluidos en header `Authorization: Bearer <token>`

### Autorización
- Usuarios solo ven sus propias órdenes
- Staff puede ver todas las órdenes
- Delivery ve órdenes asignadas o disponibles

### Validación de Datos
- Validación de stock en tiempo real
- Verificación de transiciones de estado
- Sanitización de inputs en serializers

### Transacciones Atómicas
```python
@transaction.atomic
def create_order_from_cart(self, user):
    # Toda la operación se hace en una transacción
    # Si algo falla, se hace rollback automático
```

## Monitoreo y Métricas

### Estadísticas Disponibles
- Total de órdenes por estado
- Revenue total y promedio
- Órdenes del día
- Métricas de rendimiento

### Logs Automáticos
- Cambios de estado registrados
- Errores de stock capturados
- Transacciones fallidas loggeadas

## Extensibilidad

### Futuras Mejoras Sugeridas
1. **Notificaciones**: Push/SMS en cambios de estado
2. **Tracking**: GPS en tiempo real para delivery
3. **Ratings**: Sistema de calificación post-entrega
4. **Promociones**: Cupones y descuentos avanzados
5. **Analytics**: Dashboard de métricas avanzadas
6. **Pagos**: Integración con pasarelas de pago
7. **Scheduling**: Órdenes programadas

### Puntos de Extensión
- Custom validators en serializers
- Signals para eventos de orden
- Middleware para logging
- Custom permissions para roles específicos

Esta documentación cubre todos los aspectos técnicos y de negocio del sistema de órdenes implementado en discorp.
