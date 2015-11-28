from monitoring.models import LevelSensor
from controlling.models import Valve
from controlling import brewery

STATES = {'insert_water': 1,
          'check_level': 2,
          'stop_water': 3
          }


class PreBreweryControll(object):

    def __init__(self, process):
        self.process = process
        self.valve = Valve.objects.get(pk=1)

    def insert_water(self):
        print("Opening valve to insert water. . .")
        self.valve = Valve.objects.get(pk=1)
        self.valve.is_opened = 1
        print("Valve is opened, moving to next state.")
        self.process.state = STATES.get('check_level')
        self.process.save()

    def check_level(self):
        print("Checking level of pot1. . .")
        level = LevelSensor.get_current_water_level_in('panela1')

        if level:
            print("Pot water level reached. Moving no next state.")
            self.process.state = STATES.get('stop_water')
            self.process.save()
            pass
        else:
            print("Pot water level not reached.")
            self.process.state = STATES.get('check_level')
            self.process.save()
            pass

    def stop_water(self):
        print("Closing water valve. . .")
        self.valve.is_opened = 0
        print("Valve is colsed, finishing pre brewery flow")
        self.process.state = brewery.STATES.get('initial_boiling')
        self.process.save()
