import pytest
import responses

from p2coffee.models import SensorEvent, Brew, Machine
from p2coffee.sensor_events import handle_event_created

SENSOR_ID = "ZWayVDev_zway_2-0-49-4"


@pytest.fixture
def machine(db):
    return Machine.objects.create(name="Grutenberg", device_name=SENSOR_ID)


@pytest.fixture
def sensor_events_started(db, machine):
    idle_watts = "0.0"
    started_watts = "1200"
    sensor_data = {"id": SENSOR_ID, "name": "power-meter-has-changed"}

    idle = SensorEvent.objects.create(**sensor_data, value=idle_watts, machine=machine)
    started = SensorEvent.objects.create(**sensor_data, value=started_watts, machine=machine)
    return idle, started


@responses.activate
def test_two_sensor_event_creates_brew(sensor_events_started):
    responses.add(
        responses.POST,
        "https://slack.com/api/chat.postMessage",
        json={"ok": True, "channel": "asdf", "ts": "1234"},
        status=200,
    )
    idle, started = sensor_events_started
    assert Brew.objects.count() == 0

    handle_event_created(started)

    assert Brew.objects.count() == 1
    brew = Brew.objects.get()
    assert brew.status == Brew.Status.BREWING.value
    assert brew.machine.status == Machine.Status.BREWING.value
