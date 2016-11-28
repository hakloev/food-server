from rest_framework import serializers
from .models import (Recipe,
                     RecipeIngredient,
                     RecipeStep,
                     Ingredient,
                     Plan,
                     PlanItem)


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(read_only=True)

    # TODO: Create and update here

    class Meta:
        model = RecipeIngredient
        exclude = ('recipe',)


class RecipeStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeStep
        exclude = ('recipe',)

        # TODO: Create and update here


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    steps = RecipeStepSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'website', 'type', 'ingredients', 'steps')
        depth = 1


#############


class IngredientField(serializers.Field):
    def to_internal_value(self, data):
        return Ingredient.objects.filter(pk__in=data)

    def to_representation(self, value):
        obj = Ingredient.objects.get(pk=value)
        serializer = IngredientSerializer(obj)
        return serializer.data


class ShoppingListSerializer(serializers.ModelSerializer):
    total_amount = serializers.SerializerMethodField(read_only=True)
    ingredient = IngredientField()

    @staticmethod
    def get_total_amount(obj):
        return obj['total_amount'] if 'total_amount' in obj else 0.0

    class Meta:
        model = RecipeIngredient
        fields = ('ingredient', 'total_amount')


class PlanItemSerializer(serializers.ModelSerializer):
    recipe = RecipeSerializer(read_only=False)

    class Meta:
        model = PlanItem
        depth = 2
        fields = ('day', 'recipe', 'eaten')


class PlanSerializer(serializers.ModelSerializer):
    days = PlanItemSerializer(many=True, read_only=False)

    class Meta:
        model = Plan
        fields = ('id', 'start_date', 'end_date', 'cost', 'days')
