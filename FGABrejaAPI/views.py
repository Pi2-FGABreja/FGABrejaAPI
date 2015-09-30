from flask.views import MethodView
from flask import Response
from FGABrejaAPI.serializer import Serializer
from FGABrejaAPI.models import ThermalSensor
from FGABrejaAPI.exceptions import SensorNotFound


class SensorsView(MethodView):

    def get(self, sensor_id):
        if sensor_id:
            response = self.get_sensor_response(sensor_id)
        else:
            response = self.get_all_sensors_response()
        return response

    def get_sensor_response(self, sensor_id):
        try:
            sensors = [ThermalSensor(sensor_id)]
            json_data = Serializer.serialize(sensors)
            response = Response(response=json_data, status=200,
                                mimetype="application/json")
        except SensorNotFound as error:
            response = error.get_json_response()

        return response

    def get_all_sensors_response(self):
        json_data = Serializer.serialize(ThermalSensor.all())
        return Response(response=json_data, status=200,
                        mimetype="application/json")
