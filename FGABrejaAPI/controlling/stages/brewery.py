from controlling.models import Heat
from controlling.comunication import Comunication
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
        self.serial_comunication = Comunication()

    def handle_states(self):
        state = self.process.state
        if state == STATES.get('initial_boiling'):
            logger.info("[Brewery] Function defined: initial_boiling")
            self.initial_boiling()
        elif state == STATES.get('heating'):
            logger.info("[Brewery] Function defined: heating")
            self.heating()
        elif state == STATES.get('heat_controll'):
            logger.info("[Brewery] Function defined: heat_controll")
            self.heat_controll()

    def initial_boiling(self):
        # engine_is_on = self.serial_comunication.get_engine_state()
        boiling_temperature = self.process.recipe.initial_boiling_temperature

        # while engine_is_on != "True":
        #     self.serial_comunication.turn_on_engine()
        print("TURN ON RESISTOR")
        self.serial_comunication.turn_on_resistor(boiling_temperature)
        print("READ THERMAL SENSOR")
        temperature = self.serial_comunication.read_thermal_sensor()

        if temperature < boiling_temperature:
            logger.info("[Brewery] Actual temperature is lower "
                        "than %.2f" % boiling_temperature)
            # Increase heat
            pass
        else:
            logger.info("[Brewery] Actual temperature is greater "
                        "than %.2f" % boiling_temperature)
            # Maintain temperature
            self.process.state = STATES.get('insert_malt')
            print("ACTIVATE ALARM")
            self.serial_comunication.activate_alarm()
            logger.info("[Brewery] State changed! New state: insert_malt")
        self.process.save()

    def heating(self):
        print("READ THERMAL SENSOR")
        temperature = self.serial_comunication.read_thermal_sensor()
        if temperature < self.process.actual_heat.temperature:
            logger.info("[Brewery] Temperature less than actual "
                        "heat temperature")
            # Increase temperature
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
                print("ACITVATE ALARM")
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
