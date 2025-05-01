# project/forms.py
# Made by Annelise Schreiber, aschreib@bu.edu
# Thursday, May 1, 2025
# Description: form to collect inputs to create a new Project Profile, Recipe Collection, Recipe, etc.

from django import forms
from .models import ProjectProfile, RecipeCollection, RecipeCollectionRecipe, Recipe

class CreateProfileForm(forms.ModelForm):
    '''A form to add a profile to the database.'''

    class Meta:
        '''Associate this form with a model from our database.'''
        model = ProjectProfile
        fields = ['first_name', 'last_name']

class UpdateCollectionForm(forms.ModelForm):
    '''A form to handle an update to a Recipe Collection's Recipes.'''

    class Meta:
        '''Associate this form with a model in our database.'''
        model = RecipeCollectionRecipe
        fields = ['recipe'] #which fields we can update
