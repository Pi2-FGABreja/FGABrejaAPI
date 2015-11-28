from monitoring.models import ThermalSensor
from controlling.models import Heat
from django.utils import timezone

STATES = {'initial_boiling': 1,
          'insert_malt': 2,
          'heating': 3,
          'heat_controll': 4,
          'iodine_test': 5}


class BreweryControll(object):

    def __init__(self, process):
        self.heat_order = process.recipe.get_heat_order()
        process.actual_heat = Heat.objects.get(pk=self.heat_order.get('1'))
        process.save()
        self.process = process

    def define_step(self):
        state = self.process.state
        if state == STATES.get('initial_boiling'):
            print("Step defined: initial_boiling")
            self.initial_boiling()
        elif state == STATES.get('heating'):
            print("Step defined: heating")
            self.heating()
        elif state == STATES.get('heat_controll'):
            print("Step defined: heat_controll")
            self.heat_controll()

    def initial_boiling(self):
        print("Initial Boiling")
        temperature = ThermalSensor.get_current_temperature_in('panela1')
        if temperature < 65:
            print("Temperature less than 65 degrees")
            # Increase heat
            pass
        else:
            print("Temperature greater than 65 degrees")
            # Maintain temperature
            self.process.state = STATES.get('insert_malt')
            print("Change state: insert_malt")
        self.process.save()

    def heating(self):
        print("Heating")
        temperature = ThermalSensor.get_current_temperature_in('panela1')
        if temperature < self.process.actual_heat.temperature:
            print("Temperature less than actual_heat temperature")
            # Increase temperature
            pass
        else:
            print("Temperature greater than actual_heat temperature")
            self.process.actual_heat_time = timezone.now()
            self.process.state = STATES.get('heat_controll')
            print("Change state: heat_controll")
        self.process.save()

    def heat_controll(self):
        print('Heat controll')
        if self.process.change_heat():
            print('Change heat')
            if self.check_next():
                print("Next exists")
                print(self.get_next_heat())
                heat = Heat.objects.get(pk=self.get_next_heat())
                self.process.next_heat += 1
                self.process.actual_heat = heat
                self.process.state = STATES.get('heating')
                print("Change state: heating")
            else:
                print("Without next")
                self.process.state = STATES.get('iodine_test')
                print("Change state: iodine_test")
        else:
            print('Maintain temperature')
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
