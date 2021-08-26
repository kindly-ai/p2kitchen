from braces.views import CsrfExemptMixin
from django.http import JsonResponse
from django.views import View


class SlackCommandView(CsrfExemptMixin, View):
    def post(self, request):
        """
        Example payload
        token=J976UOaX90V4rGyVxgHiZUVg&
        team_id=T0X80BHB8&
        team_domain=kindly-ai&
        channel_id=CD42RPZL7&
        channel_name=kitchen-dev&
        user_id=U85U5A4P5&
        user_name=nikolai.kristiansen&
        command=%2Fkitchen&
        text=help&
        api_app_id=A02CFA4KU2W&
        is_enterprise_install=false&
        response_url=https%3A%2F%2Fhooks.slack.com%2Fcommands%2FT0X80BHB8%2F2423424164626%2FiF1N6kkODOR7LJ3WnQMctgp0&
        trigger_id=2436038963537.31272391382.9966ca317f21653896d09baef2f77320
        """
        print(request.POST)
        payload = {
            "response_type": "in_channel",
            "text": "Yo! hypp på noe varmt brygg?",
        }
        return JsonResponse(payload)
