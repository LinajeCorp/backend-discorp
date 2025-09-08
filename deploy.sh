#!/bin/bash

# Script de despliegue para Railway
# Este script se ejecuta durante el despliegue

echo "🚀 Iniciando despliegue en Railway..."

# Instalar dependencias con uv
echo "📦 Instalando dependencias..."
uv sync

# Ejecutar migraciones
echo "🗄️ Ejecutando migraciones de base de datos..."
uv run python manage.py migrate --noinput

# Recopilar archivos estáticos
echo "📁 Recopilando archivos estáticos..."
uv run python manage.py collectstatic --noinput

# Crear superusuario si no existe (opcional)
echo "👤 Verificando superusuario..."
uv run python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print('Creando superusuario admin...')
    User.objects.create_superuser('admin', 'admin@discorp.com', 'admin123')
    print('Superusuario creado: admin/admin123')
else:
    print('Superusuario ya existe')
"

echo "✅ Despliegue completado exitosamente!"
