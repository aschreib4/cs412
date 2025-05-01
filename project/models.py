# project/models.py
# Made by Annelise Schreiber, aschreib@bu.edu
# Friday, April 18, 2025
# Description: making/defining the models for the project application

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class ProjectProfile(models.Model):
    '''Model the attributes for the Profile of the user.'''

    project_user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.TextField()
    last_name = models.TextField()

    class Meta:
        db_table = 'profile'

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f"{self.first_name} {self.last_name}"
    
    def get_owned_items(self):
        '''Return a QuerySet of owned items for this profile.'''
        #use the object manager to retrieve owned items for this profile
        ownedItems = OwnedItem.objects.filter(profile=self)
        return ownedItems

class OwnedItem(models.Model):
    '''Model the attributes for the food items the user owns.'''

    item_name = models.TextField()
    quantity = models.FloatField()
    units = models.TextField(blank=True)
    expiration_date = models.DateField()
    profile = models.ForeignKey(ProjectProfile, on_delete=models.CASCADE)

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f"{self.quantity} {self.units} of {self.item_name}"

class Recipe(models.Model):
    '''Model the attributes for the recipes on the site.'''

    recipe_name = models.TextField()
    description = models.TextField()
    created_by = models.ForeignKey(ProjectProfile, on_delete=models.CASCADE)

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
    collected_by = models.ForeignKey(ProjectProfile, on_delete=models.CASCADE)

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f"{self.collection_name}"

#Intermediary Model
class RecipeCollectionRecipe(models.Model):
    '''Intermediary model to link Recipe and RecipeCollection (for "many to many" relationship).'''

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    collection = models.ForeignKey(RecipeCollection, on_delete=models.CASCADE)

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f"{self.recipe.recipe_name} in {self.collection.collection_name}"
