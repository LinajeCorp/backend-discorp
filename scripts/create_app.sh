#!/bin/bash

# Script para crear apps Django en la carpeta apps/
# Uso: ./scripts/create_app.sh <nombre_app>
# Ejemplo: ./scripts/create_app.sh categories

set -e  # Salir si hay algún error

# Verificar que se proporcione el nombre de la app
if [ $# -eq 0 ]; then
    echo "❌ Error: Debes proporcionar el nombre de la app"
    echo "Uso: $0 <nombre_app>"
    echo "Ejemplo: $0 categories"
    exit 1
fi

APP_NAME=$1

# Verificar que el nombre de la app sea válido (solo letras, números y guiones bajos)
if [[ ! $APP_NAME =~ ^[a-zA-Z][a-zA-Z0-9_]*$ ]]; then
    echo "❌ Error: El nombre de la app debe empezar con una letra y solo contener letras, números y guiones bajos"
    echo "Ejemplo válido: categories, user_profile, orders"
    exit 1
fi

echo "🚀 Creando app Django: $APP_NAME"

# Verificar que estamos en el directorio raíz del proyecto Django
if [ ! -f "manage.py" ]; then
    echo "❌ Error: No se encontró manage.py. Ejecuta este script desde la raíz del proyecto Django"
    exit 1
fi

# Crear carpeta apps/ si no existe
if [ ! -d "apps" ]; then
    echo "📁 Creando carpeta apps/"
    mkdir -p apps
    touch apps/__init__.py
fi

# Verificar si la app ya existe
if [ -d "apps/$APP_NAME" ]; then
    echo "❌ Error: La app 'apps/$APP_NAME' ya existe"
    exit 1
fi

# Crear la app temporalmente en la raíz
echo "📦 Creando app temporal: $APP_NAME"
uv run ./manage.py startapp $APP_NAME

# Mover la app a la carpeta apps/
echo "📁 Moviendo app a apps/$APP_NAME"
mv $APP_NAME apps/

# Actualizar el archivo apps.py
echo "⚙️  Configurando apps.py"
APPS_PY_FILE="apps/$APP_NAME/apps.py"

# Crear backup del archivo original
cp "$APPS_PY_FILE" "$APPS_PY_FILE.backup"

# Actualizar el nombre de la app en apps.py
sed -i '' "s/name = '$APP_NAME'/name = 'apps.$APP_NAME'/" "$APPS_PY_FILE"

# Agregar la app a INSTALLED_APPS en settings.py
echo "⚙️  Agregando app a INSTALLED_APPS"
SETTINGS_FILE="core/settings.py"

# Crear backup del settings.py
cp "$SETTINGS_FILE" "$SETTINGS_FILE.backup"

# Buscar la línea que contiene 'django.contrib.staticfiles' y agregar la nueva app después
if grep -q "apps.$APP_NAME" "$SETTINGS_FILE"; then
    echo "⚠️  La app 'apps.$APP_NAME' ya está en INSTALLED_APPS"
else
    # Agregar la app después de django.contrib.staticfiles
    sed -i '' "/'django.contrib.staticfiles',/a\\
    'apps.$APP_NAME'," "$SETTINGS_FILE"
fi

# Verificar que todo esté correcto
echo "🔍 Verificando configuración..."
if uv run ./manage.py check > /dev/null 2>&1; then
    echo "✅ App '$APP_NAME' creada exitosamente en apps/$APP_NAME"
    echo ""
    echo "📋 Estructura creada:"
    echo "   apps/$APP_NAME/"
    echo "   ├── __init__.py"
    echo "   ├── admin.py"
    echo "   ├── apps.py"
    echo "   ├── models.py"
    echo "   ├── views.py"
    echo "   ├── tests.py"
    echo "   └── migrations/"
    echo "       └── __init__.py"
    echo ""
    echo "⚙️  Configuración actualizada:"
    echo "   - apps/$APP_NAME/apps.py: name = 'apps.$APP_NAME'"
    echo "   - core/settings.py: 'apps.$APP_NAME' agregado a INSTALLED_APPS"
    echo ""
    echo "🎯 Próximos pasos:"
    echo "   1. Editar apps/$APP_NAME/models.py para definir tus modelos"
    echo "   2. Ejecutar: uv run ./manage.py makemigrations $APP_NAME"
    echo "   3. Ejecutar: uv run ./manage.py migrate"
    echo "   4. Crear vistas en apps/$APP_NAME/views.py"
    echo "   5. Configurar URLs en core/urls.py"
else
    echo "❌ Error: La verificación de Django falló"
    echo "Restaurando archivos de backup..."
    
    # Restaurar backups si hay error
    if [ -f "$APPS_PY_FILE.backup" ]; then
        mv "$APPS_PY_FILE.backup" "$APPS_PY_FILE"
    fi
    if [ -f "$SETTINGS_FILE.backup" ]; then
        mv "$SETTINGS_FILE.backup" "$SETTINGS_FILE"
    fi
    
    # Mostrar el error específico
    echo "Detalles del error:"
    uv run ./manage.py check
    exit 1
fi

# Limpiar archivos de backup
rm -f "$APPS_PY_FILE.backup" "$SETTINGS_FILE.backup"

echo "🎉 ¡App creada y configurada correctamente!"
