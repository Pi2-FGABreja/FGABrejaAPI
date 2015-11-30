from monitoring.models import ThermalSensor
from controlling.models import Hop
from controlling.models import Heat
from django.utils import timezone
import logging

logger = logging.getLogger('fga-breja')

STATES = {'warm_must': 1,
          'add_hops': 2
          }


class BoilingControll(object):

    def __init__(self, process):
        process.actual_heat = Heat.objects.get(pk=self.heat_order.get('3'))
        process.save()
        self.process = process
        self.hops_order = self.process.recipe.get_hop_order()

    def handle_states(self):
        state = self.process.state
        if state == STATES.get('warm_must'):
            logger.info("[Boiling] Warming must. . .")
            self.process.actual_heat.temperature = 97
            self.warm_must()
        elif state == STATES.get('add_hops'):
            logger.info("[Boiling] Adding hops to pot2. . .")
            self.add_hops()

    def warm_must(self):
        temperature = ThermalSensor.get_current_temperature_in('panela2')
        if temperature < self.process.actual_heat.temperature:
            logger.info("[Boiling] Temperature less than actual "
                        "heat temperature")
            # Increase temperature
            pass
        else:
            logger.info("[Boiling] Temperature reached!")
            self.process.actual_heat_time = timezone.now()
            self.process.state = STATES.get('add_hops')
            logger.info("[Boining] State changed! New state: add_hops")
        self.process.save()

    def add_hops(self):
        if self.process.change_hop():
            logger.info('[Boiling] Hop has been added to the pot!')
            if self.check_next():
                hops = Hop.objects.get(pk=self.get_next_hop())
                self.process.next_hop += 1
                self.process.actual_hop = hops
                self.process.state = STATES.get('add_hops')
                logger.info("[Boiling] State changed! New state: add_hops")
            else:
                self.process.state = STATES.get('turn_on_chiller')
                logger.info("[Boiling] State changed! "
                            "New state: turn_on_chiller")
        else:
            # No more hops to add
            pass
        self.process.save()

    def check_next(self):
        if self.process.next_hop <= len(self.hop_order):
            return True
        else:
            return False

    def get_next_hop(self):
        next_hop = self.process.next_hop
        return self.hop_order.get(str(next_hop))
