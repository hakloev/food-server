from django.contrib import admin
from .models import Ingredient, Recipe, RecipeIngredient, RecipeStep, Plan, PlanItem


class PlanItemInline(admin.TabularInline):
    """
    Adds inline form with PlanItems for the PlanAdmin
    """
    model = PlanItem
    extra = 0


class PlanAdmin(admin.ModelAdmin):
    exclude = ('end_date',)
    inlines = [
        PlanItemInline,
    ]


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 0


class RecipeStepInline(admin.TabularInline):
    model = RecipeStep
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        RecipeStepInline,
        RecipeIngredientInline,
    ]


# admin.site.register(PlanItem, Plan)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Recipe, RecipeAdmin)

admin.site.register(Ingredient)
admin.site.register(RecipeIngredient)
admin.site.register(RecipeStep)
