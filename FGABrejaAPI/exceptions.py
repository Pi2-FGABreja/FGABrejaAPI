from flask import Response
from FGABrejaAPI.serializer import Serializer


class SensorNotFound(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)

    def get_json_response(self):
        error_json = Serializer.serialize_error(404, self.message)
        return Response(response=error_json, status=404,
                        mimetype="application/json")
