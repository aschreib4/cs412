# project/forms.py
# Made by Annelise Schreiber, aschreib@bu.edu
# Thursday, May 1, 2025
# Description: form to collect inputs to create a new Project Profile, Recipe Collection, Recipe, etc.

from django import forms
from .models import ProjectProfile, RecipeCollection, RecipeCollectionRecipe, Recipe, Ingredient

class CreateProfileForm(forms.ModelForm):
    '''A form to add a profile to the database.'''

    class Meta:
        '''Associate this form with a model from our database.'''
        model = ProjectProfile
        fields = ['first_name', 'last_name'] #which fields we can update

class RecipeCollectionForm(forms.ModelForm):
    '''Form for handling validation and rendering.'''

    class Meta:
        '''Associate this form with a model in our database.'''
        model = RecipeCollection
        fields = ['collection_name']

class RecipeForm(forms.ModelForm):
    '''Form for handling validation and rendering.'''

    class Meta:
        '''Associate this form with a model in our database.'''
        model = Recipe
        fields = ['recipe_name', 'description']

class IngredientForm(forms.ModelForm):
    '''Form for handling validation and rendering.'''

    class Meta:
        '''Associate this form with a model in our database.'''
        model = Ingredient
        fields = ['ingredient_name', 'amount_required', 'units']

class RecipeCollectionRecipeForm(forms.ModelForm):
    '''Form for handling validation and rendering.'''

    class Meta:
        model = RecipeCollectionRecipe
        fields = ['collection']