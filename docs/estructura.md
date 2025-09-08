# Estructura del proyecto (Django 5.2)

```
/core
  asgi.py
  settings.py
  urls.py
  wsgi.py
/apps
  category/
    __init__.py
    admin.py
    apps.py
    models.py
    views.py
    ...
  users/
    __init__.py
    admin.py
    apps.py
    models.py
    views.py
    ...
manage.py
pyproject.toml
README.md
uv.lock
db.sqlite3
```

- `core/settings.py`: configuración base del proyecto.
- `core/urls.py`: enrutamiento principal (usar `path()` de Django 5.2).
- `core/asgi.py` y `core/wsgi.py`: entrypoints ASGI/WSGI.
- `manage.py`: utilitario para comandos `uv run ./manage.py`.
- `apps/`: carpeta contenedora de todas las apps Django.

Base de datos predeterminada: SQLite (`db.sqlite3`).

## Comandos para crear apps
- **Makefile (recomendado)**: `make create APP=<nombre_app>`
  - Ejemplo: `make create APP=categories`
  - Ejemplo: `make create APP=users`
  - Ejemplo: `make create APP=orders`

- **Script directo**: `./scripts/create_app.sh <nombre_app>`
  - Ejemplo: `./scripts/create_app.sh categories`

- **Método manual**:
  1. `uv run ./manage.py startapp <nombre_app>`
  2. `mv <nombre_app> apps/`
  3. Editar `apps/<nombre_app>/apps.py` → `name = 'apps.<nombre_app>'`
  4. Agregar `'apps.<nombre_app>'` a `INSTALLED_APPS`

## Comandos de desarrollo
- `make dev` - iniciar servidor de desarrollo
- `make check` - verificar configuración Django
- `make migrate` - aplicar migraciones
- `make makemigrations` - crear migraciones
- `make shell` - abrir shell de Django
- `make test` - ejecutar tests
- `make help` - mostrar todos los comandos disponibles


