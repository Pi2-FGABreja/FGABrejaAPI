from django.conf.urls import url, include
from monitoring.views import (SensorView, get_ldr_sensors, get_level_sensors,
                              get_thermal_sensors, get_average_temperature)
from controlling import views
from tastypie.api import Api
from controlling.resources import ProcessResource, RecipeResource

controlling_api = Api(api_name='controlling')
controlling_api.register(ProcessResource())
controlling_api.register(RecipeResource())

urlpatterns = [
    url(r'^api/sensors/$', SensorView.as_view(),
        name='sensors_all'),
    url(r'^api/sensors/(?P<sensor_id>[0-9]+)$', SensorView.as_view(),
        name='sensors_specific'),

    url(r'^api/sensors/thermal/$', get_thermal_sensors, name='thermal'),
    url(r'^api/sensors/thermal/average/$', get_average_temperature,
        name='thermal_average'),
    url(r'^api/sensors/level/$', get_level_sensors, name='level'),
    url(r'^api/sensors/ldr/$', get_ldr_sensors, name='ldr'),
    url(r'^api/', include(controlling_api.urls)),
    url(r'^api/controlling/process/create/$', views.create_process)
]
