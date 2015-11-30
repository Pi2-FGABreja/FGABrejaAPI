from monitoring.models import LevelSensor
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger('fga-breja')

STATES = {'open_pot_valve': 1,
          'insert_water': 2,
          'check_level': 3,
          'stop_water': 4}


class FilteringControll(object):

    def __init__(self, process):
        self.process = process

    def handle_states(self):
        state = self.process.state
        if state == STATES.get('open_pot_valve'):
            logger.info("[Filtering] Function defined: open_pot_valve")
            self.open_pot_valve()
        elif state == STATES.get('insert_water'):
            logger.info("[Filtering] Function defined: insert_water")
            self.insert_water()
        elif state == STATES.get('check_level'):
            logger.info("[Filtering] Function defined: check_level")
            self.check_level()
        elif state == STATES.get('stop_water'):
            logger.info("[Filtering] Function defined: stop_water")
            self.stop_water()

    def open_pot_valve(self):
        now = timezone.now()
        minutes = timedelta(minutes=1)
        if now > self.process.filtering_init + minutes:
            logger.info("[Filtering] 20 minutes after filtering init")
            self.process.state = STATES.get('insert_water')
            self.process.save()
            logger.info("[Filtering] State changed! New state: insert_water")

    def insert_water(self):
        logger.info("[Filtering] Turn on the water")
        self.process.state = STATES.get('check_level')
        self.process.save()
        logger.info("[Filtering] State changed! New state: check_level")

    def check_level(self):
        logger.info("[Filtering] Checking level of pot2. . .")
        level = LevelSensor.get_current_water_level_in('pot2')

        if level:
            logger.info("[Filtering] Pot water level reached")
            self.process.state = STATES.get('stop_water')
            self.process.save()
            logger.info("[Filtering] State changed! New state: stop_water")
        else:
            logger.info("[Filtering] Pot water level not reached")

    def stop_water(self):
        logger.info("[Filtering] Closing valve")
        logger.info("[Filtering] State changed! New state: ---")
