from django.http import HttpResponse
from controlling.comunication import Comunication
from controlling.models import Process, Recipe
from controlling.stages import brewery, filtering
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


@csrf_exempt
def create_process(request):
    actual_process = Process.current()
    if actual_process is not None:
        actual_process.is_active = False
        actual_process.save()

    recipe_id = request.POST.get('recipe_id')
    process = Process()
    process.recipe = Recipe.objects.get(pk=recipe_id)
    process.save()
    return HttpResponse('OK')


def insert_malt(request):
    process = Process.current()
    process.malt = True
    process.state = brewery.STATES.get('heating')
    process.save()

    comunication = Comunication()
    comunication.turn_on_engine()
    return HttpResponse('OK')


def iodine_test(request):
    process = Process.current()
    process.iodine_test = True
    process.state = filtering.STATES.get('open_pot_valve')
    process.save()

    comunication = Comunication()
    comunication.turn_off_engine()
    comunication.turn_off_resistor(1)
    return HttpResponse('OK')
