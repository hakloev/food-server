from rest_framework import routers
from .views import RecipeDetailViewSet, ShoppingListViewSet

router = routers.DefaultRouter()
router.register(r'recipes', RecipeDetailViewSet)
router.register(r'shopping', ShoppingListViewSet, base_name='shopping')

urlpatterns = router.urls