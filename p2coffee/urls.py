from django.urls import path

from p2coffee.views.kindly import KindlyOutgoingView
from p2coffee.views.sensors import CreateSensorEventView
from p2coffee.views.slack import SlackCommandView
from p2coffee.views.stats import StatsView, StatsEvents

urlpatterns = [
    path("event/log/", CreateSensorEventView.as_view(), name="create-log-event"),
    path("stats/", StatsView.as_view(), name="stats"),
    path("stats/events/", StatsEvents.as_view(), name="stats-events"),
    path("kindly/", KindlyOutgoingView.as_view(), name="kindly-outgoing"),
    path("slack/commands/", SlackCommandView.as_view(), name="slack-commands"),
]
