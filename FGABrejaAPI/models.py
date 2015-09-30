import abc
import os

from FGABrejaAPI.exceptions import SensorNotFound
import yaml


BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class Sensor(object):

    @abc.abstractmethod
    def get_data(self):
        raise NotImplementedError()


class ThermalSensor(Sensor):

    def __init__(self, sensor_id):
        self.id = sensor_id

        sensor_data = self.load_initial_data()
        try:
            self.type = sensor_data.get('type')
            self.location = sensor_data.get('location')
            self.position = sensor_data.get('position')
        except AttributeError:
            raise SensorNotFound('Sensor {} does '
                                 'not exist.'.format(self.id))

    def load_initial_data(self):
        sensors_dict = self.load_yaml(self.open_yaml())
        return sensors_dict.get('sensor{}'.format(self.id))

    @classmethod
    def load_yaml(cls, yaml_file):
        return yaml.load(yaml_file.read())

    @classmethod
    def open_yaml(cls):
        yaml_file = os.path.join(BASE_DIR, 'sensors.yml')
        return open(yaml_file)

    @classmethod
    def all(cls):
        sensors_dict = cls.load_yaml(cls.open_yaml())
        sensors_list = []

        for sensor in sensors_dict:
            sensor = cls(int(sensor.replace('sensor', '')))
            sensors_list.append(sensor)

        return sensors_list
