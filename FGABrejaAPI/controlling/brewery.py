from monitoring.models import ThermalSensor
from controlling.models import Heat
from datetime import datetime

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
        self.next_heat = '2'

    def initial_boiling(self):
        temperature = ThermalSensor.get_current_temperature_in('panela1')
        if temperature < 80:
            # Increase heat
            pass
        else:
            # Maintain temperature
            self.process.state = STATES.get('insert_malt')
        self.process.save()

    def heating(self):
        temperature = ThermalSensor.get_current_temperature_in('panela1')
        if temperature < self.process.actual_heat.temperature:
            # Increase temperature
            pass
        else:
            self.process.actual_heat_time = datetime.now()
            self.process.state = STATES.get('heat_controll')
        self.process.save()

    def heat_controll(self):
        if self.process.change_heat():
            if self.check_next():
                heat = Heat.objects.get(pk=self.get_next_heat())
                self.process.actual_heat = heat
                self.process.state = STATES.get('heating')
            else:
                self.process.state = STATES.get('iodine_test')
        else:
            # Maintain temperature
            pass
        self.process.save()

    def check_next(self):
        try:
            self.heat_order.get(self.next_heat)
            return True
        except:
            return False

    def get_next_heat(self):
        return self.heat_order.get(self.next_heat)
