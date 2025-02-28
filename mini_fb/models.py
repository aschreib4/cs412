# mini_fb/models.py
# Made by Annelise Schreiber, aschreib@bu.edu
# Friday, February 21, 2025
# Description: making/defining the Profile model for mini_fb application

from django.db import models
from django.urls import reverse

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
    
    def get_absolute_url(self):
        '''Return a URL to display one instance of this object.'''
        return reverse('show_profile', kwargs={'pk':self.pk})
    
    def get_status_messages(self):
        '''Return a QuerySet of status messages for this profile.'''
        #use the object manager to retrieve comments about this article
        statusMessages = StatusMessage.objects.filter(profile=self)
        return statusMessages
    
class StatusMessage(models.Model):
    '''Model the attributes of the Facebook status message'''

    #define the data attributes of the StatusMessage object:
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE) # cascade --> can't have status w/o profile

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.message}'
