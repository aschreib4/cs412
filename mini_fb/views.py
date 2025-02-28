# mini_fb/views.py
# Made by Annelise Schreiber, aschreib@bu.edu
# Friday, February 21, 2025
# Description: views for the mini_fb application

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile
from .forms import CreateProfileForm

# Create your views here.
def show_all_profiles(request):
    '''Respond to the URL 'show_all_profiles', delegate work to a template.'''

    template_name = 'mini_fb/show_all_profiles.html'
    
    return render(request, template_name)

class ShowAllProfilesView(ListView):
    '''Define a view class to show all profiles'''
    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "profiles"

class ShowProfilePageView(DetailView):
    '''Define a view class to show a singular profile page'''
    model = Profile
    template_name = "mini_fb/show_profile.html"
    context_object_name = "profile" # note singular variable name

# Define a subclass of CreateView to handle creation of Profile objects
class CreateProfileView(CreateView):
    '''A view to handle creation of a new Profile.
    (1) Display the HTML form to the user (GET)
    (2) Process the form submission and store the new Profile object (POST)
    '''
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"