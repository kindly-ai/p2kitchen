import responses

from p2coffee.models import Brew, Machine
from p2coffee.sensor_events import handle_event_created


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


@responses.activate
def test_sensor_event_finishes_brew(sensor_event_finished, brew):
    assert brew.status == Brew.Status.BREWING.value

    handle_event_created(sensor_event_finished)

    brew.refresh_from_db()
    assert Brew.objects.count() == 1
    assert brew.status == Brew.Status.FINISHED.value
    assert brew.machine.status == Machine.Status.IDLE.value
