from django.urls import path

from p2coffee.views.kindly import KindlyOutgoingView
from p2coffee.views.sensors import CreateSensorEventView
from p2coffee.views.slack import SlackCommandView, SlackInteractionsView, SlackEventsView
from strawberry.django.views import AsyncGraphQLView
from p2coffee.schema import schema

urlpatterns = [
    path("event/log/", CreateSensorEventView.as_view(), name="create-log-event"),
    path("kindly/", KindlyOutgoingView.as_view(), name="kindly-outgoing"),
    path("slack/commands/", SlackCommandView.as_view(), name="slack-commands"),
    path("slack/interactions/", SlackInteractionsView.as_view(), name="slack-interactions"),
    path("slack/events/", SlackEventsView.as_view(), name="slack-events"),
    path("graphql", AsyncGraphQLView.as_view(schema=schema)),
]
