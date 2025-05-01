# project/views.py
# Made by Annelise Schreiber, aschreib@bu.edu
# Thursday, May 1, 2025
# Description: views for the project application

from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View, TemplateView
from .models import ProjectProfile, OwnedItem, Recipe, Ingredient, RecipeCollection, RecipeCollectionRecipe
from django.urls import reverse
from .forms import CreateProfileForm
from django.contrib.auth.forms import UserCreationForm ## for new User
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin ## for authentication

# Create your views here.
class HomePageView(TemplateView):
    '''Define a view class to display the home page'''

    template_name = 'project/homepage.html'

class ProfileListView(ListView):
    '''Define a view class to show all profiles'''

    model = ProjectProfile
    template_name = 'project/profile_list.html'
    context_object_name = 'projectprofiles'

class ProfileDetailView(DetailView):
    '''Define a view class to show a singular profile page'''

    model = ProjectProfile
    template_name = 'project/profile_detail.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        # Get the default context data (profile data)
        context = super().get_context_data(**kwargs)

        # Get the specific profile (using the pk from the URL)
        profile = self.get_object()

        # Get all of the recipes that the user has created
        context['recipes'] = Recipe.objects.filter(created_by=profile)  # Recipes created by the profile

        return context
    
class CreateProfileView(CreateView):
    '''A view to handle creation of a new Profile.
    (1) Display the HTML form to the user (GET)
    (2) Process the form submission and store the new Profile object (POST)
    '''
    form_class = CreateProfileForm
    template_name = "project/create_profile_form.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_creation_form'] = UserCreationForm()
        return context
    
    def form_valid(self, form):
        '''Override the default method to add some debug information.'''

        user_creation_form = UserCreationForm(self.request.POST)

        if user_creation_form.is_valid():
            user = user_creation_form.save()
            login(self.request, user)
            
            form.instance.user = user

            return super().form_valid(form)
            
        else:
            return self.form_invalid(form)
        
def owned_items_view(request):
    # Get the logged-in user's profile
    user_profile = ProjectProfile.objects.get(project_user=request.user)

    # Use the method from the profile to get the owned items
    owned_items = user_profile.get_owned_items()

    # Pass the owned items to the template
    return render(request, 'project/owned_items_list.html', {'owned_items': owned_items})

class OwnedItemListView(ListView):
    '''Define a view class to show all owned items of a profile'''

    model = OwnedItem
    template_name = 'project/owned_item_list.html'
    context_object_name = 'items'

class RecipeListView(ListView):
    '''Define a view class to show all recipes'''

    model = Recipe
    template_name = 'project/recipe_list.html'
    context_object_name = 'recipes'

class RecipeDetailView(DetailView):
    '''Define a view class to show a singular recipe page'''

    model = Recipe
    template_name = 'project/recipe_detail.html'
    context_object_name = 'recipe'

class RecipeCollectionListView(ListView):
    '''Define a view class to show all recipe collections'''

    model = RecipeCollection
    template_name = 'project/collection_list.html'
    context_object_name = 'collections'

class RecipeCollectionDetailView(DetailView):
    '''Define a view class to show a singular recipe collection page'''

    model = RecipeCollection
    template_name = 'project/collection_detail.html'
    context_object_name = 'collection'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the current collection instance
        collection = self.object
        # Get only recipes for this specific collection
        recipe_links = RecipeCollectionRecipe.objects.filter(collection=collection)
        context['recipe_links'] = recipe_links  # NOT 'recipes' to match template
        return context
    
class RecipeCollectionCreateView(CreateView):
    model = RecipeCollection
    fields = ['collection_name', 'collected_by']
    template_name = 'project/recipe_collection_form.html'
    success_url = '/collections/'

class RecipeCollectionUpdateView(UpdateView):
    model = RecipeCollection
    fields = ['collection_name', 'collected_by']
    template_name = 'project/recipe_collection_form.html'
    success_url = '/collections/'

class RecipeCollectionDeleteView(DeleteView):
    model = RecipeCollection
    template_name = 'project/recipe_collection_confirm_delete.html'
    success_url = '/collections/'

class LogoutConfirmationView(TemplateView):
    '''Define a view class to show a logout confirmation page'''
    model = ProjectProfile
    template_name = "project/logged_out.html"
    context_object_name = "profile"