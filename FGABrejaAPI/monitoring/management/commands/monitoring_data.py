from django.core.management.base import BaseCommand
from monitoring.models import Sensor


class Command(BaseCommand):
    help = "Create initial monitoring data"

    def handle(self, *args, **options):
        print("Creating thermal sensors...")
        Sensor.objects.create(sensor_type="thermal", location="pot1")
        Sensor.objects.create(sensor_type="thermal", location="pot1")
        Sensor.objects.create(sensor_type="thermal", location="pot2")
        Sensor.objects.create(sensor_type="thermal", location="pot2")
        Sensor.objects.create(sensor_type="thermal", location="freezer")
        Sensor.objects.create(sensor_type="thermal", location="freezer")

        print("Creating level sensors...")
        Sensor.objects.create(sensor_type="level", location="pot1")
        Sensor.objects.create(sensor_type="level", location="pot2")

        print("Creating LDR sensors...")
        Sensor.objects.create(sensor_type="ldr", location="airlock")
