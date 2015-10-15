from unittest import TestCase
from FGABrejaAPI.exceptions import SensorNotFound


class TestSensorNotFound(TestCase):

    def setUp(self):
        self.not_found = SensorNotFound('SensorNotFound')

    def test_intance(self):
        self.assertEqual(self.not_found.message, 'SensorNotFound')

    def test_str(self):
        self.assertEqual(self.not_found.__str__(), repr('SensorNotFound'))

    def test_json_response(self):
        response = self.not_found.get_json_response()
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.data, b'{"404": "SensorNotFound"}')
