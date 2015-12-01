from monitoring.models import ThermalSensor
import logging

logger = logging.getLogger('fga-breja')

STATES = {'chill_must': 1,
          'maintain_temperature': 2,
          'verify_airlock': 3
          }


class FermentationsControll(object):

    def __init__(self, process):
        self.process = process
        self.freezer_temperature = self.process.recipe.fermentation_temperature

    def handle_states(self):
        state = self.process.state
        if state == STATES.get('chill_must'):
            logger.info("[Fermentation] Function defined: chill_must")
            self.turn_on_chiller()
        elif state == STATES.get('maintain_temperature'):
            logger.info("[Fermentation] Function defined: "
                        "maintain_temperature")
            self.maintain_temperature()

    def chill_must(self):
        logger.info('[Fermentation] Cooling must on the freezer')
        temperature = ThermalSensor.get_current_temperature_in('pot3')
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
        temperature = ThermalSensor.get_current_temperature_in('pot3')
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

    #def verify_airlock(self):

