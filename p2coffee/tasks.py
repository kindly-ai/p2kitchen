import logging
from django.conf import settings
from huey.contrib.djhuey import db_task, task
from p2coffee import slack
from p2coffee.models import SensorEvent, Brew


logger = logging.getLogger(__name__)

# FIXME values in watts are guesstimates
THRESHOLD_STARTED_WATTS = 1000
THRESHOLD_FINISHED_WATTS = 500
UPDATE_DELAY_SECONDS = 3


def on_new_meter(sensor_event: SensorEvent):
    current_value = float(sensor_event.value)

    if sensor_event.name != SensorEvent.Name.METER_HAS_CHANGED.value:
        return  # Only changes are significant, ignore normal readings

    # Get previous event value
    change_events = SensorEvent.objects.filter(
        name=SensorEvent.Name.METER_HAS_CHANGED.value,
        created__lt=sensor_event.created,
        id=sensor_event.id,
    ).order_by("created")
    last_sensor_event = change_events.exclude(uuid=sensor_event.uuid).last()
    previous_value = float(last_sensor_event.value) if last_sensor_event else 0

    # Compare current with previous and check if start or finished thresholds have been crossed
    if current_value >= THRESHOLD_STARTED_WATTS > previous_value:
        brew = Brew.objects.create(
            status=Brew.Status.BREWING.value, started_event=sensor_event, machine=sensor_event.machine
        )
        start_brewing(brew)
    elif current_value <= THRESHOLD_FINISHED_WATTS < previous_value:
        # A brew is done
        try:
            brew = Brew.objects.get(status=Brew.Status.BREWING.value, id=sensor_event.id, machine=sensor_event.machine)
        except Brew.DoesNotExist:
            logger.warning("Could not find matching brew to stop for this sensor event")
            return

        # Note: It is start_brewing/update_progress responsibility to update slack with the changed brew status.
        brew.status = Brew.Status.FINISHED.value
        brew.finished_event = sensor_event
        brew.save()


@task()
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

    newer_brews = Brew.objects.filter(created__gt=brew.created).order_by("created")
    if len(newer_brews) == 0:
        message = brew.update_message()
        slack.chat_update(brew.slack_channel, brew.slack_ts, **message)
        update_progress.schedule(args=(brew_pk,), delay=UPDATE_DELAY_SECONDS)
        return

    for new_event in newer_brews:
        if new_event.type == Brew.Status.BREWING_FINISHED.value:
            message = brew.finished_message()
            slack.chat_update(brew.slack_channel, brew.slack_ts, **message)
            return

    # Multiple brewings started without finishing. This shouldn't happen.
    raise RuntimeError("Invalid coffee pot state.")
