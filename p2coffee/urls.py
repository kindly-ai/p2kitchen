from django.conf.urls import url

from p2coffee.views import CreateSensorEventView, StatsView, StatsEvents, KindlyOutgoingView

urlpatterns = [
    url(r'^event/log/$', CreateSensorEventView.as_view(), name='create-log-event'),
    url(r'^stats/$', StatsView.as_view(), name='stats'),
    url(r'^stats/events/$', StatsEvents.as_view(), name='stats-events'),
    url(r'^kindly/$', KindlyOutgoingView.as_view(), name='kindly-outgoing'),
]
