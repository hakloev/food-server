from django.conf.urls import url

from rest_framework import routers
from .views import (# ShoppingListViewSet,
                    # PlanViewSet,
                    IngredientViewSet,
                    RecipeList,
                    RecipeDetail,
                    RecipeStepList,
                    RecipeStepDetail,
                    RecipeIngredientList,
                    RecipeIngredientDetail,
                    PlanList,
                    PlanDetail,
                    PlanItemList,
                    PlanItemDetail,
                    LatestPlanView)


router = routers.DefaultRouter()
router.register(r'ingredients', IngredientViewSet)
# router.register(r'shopping', ShoppingListViewSet, base_name='shopping')
# router.register(r'plan', PlanViewSet, base_name='plan')


urlpatterns = [

    url(r'recipes/$', RecipeList.as_view()),
    url(r'recipes/(?P<pk>[0-9]+)/$', RecipeDetail.as_view()),

    url(r'recipes/(?P<pk>[0-9]+)/steps/$', RecipeStepList.as_view()),
    url(r'recipes/(?P<pk>[0-9]+)/steps/(?P<step_number>[0-9]+)/$', RecipeStepDetail.as_view()),

    url(r'^recipes/(?P<pk>[0-9]+)/ingredients/$', RecipeIngredientList.as_view()),
    url(r'^recipes/(?P<pk>[0-9]+)/ingredients/(?P<ingredient_pk>[0-9]+)/$', RecipeIngredientDetail.as_view()),

    url(r'^plans/$', PlanList.as_view()),
    url(r'^plans/(?P<pk>[0-9]+)/$', PlanDetail.as_view()),

    url(r'^plans/(?P<plan_pk>[0-9]+)/items/$', PlanItemList.as_view()),
    url(r'^plans/(?P<plan_pk>[0-9]+)/items/(?P<item_pk>[0-9]+)', PlanItemDetail.as_view()),

    url(r'plan/latest/$', LatestPlanView.as_view({ 'get': 'latest' }), name='plan_latest'),
]

urlpatterns += router.urls
