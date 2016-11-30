from django.db.models import Sum
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status, generics
from rest_framework.response import Response

from .models import Recipe, RecipeIngredient, RecipeStep, Plan, PlanItem, Ingredient
from .serializers import (RecipeSerializer,
                          ShoppingListSerializer,
                          PlanSerializer,
                          PlanItemSerializer,
                          IngredientSerializer,
                          RecipeStepSerializer,
                          RecipeIngredientSerializer)


class PlanList(generics.ListCreateAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer


class PlanDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer


class PlanItemList(generics.ListCreateAPIView):
    model = PlanItem
    serializer_class = PlanItemSerializer

    def get_queryset(self):
        """
        """
        return PlanItem.objects.filter(plan=self.kwargs['plan_pk'])

    def perform_create(self, serializer):
        plan = Plan.objects.get(pk=self.kwargs['plan_pk'])
        serializer.save(plan=plan)


class PlanItemDetail(generics.RetrieveUpdateDestroyAPIView):
    model = PlanItem
    serializer_class = PlanItemSerializer

    def get_queryset(self):
        """
        """
        return PlanItem.objects.filter(
            pk=self.kwargs['item_pk'],
            plan=self.kwargs['plan_pk'],
        )

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset)
        return obj


class RecipeList(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class RecipeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class RecipeStepList(generics.ListCreateAPIView):
    model = RecipeStep
    serializer_class = RecipeStepSerializer

    def get_queryset(self):
        """
        Returns a list of all steps for a given recipe
        """
        return RecipeStep.objects.filter(recipe=self.kwargs['pk'])

    def perform_create(self, serializer):
        recipe = Recipe.objects.get(pk=self.kwargs['pk'])
        serializer.save(recipe=recipe)


class RecipeStepDetail(generics.RetrieveUpdateDestroyAPIView):
    model = RecipeStep
    serializer_class = RecipeStepSerializer

    def get_queryset(self):
        """
        Returns a step in a recipe
        """
        return RecipeStep.objects.filter(
            step_number=self.kwargs['step_number'],
            recipe=self.kwargs['pk']
        )

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset)
        return obj


class RecipeIngredientList(generics.ListCreateAPIView):
    model = RecipeIngredient
    serializer_class = RecipeIngredientSerializer

    def get_queryset(self):
        """
        Returns a list of all ingredients for a recipe
        """
        return RecipeIngredient.objects.filter(recipe=self.kwargs['pk'])

    def perform_create(self, serializer):
        recipe = Recipe.objects.get(pk=self.kwargs['pk'])
        serializer.save(recipe=recipe)


class RecipeIngredientDetail(generics.RetrieveUpdateDestroyAPIView):
    model = RecipeIngredient
    serializer_class = RecipeIngredientSerializer

    def get_queryset(self):
        """
        This view should return an ingredient for a recipe
        """
        ingredient_id = self.kwargs['ingredient_pk']
        return RecipeIngredient.objects.filter(pk=ingredient_id)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset)
        return obj


# class RecipeDetailViewSet(viewsets.ViewSet):
#     queryset = Recipe.objects.all()
#     serializer_class = RecipeDetailSerializer
#
#     def list(self, request):
#         recipes = Recipe.objects.all()
#         serializer = RecipeDetailSerializer(recipes, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk=None):
#         queryset = Recipe.objects.all()
#         recipe = get_object_or_404(queryset, pk=pk)
#         serializer = RecipeDetailSerializer(recipe)
#         return Response(serializer.data)
#
#     def create(self, request):
#         print(request.data)
#         serializer = RecipeDetailSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             print('valid', serializer.data)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             print('errors', serializer.errors)
#         return Response({}, status=status.HTTP_400_BAD_REQUEST)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


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
