web: gunicorn p2kitchen.asgi:application -k uvicorn.workers.UvicornWorker
worker: python manage.py run_huey -w 2
release: python manage.py migrate --noinput
