web: gunicorn p2kitchen.asgi:application -k uvicorn.workers.UvicornWorker
worker: python manage.py run_huey -w 2
# FIXME: Remove after deploy
release: python manage.py rename_app p2coffee p2kitchen && python manage.py migrate --noinput
