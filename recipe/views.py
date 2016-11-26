from django.db.models import Sum

from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Recipe, RecipeIngredient, Plan
from .serializers import (RecipeSerializer,
                          RecipeDetailSerializer,
                          ShoppingListSerializer,
                          PlanSerializer)


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


class LatestPlanView(viewsets.ViewSet):

    def latest(self, request, format=None):
        try:
            plan = Plan.objects.latest()
        except Plan.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        serializer = PlanSerializer(plan)
        return Response(serializer.data)


class PlanViewSet(viewsets.ModelViewSet):
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()
