from datetime import timedelta
import json
from django.db import models
from django.utils import timezone


class Heat(models.Model):
    temperature = models.FloatField()
    duration = models.IntegerField()
    process_stage = models.CharField(max_length=50)


class Hop(models.Model):
    minutes = models.IntegerField()
    weight = models.FloatField()


class Valve(models.Model):
    is_open = models.BooleanField(default=False)


class Recipe(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    water_level = models.IntegerField()
    initial_boiling_temperature = models.FloatField()
    boiling_temperature = models.FloatField()
    boiling_duration = models.IntegerField()
    fermentation_temperature = models.FloatField(default=10)
    malt = models.CharField(max_length=250)
    malt_weight = models.FloatField()
    hops_order = models.CharField(max_length=255, blank=True)
    heat_order = models.CharField(max_length=255, blank=True)
    yeast = models.CharField(max_length=50)

    def set_hop_order(self, order):
        hop_order = {}
        for index, hop in enumerate(order, start=1):
            hop_order[index] = hop.id
        self.hops_order = json.dumps(hop_order)

    def get_hop_order(self):
        return json.loads(self.hops_order)

    def set_heat_order(self, order):
        heat_order = {}
        for index, heat in enumerate(order, start=1):
            heat_order[index] = heat.id
        self.heat_order = json.dumps(heat_order)

    def get_heat_order(self):
        return json.loads(self.heat_order)

    def insert_water_time(self):
        # Assuming water flow rate is 2L/minute
        minutes = self.water_level / 2
        return minutes


class Process(models.Model):
    initial_datetime = models.DateTimeField(auto_now_add=True)
    final_datetime = models.DateTimeField(null=True)
    recipe = models.ForeignKey('Recipe')
    iodine_test = models.BooleanField(default=False)
    malt = models.BooleanField(default=False)
    state = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    last_temperature = models.FloatField(default=0)

    actual_heat = models.ForeignKey('Heat', null=True)
    actual_heat_time = models.DateTimeField(null=True)
    next_heat = models.IntegerField(default=2)

    actual_hop = models.ForeignKey('Hop', null=True)
    next_hop = models.IntegerField(default=1)

    boiling_stop_time = models.DateTimeField(null=True)
    filtering_init = models.DateTimeField(null=True)

    @classmethod
    def current(cls):
        try:
            return cls.objects.get(is_active=True)
        except:
            return None

    def change_heat(self):
        now = timezone.now()
        delta = now - self.actual_heat_time
        if delta >= timedelta(minutes=self.actual_heat.duration):
            return True
        elif self.actual_heat_time is None:
            return True
        else:
            return False

    def change_hop(self):
        now = timezone.now()
        delta = self.boiling_stop_time - now
        if delta <= timedelta(minutes=self.actual_hop.minutes):
            return True
        elif self.boiling_stop_time is None:
            return False
        else:
            return False
