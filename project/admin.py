# project/admin.py
# Made by Annelise Schreiber, aschreib@bu.edu
# Friday, April 18, 2025
# Description: registering the models for project application

from django.contrib import admin

# Register your models here.
from .models import Profile, OwnedItem, Recipe, Ingredient, RecipeCollection
admin.site.register(Profile)
admin.site.register(OwnedItem)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(RecipeCollection)