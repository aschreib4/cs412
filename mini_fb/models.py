# mini_fb/models.py
# Made by Annelise Schreiber, aschreib@bu.edu
# Friday, February 21, 2025
# Description: making/defining the Profile model for mini_fb application

from django.db import models

# Create your models here.
class Profile(models.Model):
    '''Encapsulate the data of a profile on a mini_fb app.'''

    #define the data attributes of the Profile object
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    city = models.TextField(blank=True)
    email_address = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    #published = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name}'
