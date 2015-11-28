from django.test import TestCase
from controlling.models import Process
from controlling.pre_brewery import PreBreweryControll


class TestPreBreweryControll(TestCase):

    data = b'[{"value": true, "position": "", "sensor_type": "level", '\
           b'"location": "panela1"}]'

    def setUp(self):
        self.process = Process()
        self.pre_brewery = PreBreweryControll('panela1')

    def test_check_level(self):
        self.assertEquals(self.pre_brewery.check_level(), True)
