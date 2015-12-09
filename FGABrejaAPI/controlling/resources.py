from tastypie.resources import ModelResource
from controlling.models import Recipe, Process
from tastypie.authorization import Authorization
from tastypie.constants import ALL
from tastypie import fields


class RecipeResource(ModelResource):
    class Meta:
        queryset = Recipe.objects.all()
        allowed_methods = ['get']


class ProcessResource(ModelResource):
    recipe = fields.ForeignKey(RecipeResource,
                               'recipe', null=True, full=True)

    class Meta:
        queryset = Process.objects.all()
        allowed_methods = ['get', 'post']
        filtering = {'is_active': ALL}
        authorization = Authorization()
