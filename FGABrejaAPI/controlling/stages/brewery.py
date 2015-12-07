from monitoring.models import ThermalSensor
from controlling.models import Heat
from controlling.stages.serial_calls import SerialCalls
from django.utils import timezone
import logging

logger = logging.getLogger('fga-breja')


STATES = {'initial_boiling': 4,
          'insert_malt': 5,
          'heating': 6,
          'heat_controll': 7,
          'iodine_test': 8}


class BreweryControll(object):

    def __init__(self, process):
        self.heat_order = process.recipe.get_heat_order()
        process.actual_heat = Heat.objects.get(pk=self.heat_order.get('1'))
        process.save()
        self.process = process
        self.next_heat = '2'
        self.serial_comunication = SerialCalls()

    def handle_states(self):
        state = self.process.state
        if state == STATES.get('initial_boiling'):
            logger.info("[Brewery] Function defined: initial_boiling")
            self.initial_boiling()
        elif state == STATES.get('heating'):
            logger.info("[Brewery] Function defined: heating")
            print("TURN ON ENGINE")
            self.serial_comunication.turn_on_engine()
            self.heating()
        elif state == STATES.get('heat_controll'):
            logger.info("[Brewery] Function defined: heat_controll")
            self.heat_controll()

    def initial_boiling(self):
        boiling_temperature = self.process.recipe.initial_boiling_temperature

        self.serial_comunication.turn_on_resistor(boiling_temperature)
        temperature = ThermalSensor.get_current_temperature()

        if temperature < boiling_temperature:
            logger.info("[Brewery] Actual temperature is lower "
                        "than %.2f" % boiling_temperature)
            self.serial_comunication.turn_on_resistor(boiling_temperature)
            pass
        else:
            logger.info("[Brewery] Actual temperature is greater "
                        "than %.2f" % boiling_temperature)
            self.serial_comunication.turn_on_resistor(boiling_temperature)
            self.process.state = STATES.get('insert_malt')
            self.serial_comunication.activate_alarm()
            logger.info("[Brewery] State changed! New state: insert_malt")
        self.process.save()

    def heating(self):
        print("READ THERMAL SENSOR")
        temperature = ThermalSensor.get_current_temperature()
        if temperature < self.process.actual_heat.temperature:
            logger.info("[Brewery] Temperature less than actual "
                        "heat temperature")
            self.serial_comunication.turn_on_resistor(
                self.process.actual_heat.temperature)
            pass
        else:
            logger.info("[Brewery] Temperature greater than "
                        "actual_heat temperature")
            self.process.actual_heat_time = timezone.now()
            self.process.state = STATES.get('heat_controll')
            logger.info("[Brewery] State changed! New state: heat_controll")
        self.process.save()

    def heat_controll(self):
        if self.process.change_heat():
            logger.info('[Brewery] Previous heating is done. Change heat!')
            if self.check_next():
                heat = Heat.objects.get(pk=self.get_next_heat())
                self.process.next_heat += 1
                self.process.actual_heat = heat
                self.process.state = STATES.get('heating')
                logger.info("[Brewery] State changed! New state: heating")
            else:
                self.process.state = STATES.get('iodine_test')
                self.serial_comunication.activate_alarm()
                logger.info("[Brewery] State changed! New state: iodine_test")
        else:
            # Maintain temperature
            pass
        self.process.save()

    def check_next(self):
        if self.process.next_heat <= len(self.heat_order):
            return True
        else:
            return False

    def get_next_heat(self):
        next_heat = self.process.next_heat
        return self.heat_order.get(str(next_heat))
