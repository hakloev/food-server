from django.db import models

RECIPE_TYPES = (
    ('F', 'Fisk'),
    ('K', 'Kylling'),
    ('S', 'Svin'),
)


class Recipe(models.Model):
    name = models.CharField(max_length=500)
    website = models.URLField(blank=True, null=True)
    type = models.CharField(max_length=1, choices=RECIPE_TYPES)

    def __str__(self):
        return self.name


class RecipeStep(models.Model):
    recipe = models.ForeignKey(Recipe)
    step_number = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return '{} step {}'.format(self.recipe, self.step_number)

    class Meta:
        ordering = ['step_number']


class Ingredient(models.Model):
    name = models.CharField(max_length=400)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe)
    ingredient = models.ForeignKey(Ingredient)
    amount = models.FloatField()
    unit = models.CharField(max_length=100)
    preparation = models.TextField()

    def __str__(self):
        return '{} til {}'.format(self.ingredient, self.recipe)