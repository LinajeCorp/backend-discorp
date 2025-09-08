# Makefile para proyecto Django con uv
# Uso: make <comando>

.PHONY: help dev create install check migrate makemigrations shell test clean

# Variables
PYTHON := uv run python
MANAGE := uv run ./manage.py
APP_SCRIPT := ./scripts/create_app.sh

# Comando por defecto - mostrar ayuda
help:
	@echo "🚀 Comandos disponibles para el proyecto Django:"
	@echo ""
	@echo "📦 Desarrollo:"
	@echo "  make dev          - Iniciar servidor de desarrollo Django"
	@echo "  make install      - Instalar dependencias con uv"
	@echo ""
	@echo "🏗️  Apps:"
	@echo "  make create APP=<nombre> - Crear nueva app Django en apps/"
	@echo "  make create-app APP=<nombre> - Alias para make create"
	@echo ""
	@echo "🗄️  Base de datos:"
	@echo "  make migrate      - Aplicar migraciones"
	@echo "  make makemigrations - Crear migraciones"
	@echo "  make makemigrations-app APP=<nombre> - Crear migraciones para app específica"
	@echo ""
	@echo "🔧 Utilidades:"
	@echo "  make check        - Verificar configuración Django"
	@echo "  make shell        - Abrir shell de Django"
	@echo "  make test         - Ejecutar tests"
	@echo "  make clean        - Limpiar archivos temporales"
	@echo ""
	@echo "📋 Ejemplos:"
	@echo "  make dev"
	@echo "  make create APP=users"
	@echo "  make create APP=orders"
	@echo "  make makemigrations-app APP=users"

# Servidor de desarrollo
dev:
	@echo "🚀 Iniciando servidor de desarrollo Django..."
	$(MANAGE) runserver

# Instalar dependencias
install:
	@echo "📦 Instalando dependencias con uv..."
	uv sync

# Crear nueva app
create:
	@if [ -z "$(APP)" ]; then \
		echo "❌ Error: Debes especificar el nombre de la app"; \
		echo "Uso: make create APP=<nombre_app>"; \
		echo "Ejemplo: make create APP=users"; \
		exit 1; \
	fi
	@echo "🏗️  Creando app Django: $(APP)"
	$(APP_SCRIPT) $(APP)

# Alias para create
create-app: create

# Verificar configuración
check:
	@echo "🔍 Verificando configuración Django..."
	$(MANAGE) check

# Aplicar migraciones
migrate:
	@echo "🗄️  Aplicando migraciones..."
	$(MANAGE) migrate

# Crear migraciones
makemigrations:
	@echo "📝 Creando migraciones..."
	$(MANAGE) makemigrations

# Crear migraciones para app específica
makemigrations-app:
	@if [ -z "$(APP)" ]; then \
		echo "❌ Error: Debes especificar el nombre de la app"; \
		echo "Uso: make makemigrations-app APP=<nombre_app>"; \
		echo "Ejemplo: make makemigrations-app APP=users"; \
		exit 1; \
	fi
	@echo "📝 Creando migraciones para app: $(APP)"
	$(MANAGE) makemigrations $(APP)

# Shell de Django
shell:
	@echo "🐚 Abriendo shell de Django..."
	$(MANAGE) shell

# Ejecutar tests
test:
	@echo "🧪 Ejecutando tests..."
	$(MANAGE) test

# Limpiar archivos temporales
clean:
	@echo "🧹 Limpiando archivos temporales..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage

# Comando para crear superusuario
createsuperuser:
	@echo "👤 Creando superusuario..."
	$(MANAGE) createsuperuser

# Comando para recopilar archivos estáticos
collectstatic:
	@echo "📁 Recopilando archivos estáticos..."
	$(MANAGE) collectstatic --noinput

# Comando para mostrar migraciones pendientes
showmigrations:
	@echo "📋 Mostrando migraciones..."
	$(MANAGE) showmigrations

# Comando para mostrar SQL de una migración
sqlmigrate:
	@if [ -z "$(APP)" ] || [ -z "$(MIGRATION)" ]; then \
		echo "❌ Error: Debes especificar APP y MIGRATION"; \
		echo "Uso: make sqlmigrate APP=<nombre_app> MIGRATION=<numero_migracion>"; \
		echo "Ejemplo: make sqlmigrate APP=users MIGRATION=0001"; \
		exit 1; \
	fi
	@echo "📄 Mostrando SQL de migración: $(APP) $(MIGRATION)"
	$(MANAGE) sqlmigrate $(APP) $(MIGRATION)
