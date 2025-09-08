# Dockerfile usando imagen oficial de uv
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Habilitar bytecode compilation para mejor rendimiento
ENV UV_COMPILE_BYTECODE=1

# Copiar archivos de configuración uv
COPY uv.lock pyproject.toml ./

# Instalar dependencias (sin el proyecto) - sin cache mount para Railway
RUN uv sync --frozen --no-install-project

# Copiar código fuente
COPY . .

# Instalar el proyecto - sin cache mount para Railway
RUN uv sync --frozen

# Crear directorio para archivos estáticos
RUN mkdir -p static

# Recopilar archivos estáticos
RUN uv run python manage.py collectstatic --noinput

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["sh", "-c", "uv run python manage.py migrate && uv run gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 120"]
