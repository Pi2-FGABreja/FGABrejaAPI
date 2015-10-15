from unittest import TestCase
from FGABrejaAPI.serializer import Serializer
from FGABrejaAPI.models import ThermalSensor
from mock import patch


class TestSerializer(TestCase):

    load_yaml_data = {'sensor1': {'location': [1, 'first_pot'],
                                  'position': [1, 'lower'],
                                  'type': [1, 'themal']}, }

    @patch.object(ThermalSensor, 'load_yaml')
    def setUp(self, mock):
        mock.return_value = self.load_yaml_data
        self.obj_list = [ThermalSensor(1)]

    def test_serialize(self):
        serialized = Serializer.serialize(self.obj_list)
        self.assertEqual(len(serialized),
                         len('[{"id": 1, "type": [1, "themal"], '
                             '"location": [1, "first_pot"], '
                             '"position": [1, "lower"]}]'))
