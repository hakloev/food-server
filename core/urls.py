from rest_framework import routers
from .views import RecipeDetailViewSet, ShoppingListViewSet, PlanViewSet

router = routers.DefaultRouter()
router.register(r'recipes', RecipeDetailViewSet)
router.register(r'shopping', ShoppingListViewSet, base_name='shopping')
router.register(r'plan', PlanViewSet, base_name='plan')

urlpatterns = router.urls
