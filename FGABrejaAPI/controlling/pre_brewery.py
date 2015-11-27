from monitoring.models import LevelSensor

STATES = {'check_level': 1,
          'notify_user': 2,
          }


class BreweryControll(object):

    def __init__(self, process):
        self.process = process

    def check_level(self):
        level = LevelSensor.get_current_level_in('panela1')
        if level:
            self.process.state = STATES.get('notify_user')
            self.process.save()
            pass

    def notify_user(self):
        self.process.level_pot1 = True
