from django.conf.urls import url

from rest_framework import routers
from .views import (RecipeDetailViewSet,
                    ShoppingListViewSet,
                    PlanViewSet,
                    LatestPlanView)


router = routers.DefaultRouter()
router.register(r'recipes', RecipeDetailViewSet)
router.register(r'shopping', ShoppingListViewSet, base_name='shopping')
router.register(r'plan', PlanViewSet, base_name='plan')


urlpatterns = [
    url(r'plan/latest/$', LatestPlanView.as_view({ 'get': 'latest' }), name='plan_latest'),
]

urlpatterns += router.urls
