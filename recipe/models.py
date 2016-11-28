from django.db import models
from .utils import calculate_week_ends_for_date, get_week_from_date

RECIPE_TYPES = (
    ('F', 'Fisk'),
    ('K', 'Kylling'),
    ('S', 'Svin'),
)

INGREDIENT_UNITS = (
    ('G', 'g'),
    ('K', 'kg'),
    ('TS', 'teskje'),
    ('SS', 'spiseskje'),
)

# Define possible days
MONDAY = 0
TUESDAY = 1
WEDNESDAY = 2
THURSDAY = 3
FRIDAY = 4
SATURDAY = 5
SUNDAY = 6

WEEKDAYS = (
    (MONDAY, 'Monday'),
    (TUESDAY, 'Tuesday'),
    (WEDNESDAY, 'Wednesday'),
    (THURSDAY, 'Thursday'),
    (FRIDAY, 'Friday'),
    (SATURDAY, 'Saturday'),
    (SUNDAY, 'Sunday')
)


class Recipe(models.Model):
    name = models.CharField(max_length=500, unique=True)
    website = models.URLField(blank=True, null=True)
    type = models.CharField(max_length=1, choices=RECIPE_TYPES)

    def __str__(self):
        return self.name


class RecipeStep(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='steps', on_delete=models.CASCADE)
    step_number = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return '{} step {}'.format(self.recipe, self.step_number)

    class Meta:
        ordering = ['step_number']


class Ingredient(models.Model):
    name = models.CharField(max_length=400, unique=True)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='ingredients', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient)
    amount = models.FloatField()
    unit = models.CharField(max_length=2, choices=INGREDIENT_UNITS)
    preparation = models.CharField(max_length=200, default="")

    @property
    def unit_display(self):
        return self.get_unit_display()

    def __str__(self):
        return '{} til {}'.format(self.ingredient, self.recipe)


class Plan(models.Model):
    start_date = models.DateField(unique=True)
    end_date = models.DateField(blank=True)
    cost = models.FloatField(blank=True, default=.0)

    @property
    def week(self):
        """
        Returns the week number for models instance
        :return: String representation of the week number
        """
        return str(get_week_from_date(self.start_date))

    def __str__(self):
        return 'Plan {week} in {year}'.format(week=self.week, year=self.start_date.year)

    def save(self, *args, **kwargs):
        self.start_date, self.end_date = calculate_week_ends_for_date(self.start_date)
        super(Plan, self).save(*args, **kwargs)

    class Meta:
        get_latest_by = 'end_date'
        ordering = ['-end_date']


class PlanItem(models.Model):
    plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
        related_name='days',
        related_query_name='day',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipes',
        related_query_name='recipe',
    )

    day = models.PositiveSmallIntegerField(choices=WEEKDAYS)
    eaten = models.BooleanField(default=False)

    class Meta:
        unique_together = ('plan', 'day')
        ordering = ['plan', 'day']
