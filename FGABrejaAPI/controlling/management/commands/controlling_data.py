from django.core.management.base import BaseCommand
from controlling.models import Hop, Heat, Recipe


class Command(BaseCommand):
    help = "Create initial controlling data"

    def handle(self, *args, **options):
        print("Creating Red Ale recipe...")
        print("- Adding hops")
        hop1 = Hop.objects.create(minutes=60, weight=0.20)
        hop2 = Hop.objects.create(minutes=30, weight=0.20)
        hop3 = Hop.objects.create(minutes=15, weight=0.0)
        hop4 = Hop.objects.create(minutes=10, weight=0.20)
        hops = [hop1, hop2, hop3, hop4]

        print("- Setting heatings")
        heat1 = Heat.objects.create(temperature=65.0, duration=25,
                                    process_stage="brewery")
        heat2 = Heat.objects.create(temperature=72.0, duration=25,
                                    process_stage="brewery")
        heat3 = Heat.objects.create(temperature=80.0, duration=10,
                                    process_stage="brewery")
        heats = [heat1, heat2, heat3]

        recipe = Recipe()
        recipe.name = "Red Ale"
        recipe.description = "5.84% teor de álcool"
        recipe.malt = "75% Pilsen, 10% Malte de trigo, 10% CaraAmber, "
        "5% CaraAroma"
        recipe.water_level = 20
        recipe.initial_boiling_temperature = 65.0
        recipe.boiling_temperature = 90.0
        recipe.boiling_duration = 90
        recipe.malt_weight = 5.0
        recipe.fermentation_temperature = 10
        recipe.set_hop_order(hops)
        recipe.set_heat_order(heats)
        recipe.yeast = "BRY-97"
        recipe.save()

        print("Creating Test recipe...")
        print("- Adding hops")
        hop1 = Hop.objects.create(minutes=4, weight=0.20)
        hop2 = Hop.objects.create(minutes=3, weight=0.20)
        hop3 = Hop.objects.create(minutes=2, weight=0.0)
        hop4 = Hop.objects.create(minutes=1, weight=0.20)
        hops = [hop1, hop2, hop3, hop4]

        print("- Setting heatings")
        heat1 = Heat.objects.create(temperature=65.0, duration=2,
                                    process_stage="brewery")
        heat2 = Heat.objects.create(temperature=72.0, duration=2,
                                    process_stage="brewery")
        heat3 = Heat.objects.create(temperature=80.0, duration=2,
                                    process_stage="brewery")
        heats = [heat1, heat2, heat3]

        recipe = Recipe()
        recipe.name = "Test",
        recipe.description = "5.84% teor de álcool"
        recipe.malt = "75% Pilsen, 10% Malte de trigo, 10% CaraAmber, "
        "5% CaraAroma"
        recipe.water_level = 20
        recipe.initial_boiling_temperature = 65.0
        recipe.boiling_temperature = 90.0
        recipe.boiling_duration = 6
        recipe.malt_weight = 5.0
        recipe.fermentation_temperature = 10
        recipe.set_hop_order(hops)
        recipe.set_heat_order(heats)
        recipe.yeast = "BRY-97"
        recipe.save()
