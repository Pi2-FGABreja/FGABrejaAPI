from django.views.generic import View
from django.http import HttpResponse
from .models import Sensor
from django.core import serializers


class SensorView(View):
    http_method_names = [u'get']

    def get(self, request, sensor_id=None):
        if sensor_id:
            sensors = Sensor.read.filter(id=sensor_id)
        else:
            sensors = Sensor.read.all()

        data = serializers.serialize("json", sensors)
        return HttpResponse(data, content_type='application/json')


def get_thermal_sensors(request):
    sensors = Sensor.read.thermal()
    data = serializers.serialize("json", sensors)
    return HttpResponse(data, content_type='application/json')


def get_level_sensors(request):
    sensors = Sensor.read.level()
    data = serializers.serialize("json", sensors)
    return HttpResponse(data, content_type='application/json')


def get_ldr_sensors(request):
    sensors = Sensor.read.ldr()
    data = serializers.serialize("json", sensors)
    return HttpResponse(data, content_type='application/json')
