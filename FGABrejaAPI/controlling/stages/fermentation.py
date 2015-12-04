from monitoring.models import LdrSensor
from controlling.comunication import Comunication
import logging

logger = logging.getLogger('fga-breja')

STATES = {'chill_must': 18,
          'maintain_temperature': 19,
          'verify_airlock': 20,
          'process_end': 21}


class FermentationControll(object):

    def __init__(self, process):
        self.process = process
        self.freezer_temperature = self.process.recipe.fermentation_temperature
        self.serial_comunication = Comunication()

    def handle_states(self):
        state = self.process.state
        if state == STATES.get('chill_must'):
            logger.info("[Fermentation] Function defined: chill_must")
            self.chill_must()
        elif state == STATES.get('maintain_temperature'):
            logger.info("[Fermentation] Function defined: "
                        "maintain_temperature")
            self.maintain_temperature()
        elif state == STATES.get('verify_airlock'):
            logger.info("[Fermentation] Function defined: verify_airlock")
            self.verify_airlock()

    def chill_must(self):
        self.serial_comunication.turn_on_freezer(self.freezer_temperature)
        logger.info('[Fermentation] Cooling must on the freezer')
        temperature = self.serial_comunication.read_thermal_sensor()
        if temperature > self.freezer_temperature:
            logger.info("[Fermentation] Fermentation temperature not reached")
            self.process.state = STATES.get('chill_must')
            # Decrease temperature
            pass
        else:
            logger.info("[Fermentation] Temperature reached!")
            self.process.state = STATES.get('maintain_temperature')
            logger.info("[Fermentation] State changed! "
                        "New state: maintain_temperature")
        self.process.save()

    def maintain_temperature(self):
        temperature = self.serial_comunication.read_thermal_sensor()
        if self.freezer_temperature - 2 <= temperature \
                <= self.freezer_temperature + 2:
            logger.info("[Fermentation] Temperature on range")
            self.process.state = STATES.get('verify_airlock')
            logger.info("[Fermentation] State changed! "
                        "New state: verify_airlock")
        else:
            logger.info("[Fermentation] Temperature not on range")
            self.process.state = STATES.get('chill_must')
            pass
        self.process.save()

    def verify_airlock(self):
        has_boubles = LdrSensor.get_read_from_airlock('pot3')
        if has_boubles:
            logger.info("[Fermentation] No more boubles, "
                        "fermentation is done!")
            self.serial_comunication.activate_alarm()
            self.process.state = STATES.get("process_end")
        else:
            logger.info("[Fermentation] Airlock has boubles "
                        "fermentation still in process")
            self.process.state = STATES.get('maintain_temperature')
            pass
        self.process.save()
