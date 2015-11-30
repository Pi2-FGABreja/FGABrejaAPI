from django.db import models
from distutils.util import strtobool
import random


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

    def read_sensor(self):
        if self.sensor_type == "thermal":
            self.value = random.randint(81, 100)
        if self.sensor_type == "ldr":
            self.value = random.randint(0, 100)
        if self.sensor_type == "level":
            self.value = random.choice([True, False])
        self.save()

    def __str__(self):
        return "{} - {}, {}, {}".format(self.id, self.sensor_type,
                                        self.location, self.position)


class ThermalSensor(object):

    @classmethod
    def get_current_temperature_in(cls, location):
        sensors = Sensor.read.thermal()
        sensors = sensors.filter(location=location)
        return cls.calculate_temperature_average(sensors)

    @classmethod
    def calculate_temperature_average(cls, sensors):
        temperature_sum = 0
        for sensor in sensors:
            temperature_sum += float(sensor.value)
        return temperature_sum / sensors.count()


class LevelSensor(object):

    @classmethod
    def get_current_water_level_in(cls, location):
        sensors = Sensor.read.level()
        sensors = sensors.get(location=location)
        return bool(strtobool(sensors.value))
