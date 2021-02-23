from django.urls import path

from p2coffee.views import CreateSensorEventView, StatsView, StatsEvents, KindlyOutgoingView

urlpatterns = [
    path('event/log/', CreateSensorEventView.as_view(), name='create-log-event'),
    path('stats/', StatsView.as_view(), name='stats'),
    path('stats/events/', StatsEvents.as_view(), name='stats-events'),
    path('kindly/', KindlyOutgoingView.as_view(), name='kindly-outgoing'),
]
