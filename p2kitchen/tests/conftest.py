from datetime import timedelta

import pytest
from django.conf import settings
from django.utils.timezone import now
from freezegun import freeze_time

from p2kitchen.models import Brew, Machine, SensorEvent

SENSOR_ID = "ZWayVDev_zway_2-0-49-4"
BASE_SENSOR_DATA = {"id": SENSOR_ID, "name": "power-meter-has-changed", "device_name": "dev2"}


@pytest.fixture
def machine(db):
    return Machine.objects.create(name="Grutenberg", device_name=SENSOR_ID)


@pytest.fixture
def sensor_events_started(machine):
    idle_watts = "0.0"
    started_watts = "1200"

    with freeze_time(now() - timedelta(seconds=settings.BREWTIME_AVG_SECONDS)):
        idle = SensorEvent.objects.create(**BASE_SENSOR_DATA, value=idle_watts, machine=machine)
        started = SensorEvent.objects.create(**BASE_SENSOR_DATA, value=started_watts, machine=machine)
    return idle, started


@pytest.fixture
def brew(sensor_events_started, machine):
    started = sensor_events_started[1]
    return Brew.objects.create(started_event=started, machine=machine)


@pytest.fixture
def sensor_event_finished(brew):
    finished_watts = "500.0"
    return SensorEvent.objects.create(**BASE_SENSOR_DATA, value=finished_watts, machine=brew.machine)
