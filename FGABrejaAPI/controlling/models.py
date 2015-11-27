from django.db import models


class Heat(models.Model):
    temperature = models.FloatField()
    duration = models.IntegerField()


class Hop(models.Model):
    minutes = models.IntegerField()
    weight = models.FloatField()


class Recipe(models.Model):
    heaters = models.ForeignKey('Heat')
    hops = models.ForeignKey('Hop')


class Process(models.Model):
    initial_datetime = models.DateTimeField(auto_now=True)
    final_datetime = models.DateTimeField(null=True)
    recipe = models.ForeignKey('Recipe')
    iodine_test = models.BooleanField(default=False)
    malt = models.BooleanField(default=False)
    state = models.IntegerField()
    level_po1 = models.BooleanField(default=False)
    level_pot2 = models.BooleanField(default=False)
