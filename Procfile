web: gunicorn coffeesite.wsgi
worker: python manage.py run_huey -w 2
release: python manage.py migrate --noinput