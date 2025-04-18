# project/models.py
# Made by Annelise Schreiber, aschreib@bu.edu
# Friday, April 18, 2025
# Description: making/defining the models for the project application

from django.db import models

# Create your models here.
class Profile(models.Model):
    '''Model the attributes for the Profile of the user.'''

    first_name = models.TextField()
    last_name = models.TextField()

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f"{self.first_name} {self.last_name}"

class OwnedItem(models.Model):
    '''Model the attributes for the food items the user owns.'''

    item_name = models.TextField()
    quantity = models.FloatField()
    units = models.TextField(blank=True)
    expiration_date = models.DateField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f"{self.quantity} {self.units} of {self.item_name}"

class Recipe(models.Model):
    '''Model the attributes for the recipes on the site.'''

    recipe_name = models.TextField()
    description = models.TextField()
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f"{self.recipe_name}"

class Ingredient(models.Model):
    '''Model the attributes for the ingredients that are in the recipes.'''

    ingredient_name = models.TextField()
    amount_required = models.FloatField()
    units = models.TextField(blank=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f"Need {self.amount_required} {self.units} of {self.ingredient_name}"
    
class RecipeCollection(models.Model):
    '''Model the attributes for the collections of recipes that will be formed.'''

    collection_name = models.TextField()
    collected_by = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f"{self.collection_name}"
    
# Intermediary model to link Recipe and RecipeCollection (for many to many relationship)
class RecipeCollectionRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    collection = models.ForeignKey(RecipeCollection, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.recipe.recipe_name} in {self.collection.collection_name}"
