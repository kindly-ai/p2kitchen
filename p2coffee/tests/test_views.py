from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from p2coffee.models import SensorEvent


def test_sensor_event_create(db, api_client: APIClient):
    params = {
        "name": "power-meter-has-changed",
        "id": "ZWayVDev_zway_2-0-49-4",
        "value": "4.6",
    }
    url = f'{reverse("create-log-event")}'

    assert SensorEvent.objects.count() == 0

    response = api_client.get(url, data=params, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert SensorEvent.objects.count() == 1
    event = SensorEvent.objects.get()

    assert event.name == params["name"]
    assert event.id == params["id"]
    assert event.value == params["value"]
