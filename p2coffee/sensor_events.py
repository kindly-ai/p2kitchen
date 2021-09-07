import logging

from p2coffee.models import SensorEvent, Brew

from p2coffee.tasks import start_brewing

logger = logging.getLogger(__name__)

# FIXME values in watts are guesstimates
THRESHOLD_STARTED_WATTS = 1000
THRESHOLD_FINISHED_WATTS = 500


def handle_event_created(sensor_event: SensorEvent):
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
