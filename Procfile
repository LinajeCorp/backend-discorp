web: uv run gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 120
release: uv run python manage.py migrate
