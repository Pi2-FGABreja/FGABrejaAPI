from monitoring.models import ThermalSensor

STATES = {'initial_boiling': 1,
          'insert_malt': 2,
          'heating': 3,
          'heat_controll': 4,
          'iodine_test': 5}


class BreweryControll(object):

    def __init__(self, process):
        self.process = process

    def initial_boiling(self):
        temperature = ThermalSensor.get_current_temperature_in('panela1')
        if temperature < 80:
            # Increase heat
            pass
        else:
            self.process.state = STATES.get('insert_malt')
            self.process.save()

    def insert_malt(self):
        pass

    def heating(self):
        pass

    def heat_controll(self):
        pass

    def iodine_test(self):
        pass
