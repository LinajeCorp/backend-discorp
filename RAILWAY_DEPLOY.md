# Despliegue en Railway - Discorp Backend

## 🚀 Configuración Automática

Este proyecto está configurado para desplegarse automáticamente en Railway usando:

- `railway.json` - Configuración principal
- `nixpacks.toml` - Build configuration
- `Procfile` - Comandos de proceso
- `deploy.sh` - Script de despliegue

## 📋 Variables de Entorno Requeridas

### Variables Básicas
```bash
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=*
DJANGO_SETTINGS_MODULE=core.settings
```

### Base de Datos (PostgreSQL)
```bash
DATABASE_URL=postgresql://user:pass@host:port/dbname
# O usando variables individuales:
POSTGRES_DB=discorp_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### Redis (para WebSockets)
```bash
REDIS_URL=redis://localhost:6379
```

### Cloudinary (para archivos media)
```bash
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

### Stripe (pagos)
```bash
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

### PayPal (pagos)
```bash
PAYPAL_CLIENT_ID=your-client-id
PAYPAL_CLIENT_SECRET=your-client-secret
PAYPAL_SANDBOX=True
```

### Frontend
```bash
FRONTEND_URL=https://your-frontend-domain.com
```

## 🔧 Pasos para Desplegar

### 1. Crear Proyecto en Railway
```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Crear proyecto
railway new
```

### 2. Conectar Repositorio
- Ve a Railway Dashboard
- Conecta tu repositorio de GitHub
- Railway detectará automáticamente la configuración

### 3. Agregar Servicios
```bash
# PostgreSQL
railway add postgresql

# Redis (opcional, para WebSockets)
railway add redis
```

### 4. Configurar Variables de Entorno
```bash
# Opción 1: Desde CLI
railway variables set SECRET_KEY="your-secret-key"
railway variables set DEBUG="False"
railway variables set ALLOWED_HOSTS="*"

# Opción 2: Desde Dashboard
# Ve a tu proyecto > Variables > Add Variable
```

### 5. Deploy
```bash
# Deploy automático desde GitHub
git push origin main

# O deploy manual
railway up
```

## 🌐 URLs Importantes

Después del despliegue, tendrás acceso a:

- **API Base**: `https://your-app.railway.app/api/v1/`
- **Admin**: `https://your-app.railway.app/admin/`
- **Swagger UI**: `https://your-app.railway.app/docs/`
- **ReDoc**: `https://your-app.railway.app/redoc/`

### Endpoints Principales
- `GET /api/v1/products/` - Lista de productos desde Strapi
- `GET /api/v1/users/` - Gestión de usuarios
- `POST /api/v1/auth/login/` - Login JWT

## 🔒 Superusuario

El script de despliegue crea automáticamente un superusuario:
- **Usuario**: `admin`
- **Email**: `admin@discorp.com`
- **Contraseña**: `admin123`

⚠️ **Importante**: Cambia estas credenciales después del primer login.

## 🐛 Troubleshooting

### Error: "No module named 'uv'"
- Railway debería instalar `uv` automáticamente
- Verifica que `nixpacks.toml` esté presente

### Error: "Database connection failed"
- Verifica que PostgreSQL esté agregado al proyecto
- Confirma las variables de entorno de la BD

### Error: "Static files not found"
- El comando `collectstatic` se ejecuta automáticamente
- Verifica que `STATIC_ROOT` esté configurado

### Error: "CORS issues"
- Actualiza `CORS_ALLOWED_ORIGINS` en settings.py
- Configura `FRONTEND_URL` correctamente

## 📊 Monitoreo

Railway proporciona:
- **Logs**: Ver logs en tiempo real
- **Métricas**: CPU, memoria, requests
- **Health checks**: Endpoint `/admin/` para verificar salud

## 🔄 CI/CD

El despliegue es automático:
1. Push a `main` branch
2. Railway detecta cambios
3. Ejecuta build automáticamente
4. Deploy sin downtime

## 📝 Comandos Útiles

```bash
# Ver logs
railway logs

# Ejecutar comandos en producción
railway run python manage.py migrate
railway run python manage.py createsuperuser

# Abrir shell
railway shell

# Ver variables
railway variables

# Conectar a BD
railway connect postgresql
```

## 🚨 Notas de Producción

1. **SECRET_KEY**: Usar una key segura y única
2. **DEBUG**: Siempre `False` en producción
3. **ALLOWED_HOSTS**: Configurar dominios específicos
4. **SSL**: Railway proporciona HTTPS automáticamente
5. **Backups**: Railway hace backups automáticos de PostgreSQL

¡Tu aplicación Django está lista para producción en Railway! 🎉
