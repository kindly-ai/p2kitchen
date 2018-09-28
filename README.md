## Install
    pipenv install
    pipenv run python manage.py migrate

## Development tasks
    # Run worker
    pipenv run python manage.py run_huey -w 2


## Environment variables
- `SLACK_CHANNEL`
- `SLACK_API_TOKEN`
- `SLACK_BOT_USERNAME`
- `SLACK_WEBHOOK_URL`

## TODO
- More stats
- Management command that can create proper coffepot events from sensor events
