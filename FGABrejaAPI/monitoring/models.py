from controlling.comunication import Comunication
from django.db import models
from distutils.util import strtobool


class SensorManager(models.Manager):

    def read(self, sensors):
        for sensor in sensors:
            sensor.read_sensor()
        return sensors

    def all(self):
        sensors = Sensor.objects.all()
        return self.read(sensors)

    def filter(self, **kwargs):
        sensors = Sensor.objects.filter(**kwargs)
        return self.read(sensors)

    def thermal(self):
        sensors = Sensor.objects.filter(sensor_type="thermal")
        return self.read(sensors)

    def level(self):
        sensors = Sensor.objects.filter(sensor_type="level")
        return self.read(sensors)

    def ldr(self):
        sensors = Sensor.objects.filter(sensor_type="ldr")
        return self.read(sensors)


class Sensor(models.Model):

    sensor_type = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    value = models.CharField(max_length=50, default=0)

    objects = models.Manager()
    read = SensorManager()
    serial_comunication = Comunication()

    def read_sensor(self):
        if self.sensor_type == "thermal":
            self.value = self.serial_comunication.read_thermal_sensor()
        if self.sensor_type == "level":
            self.value = self.serial_comunication.get_pot_level()
        self.save()

    def __str__(self):
        return "{} - {}, {}, {}".format(self.id, self.sensor_type,
                                        self.location, self.position)


class ThermalSensor(object):

    @classmethod
    def get_current_temperature(cls):
        sensors = Sensor.read.thermal()
        sensors = sensors.get(pk=1)
        return float(sensors.value)


class LevelSensor(object):

    @classmethod
    def get_current_water_level(cls):
        sensors = Sensor.read.level()
        sensors = sensors.get(pk=2)
        return bool(strtobool(sensors.value))
