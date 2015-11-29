from monitoring.models import LevelSensor
from controlling.models import Valve
from controlling.stages import brewery
import logging

logger = logging.getLogger('fga-breja')

STATES = {'insert_water': 1,
          'check_level': 2,
          'stop_water': 3
          }


class PreBreweryControll(object):

    def __init__(self, process):
        self.process = process
        self.valve = Valve.objects.get(pk=1)

    def insert_water(self):
        logger.info("[PreBrewery] Opening valve")
        self.valve = Valve.objects.get(pk=1)
        self.valve.is_opened = 1
        self.process.state = STATES.get('check_level')
        self.process.save()
        logger.info("[PreBrewery] State changed! New state: check_level")

    def check_level(self):
        logger.info("[PreBrewery] Checking level of pot1. . .")
        level = LevelSensor.get_current_water_level_in('panela1')

        if level:
            logger.info("[PreBrewery] Pot water level reached")
            self.process.state = STATES.get('stop_water')
            self.process.save()
            logger.info("[PreBrewery] State changed! New state: stop_water")
        else:
            logger.info("[PreBrewery] Pot water level not reached")
            self.process.state = STATES.get('check_level')
            self.process.save()

    def stop_water(self):
        logger.info("[PreBrewery] Closing water valve")
        self.valve.is_opened = 0
        self.process.state = brewery.STATES.get('initial_boiling')
        self.process.save()
        logger.info("[PreBrewery] State changed! New state: "
                    "initial_boiling (from brewery process)")
