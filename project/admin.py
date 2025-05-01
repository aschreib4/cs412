# project/admin.py
# Made by Annelise Schreiber, aschreib@bu.edu
# Friday, April 18, 2025
# Description: registering the models for project application

from django.contrib import admin

# Register your models here.
from .models import ProjectProfile, OwnedItem, Recipe, Ingredient, RecipeCollection, RecipeCollectionRecipe
admin.site.register(ProjectProfile)
admin.site.register(OwnedItem)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(RecipeCollection)
admin.site.register(RecipeCollectionRecipe)