from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, DetailView
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Recipe, RecipeIngredient, RecipeStep, Plan
from .serializers import RecipeSerializer, RecipeDetailSerializer, ShoppingListSerializer, PlanSerializer
from .forms import RecipeForm, IngredientFormSet, StepFormSet


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


class PlanViewSet(viewsets.ModelViewSet):
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()


class RecipeDetailView(DetailView):
    template_name = 'recipe/recipe_detail.html'
    model = Recipe

    def get_context_data(self, **kwargs):
        context = super(RecipeDetailView, self).get_context_data(**kwargs)
        context['ingredients'] = RecipeIngredient.objects.filter(recipe=context['recipe'])
        context['steps'] = RecipeStep.objects.filter(recipe=context['recipe'])
        return context


class RecipeCreateView(CreateView):
    template_name = 'recipe/recipe_form.html'
    model = Recipe
    form_class = RecipeForm

    def get(self, request, *args, **kwargs):
        self.object = None
        form = self.form_class(self.object)

        ingredient_form = IngredientFormSet(instance=self.object)
        step_form = StepFormSet(instance=self.object)

        return self.render_to_response(
            self.get_context_data(
                form=form,
                ingredient_form=ingredient_form,
                step_form=step_form
            )
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.form_class(request.POST)

        ingredient_form = IngredientFormSet(request.POST, instance=self.object)
        step_form = StepFormSet(request.POST, instance=self.object)

        if form.is_valid() and ingredient_form.is_valid() and step_form.is_valid():
            return self.form_valid(form, ingredient_form, step_form)

        return self.form_invalid(form, ingredient_form, step_form)

    def form_valid(self, form, ingredient_form, step_form):
        self.object = form.save()
        ingredient_form.instance = self.object
        ingredient_form.save()
        step_form.instance = self.object
        step_form.save()
        return HttpResponseRedirect('/')

    def form_invalid(self, form, ingredient_form, step_form):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  ingredient_form=ingredient_form,
                                  step_form=step_form
                                  )
        )


class RecipeEditView(UpdateView):

    template_name = 'recipe/recipe_form.html'
    model = Recipe
    form_class = RecipeForm

    def get_object(self, queryset=None):
        obj = Recipe.objects.get(id=self.kwargs['pk'])
        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(instance=self.object)

        ingredient_form = IngredientFormSet(instance=self.object)
        step_form = StepFormSet(instance=self.object)

        return self.render_to_response(
            self.get_context_data(
                form=form,
                ingredient_form=ingredient_form,
                step_form=step_form
            )
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)

        ingredient_form = IngredientFormSet(request.POST, instance=self.object)
        step_form = StepFormSet(request.POST, instance=self.object)

        if form.is_valid() and ingredient_form.is_valid() and step_form.is_valid():
            return self.form_valid(form, ingredient_form, step_form)

        return self.form_invalid(form, ingredient_form, step_form)

    def form_valid(self, form, ingredient_form, step_form):
        self.object = form.save()
        ingredient_form.instance = self.object
        ingredient_form.save()
        step_form.instance = self.object
        step_form.save()
        return HttpResponseRedirect('/')

    def form_invalid(self, form, ingredient_form, step_form):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  ingredient_form=ingredient_form,
                                  step_form=step_form
                                  )
        )
