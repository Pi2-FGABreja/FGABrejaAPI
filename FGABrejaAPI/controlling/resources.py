from tastypie.resources import ModelResource
from controlling.models import Recipe, Process
from tastypie.authorization import Authorization
from tastypie.constants import ALL


class RecipeResource(ModelResource):
    class Meta:
        queryset = Recipe.objects.all()
        allowed_methods = ['get']


class ProcessResource(ModelResource):
    class Meta:
        queryset = Process.objects.all()
        allowed_methods = ['get', 'post']
        filtering = {'is_active': ALL}
