from django.urls import reverse
from django.views.generic import TemplateView
from itertools import groupby

from rest_framework.response import Response
from rest_framework.views import APIView

from p2coffee.models import SensorEvent, CoffeePotEvent, SensorName


class StatsView(TemplateView):
    template_name = "p2coffee/stats.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            {
                "last_state": self._get_last_power_state(),
                "last_brew": self._get_last_coffee_event(),
                "urls": {"stats-events": reverse("stats-events")},
            }
        )

        return context

    def _get_last_power_state(self):
        return SensorEvent.objects.filter(name=SensorName.SWITCH.value).last()

    def _get_last_coffee_event(self):
        return CoffeePotEvent.objects.last()


class StatsEvents(APIView):
    """List events grouped by name, in highcharts friendly format."""

    def get(self, request, format=None):
        return Response(self._get_events())

    def _get_events(self):
        events = SensorEvent.objects.filter(name=SensorName.METER_HAS_CHANGED.value).values("name", "value", "created")

        # Group the data
        keyfunc = lambda x: x["name"]
        event_groups = []
        data = sorted(events, key=keyfunc)
        for key, group in groupby(data, keyfunc):
            event_groups.append({"name": key, "data": self._events_to_highcharts_format(group)})

        return event_groups

    def _events_to_highcharts_format(self, events):
        return list(map(lambda e: [e["created"].timestamp() * 1000, float(e["value"])], events))
