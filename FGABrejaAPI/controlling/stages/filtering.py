from monitoring.models import LevelSensor
from controlling.stages import boiling
from controlling.comunication import Comunication
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger('fga-breja')

STATES = {'open_pot_valve': 9,
          'insert_water': 10,
          'check_level': 11,
          'stop_water': 12}


class FilteringControll(object):

    def __init__(self, process):
        self.process = process
        self.serial_comunication = Comunication()
        self.serial_comunication.turn_off_resistor(1)

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
        self.serial_comunication.activate_alarm()
        now = timezone.now()
        minutes = timedelta(minutes=1)
        if now > self.process.filtering_init + minutes:
            logger.info("[Filtering] 20 minutes after filtering init")
            self.serial_comunication.activate_alarm()
            self.process.state = STATES.get('insert_water')
            self.process.save()
            logger.info("[Filtering] State changed! New state: insert_water")

    def insert_water(self):
        self.serial_comunication.insert_water()
        logger.info("[Filtering] Turn on the water")
        self.process.state = STATES.get('check_level')
        self.process.save()
        logger.info("[Filtering] State changed! New state: check_level")

    def check_level(self):
        logger.info("[Filtering] Checking level of pot2. . .")
        level = LevelSensor.get_current_water_level()

        if level:
            logger.info("[Filtering] Pot water level reached")
            self.process.state = STATES.get('stop_water')
            self.process.save()
            logger.info("[Filtering] State changed! New state: stop_water")
        else:
            logger.info("[Filtering] Pot water level not reached")

    def stop_water(self):
        self.serial_comunication.stop_water()
        logger.info("[Filtering] Closing valve")
        self.process.state = boiling.STATES.get('warm_must')
        self.process.save()
        logger.info("[Filtering] State changed! New state: warm_must "
                    "(from boiling process)")
