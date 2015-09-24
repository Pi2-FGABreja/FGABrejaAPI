import abc
import yaml
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class Sensor(object):

    @abc.abstractmethod
    def get_data(self):
        raise NotImplementedError()


class ThermalSensor(Sensor):

    def __init__(self, sensor_id):
        self.id = sensor_id

        sensor_data = self.load_data()
        self.type = sensor_data.get('type')
        self.location = sensor_data.get('location')
        self.position = sensor_data.get('position')

    def load_data(self):
        yaml_file = os.path.join(BASE_DIR, 'sensors.yml')
        yaml_file = open(yaml_file)
        sensors_dict = yaml.load(yaml_file.read())
        return sensors_dict.get('sensor{}'.format(self.id))
