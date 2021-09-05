## Get started
```shell
pipenv install --dev
pipenv run python manage.py migrate
pipenv run python manage.py createsuperuser
cp .env.default .env  # Add your keys
pipenv run python manage.py runserver  # Run server
pipenv run python manage.py run_huey -w 2  # Run worker
```

## Environment variables
- `SLACK_CHANNEL`
- `SLACK_API_TOKEN`
- `SLACK_SIGNING_SECRET`
