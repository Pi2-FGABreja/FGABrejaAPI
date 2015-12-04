from controlling.comunication import Comunication
import logging

logger = logging.getLogger('fga-breja')

STATES = {'turn_on_chiller': 16,
          'check_temperature': 17}


class CoolingControll(object):

    def __init__(self, process):
        self.process = process
        self.serial_comunication = Comunication()

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
        temperature = self.serial_comunication.read_thermal_sensor()
        if temperature < 20.0:
            logger.info("[Cooling] Temperature is lower than 20 degrees")
            self.serial_comunication.turn_off_chiller()
            logger.info("[Cooling] Turning off water on chiller")
            self.process.state = STATES.get('check_temperature')
            self.process.save()
            logger.info("[Cooling] State changed! New state: ---")
