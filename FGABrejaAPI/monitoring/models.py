from django.db import models
import random


class SensorManager(models.Manager):

    def all(self):
        sensors = Sensor.objects.all()
        for sensor in sensors:
            sensor.read_sensor()
        return sensors

    def filter(self, **kwargs):
        sensors = Sensor.objects.filter(**kwargs)
        for sensor in sensors:
            sensor.read_sensor()
        return sensors


class Sensor(models.Model):

    sensor_type = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    value = models.CharField(max_length=50)

    objects = models.Manager()
    read = SensorManager()

    def read_sensor(self):
        if self.sensor_type == "thermal":
            self.value = random.random() * 10
            self.save()
        if self.sensor_type == "ldr":
            self.value = random.randint(0, 100)
