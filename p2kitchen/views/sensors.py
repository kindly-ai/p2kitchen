from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View

from p2kitchen.forms import SensorEventForm
from p2kitchen.models import Machine
from p2kitchen.sensor_events import handle_event_created


class CreateSensorEventView(View):
    """
    Logs a sensor event and runs on_new_meter task

    EXAMPLE request:
        GET /event/log/?name=power-meter-has-changed&id=ZWayVDev_zway_2-0-49-4&value=4.6&device_name=dev2
    """

    def get(self, request, *args, **kwargs):
        form = SensorEventForm(request.GET)

        if not form.is_valid():
            return HttpResponseBadRequest("Curse you coffeepot!")

        event = form.save(commit=False)
        device_name = event.device_name
        machine, created = Machine.objects.get_or_create(device_name=device_name, defaults={"name": device_name})
        event.machine = machine
        event.save()

        handle_event_created(event)

        return HttpResponse("Thank you coffepot!")
