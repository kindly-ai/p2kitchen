from braces.views import CsrfExemptMixin
from django.http import JsonResponse
from django.views import View

from p2coffee.models import CoffeePotEvent


class KindlyOutgoingView(CsrfExemptMixin, View):
    def post(self, request):
        # TODO: Rewrite using Brews
        last_event = CoffeePotEvent.objects.last()
        brewing_status = "I'm a coffee pot!"
        if last_event:
            brewing_status = last_event.as_slack_text()

        return JsonResponse({"reply": brewing_status})
