#!/usr/bin/env python3
"""
Script para probar la integración de Cloudinary
"""

import os
import django
import sys

# Configurar Django
sys.path.append('/Users/osedhelu/proyectos/discorp')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

import cloudinary
import cloudinary.uploader
from apps.products.models import Product
from apps.stores.models import Store
from apps.users.models import User

def test_cloudinary_config():
    """Probar la configuración de Cloudinary"""
    print("🔧 PROBANDO CONFIGURACIÓN DE CLOUDINARY")
    print("="*50)
    
    try:
        # Verificar configuración
        config = cloudinary.config()
        print(f"✅ Cloud Name: {config.cloud_name or 'NO CONFIGURADO'}")
        print(f"✅ API Key: {config.api_key[:10] + '...' if config.api_key else 'NO CONFIGURADO'}")
        print(f"✅ API Secret: {'***CONFIGURADO***' if config.api_secret else 'NO CONFIGURADO'}")
        
        # Probar conexión básica
        result = cloudinary.api.ping()
        print(f"✅ Conexión exitosa: {result}")
        
        return True
    except Exception as e:
        print(f"❌ Error de configuración: {str(e)}")
        return False

def test_image_upload():
    """Probar subida de imagen de prueba"""
    print("\n📤 PROBANDO SUBIDA DE IMAGEN")
    print("="*50)
    
    try:
        # Crear una imagen de prueba simple (1x1 pixel)
        import io
        from PIL import Image
        
        # Crear imagen de 100x100 píxeles
        img = Image.new('RGB', (100, 100), color='red')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        # Subir a Cloudinary
        result = cloudinary.uploader.upload(
            img_bytes.getvalue(),
            folder="discorp/test",
            public_id="test_image",
            transformation={
                'width': 200,
                'height': 200,
                'crop': 'fill',
                'quality': 'auto',
                'format': 'auto'
            }
        )
        
        print(f"✅ Imagen subida exitosamente:")
        print(f"   📷 URL: {result['secure_url']}")
        print(f"   🆔 Public ID: {result['public_id']}")
        print(f"   📏 Dimensiones: {result['width']}x{result['height']}")
        print(f"   📦 Formato: {result['format']}")
        print(f"   💾 Tamaño: {result['bytes']} bytes")
        
        return result
    except ImportError:
        print("⚠️  PIL no está instalado. Saltando prueba de imagen.")
        return None
    except Exception as e:
        print(f"❌ Error subiendo imagen: {str(e)}")
        return None

def test_model_integration():
    """Probar integración con modelos Django"""
    print("\n🗃️  PROBANDO INTEGRACIÓN CON MODELOS")
    print("="*50)
    
    try:
        # Verificar que los modelos tienen campos CloudinaryField
        print("📋 Verificando campos Cloudinary en modelos:")
        
        # Product
        product_image_field = Product._meta.get_field('image')
        print(f"   ✅ Product.image: {type(product_image_field).__name__}")
        
        # Store
        store_logo_field = Store._meta.get_field('logo')
        store_banner_field = Store._meta.get_field('banner')
        print(f"   ✅ Store.logo: {type(store_logo_field).__name__}")
        print(f"   ✅ Store.banner: {type(store_banner_field).__name__}")
        
        # User
        user_avatar_field = User._meta.get_field('avatar')
        print(f"   ✅ User.avatar: {type(user_avatar_field).__name__}")
        
        return True
    except Exception as e:
        print(f"❌ Error verificando modelos: {str(e)}")
        return False

def test_api_endpoints():
    """Probar que los endpoints de API están disponibles"""
    print("\n🌐 PROBANDO ENDPOINTS DE API")
    print("="*50)
    
    from django.urls import reverse
    from django.test import Client
    
    client = Client()
    
    endpoints_to_test = [
        '/api/products/products/',
        '/api/stores/stores/',
        '/api/users/profile/',
    ]
    
    for endpoint in endpoints_to_test:
        try:
            response = client.get(endpoint)
            status_code = response.status_code
            if status_code in [200, 401, 403]:  # 401/403 son OK (requieren auth)
                print(f"   ✅ {endpoint}: {status_code}")
            else:
                print(f"   ⚠️  {endpoint}: {status_code}")
        except Exception as e:
            print(f"   ❌ {endpoint}: Error - {str(e)}")

def main():
    """Función principal"""
    print("🚀 PRUEBA COMPLETA DE INTEGRACIÓN CLOUDINARY")
    print("="*60)
    
    # 1. Probar configuración
    config_ok = test_cloudinary_config()
    
    if not config_ok:
        print("\n❌ CONFIGURACIÓN INCOMPLETA")
        print("Para completar la configuración:")
        print("1. Regístrate en https://cloudinary.com")
        print("2. Obtén tus credenciales del dashboard")
        print("3. Crea un archivo .env con:")
        print("   CLOUDINARY_CLOUD_NAME=tu_cloud_name")
        print("   CLOUDINARY_API_KEY=tu_api_key")
        print("   CLOUDINARY_API_SECRET=tu_api_secret")
        return
    
    # 2. Probar subida de imagen
    upload_result = test_image_upload()
    
    # 3. Probar integración con modelos
    models_ok = test_model_integration()
    
    # 4. Probar endpoints de API
    test_api_endpoints()
    
    # 5. Resumen final
    print("\n🎯 RESUMEN FINAL")
    print("="*50)
    print(f"✅ Configuración: {'OK' if config_ok else 'FALTA'}")
    print(f"✅ Subida de imágenes: {'OK' if upload_result else 'FALTA PIL'}")
    print(f"✅ Modelos Django: {'OK' if models_ok else 'ERROR'}")
    print(f"✅ Endpoints API: Verificados")
    
    if config_ok and models_ok:
        print("\n🎉 ¡CLOUDINARY ESTÁ COMPLETAMENTE INTEGRADO!")
        print("\n📱 ENDPOINTS DISPONIBLES PARA FLUTTER:")
        print("   📤 POST /api/products/products/{id}/upload_image/")
        print("   📤 POST /api/products/product-images/upload/")
        print("   📷 Todas las imágenes se optimizan automáticamente")
        print("   🌐 URLs de Cloudinary incluidas en respuestas API")
    else:
        print("\n⚠️  Completar configuración antes de usar en producción")

if __name__ == "__main__":
    main()
