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
    id = serializers.IntegerField(required=False)
    # ingredient = IngredientSerializer(read_only=True)  # Will only show on GET
    ingredient_id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), source='ingredient',
    )  # Will only be required on POST

    # TODO: Create and update here

    class Meta:
        model = RecipeIngredient
        exclude = ('recipe', 'ingredient')


class RecipeStepSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = RecipeStep
        exclude = ('recipe',)

        # TODO: Create and update here


class RecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    ingredients = RecipeIngredientSerializer(many=True, required=False)
    steps = RecipeStepSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'website', 'type', 'ingredients', 'steps')
        depth = 1

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients', None)
        steps = validated_data.pop('steps', None)
        recipe = Recipe.objects.create(**validated_data)
        if ingredients:
            for ingredient in ingredients:
                RecipeIngredient.objects.create(**ingredient, recipe=recipe)

        if steps:
            for step in steps:
                RecipeStep.objects.create(**step, recipe=recipe)

        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients', None)
        steps = validated_data.pop('steps', None)

        ingredient_ids = filter(lambda x: x is not None, [ingredient.get('id', None) for ingredient in ingredients])
        for ingredient in instance.ingredients.all():
            if ingredient.id not in ingredient_ids:
                ingredient.delete()

        step_ids = filter(lambda x: x is not None, [step.get('id', None) for step in steps])
        for step in instance.steps.all():
            if step.id not in step_ids:
                step.delete()

        for ingredient in ingredients:
            ingredient_id = ingredient.pop('id', None)
            temp_ingredient = RecipeIngredient.objects.get(id=ingredient_id) if ingredient_id else None
            if temp_ingredient:
                for attr, value in ingredient.items():
                    setattr(temp_ingredient, attr, value)
                temp_ingredient.save()
            else:
                RecipeIngredient.objects.create(**ingredient, recipe=instance)

        for step in steps:
            step_id = step.pop('id', None)
            temp_step = RecipeStep.objects.get(id=step_id) if step_id else None
            if temp_step:
                for attr, value in step.items():
                    setattr(temp_step, attr, value)
                temp_step.save()
            else:
                RecipeStep.objects.create(**step, recipe=instance)

        instance.name = validated_data.get('name', instance.name)
        instance.website = validated_data.get('website', instance.website)
        instance.type = validated_data.get('type', instance.type)
        instance.save()

        return instance


class PlanItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    day = serializers.IntegerField(required=True)
    recipe_id = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(), source='recipe', write_only=False, allow_null=True,
    )

    class Meta:
        model = PlanItem
        depth = 2
        fields = ('id', 'day', 'recipe_id', 'eaten')


class PlanSerializer(serializers.ModelSerializer):
    items = PlanItemSerializer(many=True, required=False)

    def create(self, validated_data):
        items = validated_data.pop('items', None)
        plan = Plan.objects.create(**validated_data)
        if items is not None:
            for item in items:
                day = item.pop('day')
                plan_item = PlanItem.objects.get(plan=plan, day=day)
                for attr, value in item.items():
                    setattr(plan_item, attr, value)
                plan_item.save()
        return plan

    def update(self, instance, validated_data):
        items = validated_data.pop('items', None)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.cost = validated_data.get('cost', instance.cost)
        instance.save()
        if items:
            for item in items:
                item_id = item.pop('id', None)
                if item_id:
                    plan_item = PlanItem.objects.get(id=item_id, plan=instance)
                    for attr, value in item.items():
                        setattr(plan_item, attr, value)
                    plan_item.save()
        return instance

    class Meta:
        model = Plan
        fields = ('id', 'start_date', 'end_date', 'cost', 'items')


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
