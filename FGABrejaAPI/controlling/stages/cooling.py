from monitoring.models import ThermalSensor
import logging

logger = logging.getLogger('fga-breja')

STATES = {'turn_on_chiller': 1,
          'check_temperature': 2}


class CoolingControll(object):

    def __init__(self, process):
        self.process = process

    def handle_states(self):
        state = self.process.state
        if state == STATES.get('turn_on_chiller'):
            logger.info("[Cooling] Function defined: turn_on_chiller")
            self.turn_on_chiller()
        elif state == STATES.get('check_temperature'):
            logger.info("[Cooling] Function defined: check_temperature")
            self.check_temperature()

    def turn_on_chiller(self):
        logger.info('[Cooling] Turning on water on chiller')
        self.process.state = STATES.get('check_temperature')
        self.process.save()
        logger.info("[Cooling] State changed! New state: check_temperature")

    def check_temperature(self):
        temperature = ThermalSensor.get_current_temperature_in('pot2')
        if temperature < 20.0:
            logger.info("[Cooling] Temperature is lower than 20 degrees")
            logger.info("[Cooling] Turning off water on chiller")
            self.process.state = STATES.get('check_temperature')
            self.process.save()
            logger.info("[Cooling] State changed! New state: ---")
