from django.db import models


class Sensor(models.Model):

    sensor_type = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    position = models.CharField(max_length=50)

    class Meta:
        abstract = True


class ThermalSensor(Sensor):

    sensor_type = "thermal"
    temperature = models.FloatField()


class LevelSensor(Sensor):

    sensor_type = "level"
    level = models.CharField(max_length=50)


class LDRSensor(Sensor):

    sensor_type = "ldr"
    luminosity = models.IntegerField()
