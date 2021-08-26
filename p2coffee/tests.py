from urllib.parse import urlencode

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from p2coffee.models import SensorEvent


class TestEvents(APITestCase):
    def test_event_create(self):

        query_params = {
            "name": "power-meter-has-changed",
            "id": "ZWayVDev_zway_2-0-49-4",
            "value": "4.6",
        }
        url = f'{reverse("create-log-event")}?{urlencode(query_params)}'
        print(url)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(SensorEvent.objects.count(), 1)
        event = SensorEvent.objects.get()
        self.assertEqual(event.name, query_params["name"])
        self.assertEqual(event.id, query_params["id"])
        self.assertEqual(event.value, query_params["value"])
