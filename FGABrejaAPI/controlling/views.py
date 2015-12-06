from django.http import HttpResponse
from controlling.models import Process
import json

# Create your views here.


def create_process(request):
    print('oioioioioioi')
    process = Process()
    process.recipe_id = request.POST.get('recipe_id')
    process.state = 1
    process.save()
    data = json.dumps(process.__dict__)
    return HttpResponse(data, content_type='application/json')
