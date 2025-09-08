# PLANIFICACIÓN PROYECTO INSTAORDER
## Flutter + Supabase - Sistema de Pedidos en Tiempo Real

### 📋 RESUMEN DEL PROYECTO
- **Presupuesto**: 10.000.000 COP (2.350 USD)
- **Duración**: 13 semanas
- **Tecnologías**: Flutter + Supabase + OneSignal
- **Aplicaciones**: 3 apps (Tiendas, Clientes, Domiciliarios)

---

## 🗓️ CRONOGRAMA DETALLADO

### SEMANA 1-2: DISEÑO Y PLANIFICACIÓN (1.5 semanas)
- [ ] **Diseño UI/UX simplificado** (200 USD)
- [ ] **Configuración de Supabase**
- [ ] **Diseño de base de datos**
- [ ] **Arquitectura de la aplicación**

### SEMANA 3-12: DESARROLLO (10 semanas)

#### **SEMANA 3-5: App Clientes** (900 USD - 3.600.000 COP)
- [ ] Configuración del proyecto Flutter
- [ ] Autenticación con Supabase
- [ ] Pantalla de registro/login
- [ ] Lista de restaurantes
- [ ] Menú de productos
- [ ] Carrito de compras
- [ ] Proceso de checkout
- [ ] Historial de pedidos
- [ ] Seguimiento en tiempo real

#### **SEMANA 6-8: App Tiendas** (700 USD - 2.800.000 COP)
- [ ] Configuración del proyecto Flutter
- [ ] Autenticación de tiendas
- [ ] Dashboard de pedidos
- [ ] Gestión de menú
- [ ] Notificaciones de nuevos pedidos
- [ ] Estado de pedidos
- [ ] Reportes básicos

#### **SEMANA 9-10: App Domiciliarios** (400 USD - 1.600.000 COP)
- [ ] Configuración del proyecto Flutter
- [ ] Autenticación de domiciliarios
- [ ] Lista de pedidos disponibles
- [ ] Aceptar/rechazar pedidos
- [ ] Seguimiento GPS
- [ ] Notificaciones push
- [ ] Historial de entregas

#### **SEMANA 11-12: Backend y Integración** (150 USD - 600.000 COP)
- [ ] Configuración de OneSignal
- [ ] Webhooks de Supabase
- [ ] Integración de notificaciones
- [ ] Testing de integración
- [ ] Optimización de performance

### SEMANA 13: PRUEBAS Y DEPLOY (1.5 semanas)
- [ ] Testing completo
- [ ] Corrección de bugs
- [ ] Deploy a producción
- [ ] Documentación final

---

## 🗄️ ESTRUCTURA DE BASE DE DATOS SUPABASE

### TABLAS PRINCIPALES

#### 1. **users** (Autenticación)
```sql
-- Tabla de usuarios (manejada por Supabase Auth)
-- Se extiende con perfiles personalizados
CREATE TABLE public.profiles (
  id UUID REFERENCES auth.users(id) PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  full_name TEXT,
  phone TEXT,
  user_type TEXT CHECK (user_type IN ('customer', 'store', 'delivery')),
  avatar_url TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### 2. **stores** (Restaurantes/Tiendas)
```sql
CREATE TABLE public.stores (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  owner_id UUID REFERENCES public.profiles(id) NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  address TEXT NOT NULL,
  latitude DECIMAL(10, 8),
  longitude DECIMAL(11, 8),
  phone TEXT,
  email TEXT,
  logo_url TEXT,
  is_active BOOLEAN DEFAULT true,
  opening_hours JSONB,
  delivery_radius INTEGER DEFAULT 5000, -- metros
  minimum_order DECIMAL(10, 2) DEFAULT 0,
  delivery_fee DECIMAL(10, 2) DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### 3. **categories** (Categorías de productos)
```sql
CREATE TABLE public.categories (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  store_id UUID REFERENCES public.stores(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  description TEXT,
  image_url TEXT,
  sort_order INTEGER DEFAULT 0,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### 4. **products** (Productos)
```sql
CREATE TABLE public.products (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  store_id UUID REFERENCES public.stores(id) ON DELETE CASCADE,
  category_id UUID REFERENCES public.categories(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  description TEXT,
  price DECIMAL(10, 2) NOT NULL,
  image_url TEXT,
  is_available BOOLEAN DEFAULT true,
  preparation_time INTEGER DEFAULT 15, -- minutos
  sort_order INTEGER DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### 5. **orders** (Pedidos)
```sql
CREATE TABLE public.orders (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  customer_id UUID REFERENCES public.profiles(id) NOT NULL,
  store_id UUID REFERENCES public.stores(id) NOT NULL,
  delivery_id UUID REFERENCES public.profiles(id),
  order_number TEXT UNIQUE NOT NULL,
  status TEXT CHECK (status IN ('pending', 'confirmed', 'preparing', 'ready', 'picked_up', 'delivered', 'cancelled')) DEFAULT 'pending',
  total_amount DECIMAL(10, 2) NOT NULL,
  delivery_fee DECIMAL(10, 2) DEFAULT 0,
  tax_amount DECIMAL(10, 2) DEFAULT 0,
  subtotal DECIMAL(10, 2) NOT NULL,
  delivery_address TEXT NOT NULL,
  delivery_latitude DECIMAL(10, 8),
  delivery_longitude DECIMAL(11, 8),
  customer_notes TEXT,
  estimated_delivery_time TIMESTAMP WITH TIME ZONE,
  actual_delivery_time TIMESTAMP WITH TIME ZONE,
  payment_method TEXT DEFAULT 'cash',
  payment_status TEXT CHECK (payment_status IN ('pending', 'paid', 'failed')) DEFAULT 'pending',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### 6. **order_items** (Items del pedido)
```sql
CREATE TABLE public.order_items (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  order_id UUID REFERENCES public.orders(id) ON DELETE CASCADE,
  product_id UUID REFERENCES public.products(id),
  product_name TEXT NOT NULL, -- Snapshot del nombre del producto
  product_price DECIMAL(10, 2) NOT NULL, -- Snapshot del precio
  quantity INTEGER NOT NULL DEFAULT 1,
  subtotal DECIMAL(10, 2) NOT NULL,
  notes TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### 7. **delivery_zones** (Zonas de entrega)
```sql
CREATE TABLE public.delivery_zones (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  store_id UUID REFERENCES public.stores(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  delivery_fee DECIMAL(10, 2) DEFAULT 0,
  minimum_order DECIMAL(10, 2) DEFAULT 0,
  estimated_time INTEGER DEFAULT 30, -- minutos
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### 8. **notifications** (Notificaciones)
```sql
CREATE TABLE public.notifications (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES public.profiles(id) NOT NULL,
  title TEXT NOT NULL,
  message TEXT NOT NULL,
  type TEXT CHECK (type IN ('order', 'delivery', 'system')) NOT NULL,
  data JSONB, -- Datos adicionales (order_id, etc.)
  is_read BOOLEAN DEFAULT false,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### 9. **delivery_locations** (Ubicaciones de domiciliarios)
```sql
CREATE TABLE public.delivery_locations (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  delivery_id UUID REFERENCES public.profiles(id) NOT NULL,
  latitude DECIMAL(10, 8) NOT NULL,
  longitude DECIMAL(11, 8) NOT NULL,
  is_online BOOLEAN DEFAULT false,
  current_order_id UUID REFERENCES public.orders(id),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## 🔧 TRIGGERS Y FUNCIONES

### 1. **Trigger para actualizar updated_at**
```sql
-- Función para actualizar updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Aplicar a todas las tablas que necesiten updated_at
CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON public.profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_stores_updated_at BEFORE UPDATE ON public.stores FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_products_updated_at BEFORE UPDATE ON public.products FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_orders_updated_at BEFORE UPDATE ON public.orders FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_delivery_locations_updated_at BEFORE UPDATE ON public.delivery_locations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

### 2. **Trigger para generar order_number**
```sql
-- Función para generar número de pedido
CREATE OR REPLACE FUNCTION generate_order_number()
RETURNS TRIGGER AS $$
BEGIN
    NEW.order_number := 'ORD-' || EXTRACT(YEAR FROM NOW()) || 
                       LPAD(EXTRACT(MONTH FROM NOW())::TEXT, 2, '0') ||
                       LPAD(EXTRACT(DAY FROM NOW())::TEXT, 2, '0') || '-' ||
                       LPAD(NEW.id::TEXT, 8, '0');
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER generate_order_number_trigger BEFORE INSERT ON public.orders FOR EACH ROW EXECUTE FUNCTION generate_order_number();
```

### 3. **Trigger para notificaciones de pedidos**
```sql
-- Función para enviar notificaciones cuando cambia el estado del pedido
CREATE OR REPLACE FUNCTION notify_order_status_change()
RETURNS TRIGGER AS $$
BEGIN
    -- Notificar al cliente
    INSERT INTO public.notifications (user_id, title, message, type, data)
    VALUES (
        NEW.customer_id,
        'Estado de pedido actualizado',
        'Tu pedido #' || NEW.order_number || ' está ' || NEW.status,
        'order',
        jsonb_build_object('order_id', NEW.id, 'status', NEW.status)
    );
    
    -- Notificar a la tienda si es un nuevo pedido
    IF NEW.status = 'pending' AND (OLD.status IS NULL OR OLD.status != 'pending') THEN
        INSERT INTO public.notifications (user_id, title, message, type, data)
        SELECT 
            s.owner_id,
            'Nuevo pedido recibido',
            'Pedido #' || NEW.order_number || ' por $' || NEW.total_amount,
            'order',
            jsonb_build_object('order_id', NEW.id, 'amount', NEW.total_amount)
        FROM public.stores s WHERE s.id = NEW.store_id;
    END IF;
    
    -- Notificar al domiciliario si se asigna
    IF NEW.delivery_id IS NOT NULL AND (OLD.delivery_id IS NULL OR OLD.delivery_id != NEW.delivery_id) THEN
        INSERT INTO public.notifications (user_id, title, message, type, data)
        VALUES (
            NEW.delivery_id,
            'Pedido asignado',
            'Pedido #' || NEW.order_number || ' asignado para entrega',
            'delivery',
            jsonb_build_object('order_id', NEW.id, 'address', NEW.delivery_address)
        );
    END IF;
    
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER notify_order_status_change_trigger AFTER UPDATE ON public.orders FOR EACH ROW EXECUTE FUNCTION notify_order_status_change();
```

### 4. **Función para buscar domiciliarios cercanos**
```sql
-- Función para encontrar domiciliarios disponibles cerca de una ubicación
CREATE OR REPLACE FUNCTION find_nearby_delivery(
    target_lat DECIMAL(10, 8),
    target_lng DECIMAL(11, 8),
    radius_meters INTEGER DEFAULT 5000
)
RETURNS TABLE (
    delivery_id UUID,
    distance_meters DECIMAL(10, 2),
    is_online BOOLEAN
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        dl.delivery_id,
        (6371000 * acos(cos(radians(target_lat)) * cos(radians(dl.latitude)) * 
         cos(radians(dl.longitude) - radians(target_lng)) + 
         sin(radians(target_lat)) * sin(radians(dl.latitude))))::DECIMAL(10, 2) as distance_meters,
        dl.is_online
    FROM public.delivery_locations dl
    WHERE dl.is_online = true 
    AND dl.current_order_id IS NULL
    AND (6371000 * acos(cos(radians(target_lat)) * cos(radians(dl.latitude)) * 
         cos(radians(dl.longitude) - radians(target_lng)) + 
         sin(radians(target_lat)) * sin(radians(dl.latitude)))) <= radius_meters
    ORDER BY distance_meters ASC;
END;
$$ language 'plpgsql';
```

---

## 🔐 POLÍTICAS DE SEGURIDAD (RLS)

### 1. **Políticas para profiles**
```sql
-- Habilitar RLS
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- Usuarios pueden ver solo su propio perfil
CREATE POLICY "Users can view own profile" ON public.profiles
    FOR SELECT USING (auth.uid() = id);

-- Usuarios pueden actualizar solo su propio perfil
CREATE POLICY "Users can update own profile" ON public.profiles
    FOR UPDATE USING (auth.uid() = id);

-- Usuarios pueden insertar su propio perfil
CREATE POLICY "Users can insert own profile" ON public.profiles
    FOR INSERT WITH CHECK (auth.uid() = id);
```

### 2. **Políticas para stores**
```sql
ALTER TABLE public.stores ENABLE ROW LEVEL SECURITY;

-- Cualquiera puede ver tiendas activas
CREATE POLICY "Anyone can view active stores" ON public.stores
    FOR SELECT USING (is_active = true);

-- Solo el dueño puede modificar su tienda
CREATE POLICY "Store owners can manage their store" ON public.stores
    FOR ALL USING (owner_id = auth.uid());
```

### 3. **Políticas para orders**
```sql
ALTER TABLE public.orders ENABLE ROW LEVEL SECURITY;

-- Clientes pueden ver sus propios pedidos
CREATE POLICY "Customers can view own orders" ON public.orders
    FOR SELECT USING (customer_id = auth.uid());

-- Tiendas pueden ver pedidos de su tienda
CREATE POLICY "Stores can view their orders" ON public.orders
    FOR SELECT USING (
        store_id IN (
            SELECT id FROM public.stores WHERE owner_id = auth.uid()
        )
    );

-- Domiciliarios pueden ver pedidos asignados
CREATE POLICY "Delivery can view assigned orders" ON public.orders
    FOR SELECT USING (delivery_id = auth.uid());

-- Clientes pueden crear pedidos
CREATE POLICY "Customers can create orders" ON public.orders
    FOR INSERT WITH CHECK (customer_id = auth.uid());

-- Tiendas pueden actualizar pedidos de su tienda
CREATE POLICY "Stores can update their orders" ON public.orders
    FOR UPDATE USING (
        store_id IN (
            SELECT id FROM public.stores WHERE owner_id = auth.uid()
        )
    );
```

---

## 📱 ESTRUCTURA DE CARPETAS FLUTTER

```
lib/
├── core/
│   ├── constants/
│   ├── errors/
│   ├── network/
│   └── utils/
├── features/
│   ├── auth/
│   │   ├── domain/
│   │   ├── infrastructure/
│   │   └── presentation/
│   ├── stores/
│   │   ├── domain/
│   │   ├── infrastructure/
│   │   └── presentation/
│   ├── orders/
│   │   ├── domain/
│   │   ├── infrastructure/
│   │   └── presentation/
│   └── delivery/
│       ├── domain/
│       ├── infrastructure/
│       └── presentation/
├── shared/
│   ├── widgets/
│   ├── providers/
│   └── models/
└── main.dart
```

---

## 🔧 DEPENDENCIAS NECESARIAS

### **pubspec.yaml**
```yaml
dependencies:
  flutter:
    sdk: flutter
  
  # Supabase
  supabase_flutter: ^2.3.4
  
  # Estado
  flutter_riverpod: ^2.4.9
  riverpod_annotation: ^2.3.3
  
  # Navegación
  go_router: ^13.2.0
  
  # UI
  cupertino_icons: ^1.0.8
  google_fonts: ^6.1.0
  
  # Utilidades
  intl: ^0.19.0
  image_picker: ^1.0.7
  cached_network_image: ^3.3.1
  
  # Geolocalización
  geolocator: ^11.0.0
  geocoding: ^3.0.0
  
  # Notificaciones
  onesignal_flutter: ^5.0.4
  
  # Otros
  uuid: ^4.3.3
  json_annotation: ^4.8.1

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^5.0.0
  build_runner: ^2.4.8
  json_serializable: ^6.7.1
  riverpod_generator: ^2.3.9
```

---

## 📋 CHECKLIST DE ACTIVIDADES

### **SEMANA ACTUAL: [ESPECIFICAR SEMANA]**
- [ ] **Actividad 1**: [DESCRIPCIÓN]
- [ ] **Actividad 2**: [DESCRIPCIÓN]
- [ ] **Actividad 3**: [DESCRIPCIÓN]

### **PRÓXIMA SEMANA**
- [ ] **Actividad 1**: [DESCRIPCIÓN]
- [ ] **Actividad 2**: [DESCRIPCIÓN]
- [ ] **Actividad 3**: [DESCRIPCIÓN]

---

## 🎯 OBJETIVOS SEMANALES

### **Semana 1-2**: Diseño y Configuración
- [ ] Diseño UI/UX completado
- [ ] Supabase configurado
- [ ] Base de datos creada
- [ ] Estructura del proyecto definida

### **Semana 3-5**: App Clientes
- [ ] Autenticación funcionando
- [ ] Lista de restaurantes
- [ ] Carrito de compras
- [ ] Proceso de checkout

### **Semana 6-8**: App Tiendas
- [ ] Dashboard de pedidos
- [ ] Gestión de menú
- [ ] Notificaciones push

### **Semana 9-10**: App Domiciliarios
- [ ] Sistema de asignación
- [ ] Seguimiento GPS
- [ ] Notificaciones

### **Semana 11-12**: Integración
- [ ] OneSignal configurado
- [ ] Webhooks funcionando
- [ ] Testing completo

### **Semana 13**: Finalización
- [ ] Deploy a producción
- [ ] Documentación
- [ ] Entrega final

---

## 📞 CONTACTO Y SOPORTE
- **Desarrollador**: [TU NOMBRE]
- **Email**: [TU EMAIL]
- **WhatsApp**: [TU NÚMERO]

---

*Última actualización: [FECHA]*
*Versión del documento: 1.0* 