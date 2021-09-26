import logging
from django.conf import settings
from huey.contrib.djhuey import db_task
from p2coffee import slack
from p2coffee.models import Brew


logger = logging.getLogger(__name__)

UPDATE_DELAY_SECONDS = 3


@db_task()
def start_brewing(brew: Brew):
    logger.debug("Starting brewing")
    message = brew.started_message()
    response = slack.chat_post_message(settings.SLACK_CHANNEL, **message)

    brew.slack_channel = response["channel"]
    brew.slack_ts = response["ts"]
    brew.save()

    update_progress.schedule(args=(brew.pk,), delay=UPDATE_DELAY_SECONDS)


@db_task()
def update_progress(brew_pk):
    logger.debug("Updating progress")
    try:
        brew = Brew.objects.get(pk=brew_pk)
    except Brew.DoesNotExist:
        logger.error(f"Critical error! Brew {brew_pk} doesn't exist.")
        return

    if brew.status == Brew.Status.FINISHED.value:
        message = brew.finished_message()
        slack.chat_update(brew.slack_channel, brew.slack_ts, **message)
        return
    elif brew.status == Brew.Status.INVALID.value:
        slack.chat_delete(brew.slack_channel, brew.slack_ts)
        return

    message = brew.update_message()
    slack.chat_update(brew.slack_channel, brew.slack_ts, **message)
    # Keep updating progress
    update_progress.schedule(args=(brew_pk,), delay=UPDATE_DELAY_SECONDS)
