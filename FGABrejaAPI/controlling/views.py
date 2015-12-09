from django.http import HttpResponse
from controlling.models import Process, Recipe
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


@csrf_exempt
def create_process(request):
    recipe_id = request.POST.get('recipe_id')
    process = Process()
    process.recipe = Recipe.objects.get(pk=recipe_id)
    process.save()
    return HttpResponse('OK')
