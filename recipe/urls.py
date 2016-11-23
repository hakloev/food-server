from django.conf.urls import url

from rest_framework import routers
from .views import RecipeDetailViewSet, ShoppingListViewSet, PlanViewSet, RecipeCreateView, RecipeEditView, RecipeDetailView


router = routers.DefaultRouter()
router.register(r'recipes', RecipeDetailViewSet)
router.register(r'shopping', ShoppingListViewSet, base_name='shopping')
router.register(r'plan', PlanViewSet, base_name='plan')


urlpatterns = [
    url(r'^create/$', RecipeCreateView.as_view(), name='recipe_create'),
    url(r'^edit/(?P<pk>[0-9]+)/$', RecipeEditView.as_view(), name='recipe_edit'),
    url(r'^detail/(?P<pk>[0-9]+)/$', RecipeDetailView.as_view(), name='recipe_detail'),
    # url(r'^api/$', router.urls(), name='api'),
]
