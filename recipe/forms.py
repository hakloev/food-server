from django.forms import ModelForm, Textarea, Select
from django.forms.models import inlineformset_factory

from .models import Recipe, RecipeIngredient, RecipeStep


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'
        widgets = {
            'type': Select
        }

IngredientFormSet = inlineformset_factory(
    Recipe,
    RecipeIngredient,
    form=RecipeForm,
    fk_name='recipe',
    extra=1,
    can_delete=False,
    widgets={
      'preparation': Textarea(attrs={'class': 'materialize-textarea'}),
    }
)

StepFormSet = inlineformset_factory(
    Recipe,
    RecipeStep,
    form=RecipeForm,
    extra=1,
    can_delete=False,
    widgets={
        'description': Textarea(attrs={'class': 'materialize-textarea'}),
    }
)
