import logging

from p2coffee.models import Brew, Machine, SensorEvent
from p2coffee.tasks import start_brewing

logger = logging.getLogger(__name__)

# FIXME values in watts are guesstimates
THRESHOLD_STARTED_WATTS = 1000
THRESHOLD_FINISHED_WATTS = 500


def _get_previous_value(sensor_event: SensorEvent):
    change_events = SensorEvent.objects.filter(
        name=SensorEvent.Name.METER_HAS_CHANGED.value, created__lt=sensor_event.created, id=sensor_event.id
    ).order_by("created")
    last_sensor_event = change_events.exclude(uuid=sensor_event.uuid).last()
    return float(last_sensor_event.value) if last_sensor_event else 0


def handle_event_created(sensor_event: SensorEvent):
    if sensor_event.name != SensorEvent.Name.METER_HAS_CHANGED.value:
        return  # Only changes are significant, ignore normal readings

    current_value = float(sensor_event.value)
    previous_value = _get_previous_value(sensor_event)

    # Compare current with previous and check if start or finished thresholds have been crossed
    if current_value >= THRESHOLD_STARTED_WATTS > previous_value:
        handle_started(sensor_event)
    elif current_value <= THRESHOLD_FINISHED_WATTS < previous_value:
        handle_finished(sensor_event)


def handle_started(sensor_event: SensorEvent):
    brew = Brew.objects.create(
        status=Brew.Status.BREWING.value, started_event=sensor_event, machine=sensor_event.machine
    )
    brew.machine.status = Machine.Status.BREWING.value
    brew.machine.save()
    start_brewing(brew)


def handle_finished(sensor_event: SensorEvent):
    """Note: It is start_brewing/update_progress responsibility to update slack with the changed brew status."""

    try:
        brew = Brew.objects.get(status=Brew.Status.BREWING.value, machine=sensor_event.machine)
    except Brew.DoesNotExist:
        logger.warning("Could not find matching brew to stop for this sensor event")
        return

    if brew.progress <= 50:
        brew.status = Brew.Status.INVALID.value
    else:
        brew.status = Brew.Status.FINISHED.value

    brew.finished_event = sensor_event
    brew.save()
    brew.machine.status = Machine.Status.IDLE.value
    brew.machine.save()
