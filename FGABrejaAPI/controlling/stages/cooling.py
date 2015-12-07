from monitoring.models import ThermalSensor
from controlling.stages import fermentation
from controlling.stages.serial_calls import SerialCalls
import logging

logger = logging.getLogger('fga-breja')

STATES = {'turn_on_chiller': 16,
          'check_temperature': 17}


class CoolingControll(object):

    def __init__(self, process):
        self.process = process
        self.serial_comunication = SerialCalls()

    def handle_states(self):
        state = self.process.state
        if state == STATES.get('turn_on_chiller'):
            logger.info("[Cooling] Function defined: turn_on_chiller")
            self.turn_on_chiller()
        elif state == STATES.get('check_temperature'):
            logger.info("[Cooling] Function defined: check_temperature")
            self.check_temperature()

    def turn_on_chiller(self):
        self.serial_comunication.turn_on_chiller()
        logger.info('[Cooling] Turning on water on chiller')
        self.process.state = STATES.get('check_temperature')
        self.process.save()
        logger.info("[Cooling] State changed! New state: check_temperature")

    def check_temperature(self):
        temperature = ThermalSensor.get_current_temperature()
        logger.info("[Cooling] Temperature: %.2f" % temperature)
        if temperature < 2:
            logger.info("[Cooling] Temperature is lower than 20 degrees")
            self.serial_comunication.turn_off_chiller()
            logger.info("[Cooling] Turning off water on chiller")
            self.process.state = fermentation.STATES.get('chill_must')
            self.process.save()
            logger.info("[Cooling] Cooling stage completed! "
                        "New state: chill_must")
