# mini_fb/forms.py
# Made by Annelise Schreiber, aschreib@bu.edu
# Friday, February 28, 2025
# Description: form to collect inputs to create a new Profile

from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    '''A form to add a profile to the database.'''

    class Meta:
        '''Associate this form with a model from our database.'''
        model = Profile
        # fields = ['first_name', 'last_name', 'city', 'email_address', 'profile_image_url']
        fields = ['first_name', 'last_name', 'city', 'email_address', 'image_file']

class UpdateProfileForm(forms.ModelForm):
    '''A form to handle an update to a Profile.'''

    class Meta:
        '''Associate this form with a model in our database.'''
        model = Profile
        fields = ['city', 'email_address', 'image_file'] #which fields we can update

class CreateStatusMessageForm(forms.ModelForm):
    '''A form to add a status message to a profile.'''

    class Meta:
        '''Associate this form with a model from our database.'''
        model = StatusMessage
        #fields = ['timestamp', 'message', 'profile']
        fields = ['message']