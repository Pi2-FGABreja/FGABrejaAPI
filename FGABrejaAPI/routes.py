from FGABrejaAPI import app
from FGABrejaAPI.views import SensorsView

sensors_view = SensorsView.as_view('sensors_view')
app.add_url_rule('/sensors/', defaults={'sensor_id': None},
                 view_func=sensors_view, methods=['GET', ])
app.add_url_rule('/sensors/<int:sensor_id>/',
                 view_func=sensors_view, methods=['GET', ])
