from django.conf.urls import url
from monitoring.views import SensorView

urlpatterns = [
    url(r'^api/sensors/$', SensorView.as_view(),
        name='sensors_all'),
    url(r'^api/sensors/(?P<sensor_id>[0-9]+)$', SensorView.as_view(),
        name='sensors_specific'),
]
