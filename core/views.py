from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Recipe, RecipeIngredient
from .serializers import RecipeSerializer, RecipeDetailSerializer, ShoppingListSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class RecipeDetailViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeDetailSerializer


class ShoppingListViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = RecipeIngredient.objects.values('ingredient').annotate(
            total_amount=Sum('amount')
        )
        serializer = ShoppingListSerializer(queryset, many=True)
        return Response(serializer.data)
