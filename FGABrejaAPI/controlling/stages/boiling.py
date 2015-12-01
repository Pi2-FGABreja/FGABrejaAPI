from monitoring.models import ThermalSensor
from controlling.models import Hop
from controlling.models import Heat
from controlling.stages import cooling
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger('fga-breja')

STATES = {'warm_must': 1,
          'add_hops': 2,
          'continue_boiling': 3
          }


class BoilingControll(object):

    def __init__(self, process):
        self.heat_order = process.recipe.get_heat_order()
        self.hop_order = process.recipe.get_hop_order()
        process.actual_heat = Heat.objects.get(pk=self.heat_order.get('1'))
        process.actual_hop = Hop.objects.get(pk=self.hop_order.get('1'))
        process.save()
        self.process = process

    def handle_states(self):
        state = self.process.state
        if state == STATES.get('warm_must'):
            logger.info("[Boiling] Function defined: warm_must")
            self.process.actual_heat.temperature = \
                self.process.recipe.boiling_temperature
            self.warm_must()
        elif state == STATES.get('add_hops'):
            logger.info("[Boiling] Function defined: add_hops")
            self.add_hops()
        elif state == STATES.get('continue_boiling'):
            logger.info("[Boiling] Function defined: continue_boiling")
            self.continue_boiling()

    def warm_must(self):
        temperature = ThermalSensor.get_current_temperature_in('pot2')
        if temperature < self.process.actual_heat.temperature:
            logger.info("[Boiling] Temperature less than actual "
                        "heat temperature")
            self.process.state = STATES.get('warm_must')
            # Increase temperature
            pass
        else:
            logger.info("[Boiling] Temperature reached!")
            self.process.actual_hop_time = timezone.now()
            self.process.actual_heat_time = timezone.now()
            self.process.state = STATES.get('add_hops')
            self.process.boiling_stop_time = timezone.now() + \
                timedelta(minutes=self.process.recipe.boiling_duration)
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
                self.process.state = STATES.get('continue_boiling')
                logger.info("[Boiling] State changed! "
                            "New state: continue_boiling")
        else:
            # No more hops to add
            pass
        self.process.save()

    def continue_boiling(self):
        if self.check_boiling_time_reached():
            logger.info("[Boiling] Boiling stage completed!"
                        "New state: turn_on_chiller")
            self.process.state = cooling.STATES.get('turn_on_chiller')

    def check_next(self):
        if self.process.next_hop <= len(self.hop_order):
            return True
        else:
            return False

    def get_next_hop(self):
        next_hop = self.process.next_hop
        return self.hop_order.get(str(next_hop))

    def check_boiling_time_reached(self):
        now = timezone.now()

        if now >= self.process.boiling_stop_time:
            return True
        else:
            return False
