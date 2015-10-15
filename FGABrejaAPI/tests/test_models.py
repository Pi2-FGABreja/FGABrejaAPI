from unittest import TestCase
from FGABrejaAPI.models import Sensor, ThermalSensor
from FGABrejaAPI.exceptions import SensorNotFound
from mock import patch


class TestSensor(TestCase):

    def test_get_data(self):
        sensor = Sensor()
        with self.assertRaises(NotImplementedError):
            sensor.get_data()


class TestThermalSensor(TestCase):

    load_yaml_data = {'sensor1': {'location': [1, 'first_pot'],
                                  'position': [1, 'lower'],
                                  'type': [1, 'themal']}, }

    open_yaml_data = '''sensor1:
    type:
        - 1
        - themal
    location:
        - 1
        - first_pot
    position:
        - 1
        - lower'''

    @patch.object(ThermalSensor, 'load_yaml')
    def test_initial_instance(self, mock):
        mock.return_value = self.load_yaml_data
        sensor = ThermalSensor(1)
        self.assertEqual(sensor.type, [1, 'themal'])
        self.assertEqual(sensor.position, [1, 'lower'])
        self.assertEqual(sensor.location, [1, 'first_pot'])

    @patch.object(ThermalSensor, 'load_yaml')
    def test_sensor_not_found(self, mock):
        mock.return_value = self.load_yaml_data

        with self.assertRaises(SensorNotFound):
            ThermalSensor(2)

    @patch.object(ThermalSensor, 'open_yaml')
    def test_load_yaml(self, mock):
        mock.return_value = self.open_yaml_data

        self.assertEqual(ThermalSensor.load_yaml(), self.load_yaml_data)

    @patch.object(ThermalSensor, 'load_yaml')
    def test_all(self, mock):
        mock.return_value = self.load_yaml_data

        self.assertEqual(len(ThermalSensor.all()), 1)
