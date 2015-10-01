import json


class Serializer(object):

    @classmethod
    def serialize(cls, obj_list):
        json_list = []
        for obj in obj_list:
            obj_attrs = obj.__dict__
            obj_dict = {}
            for attr in obj_attrs.keys():
                obj_dict[attr] = obj_attrs.get(attr)

            json_list.append(obj_dict)

        return json.dumps(json_list)

    @classmethod
    def serialize_error(cls, error_code, error_message):
        error_dict = {}
        error_dict[error_code] = error_message
        print(error_dict)
        return json.dumps(error_dict)
