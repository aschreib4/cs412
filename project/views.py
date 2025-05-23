# project/views.py
# Made by Annelise Schreiber, aschreib@bu.edu
# Thursday, May 1, 2025
# Description: views for the project application

from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, FormView
from .models import ProjectProfile, OwnedItem, Recipe, Ingredient, RecipeCollection, RecipeCollectionRecipe
from django.urls import reverse_lazy
from .forms import CreateProfileForm, RecipeForm, IngredientForm, RecipeCollectionForm, ItemForm
from django.contrib.auth.forms import UserCreationForm ## for new User
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin ## for authentication

# Create your views here.
def get_user_profile(user):
    try:
        return ProjectProfile.objects.get(project_user=user)
    except ProjectProfile.DoesNotExist:
        raise Http404("Profile not found")
    
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
        '''Provide additional context to template'''

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
        '''Provide additional context to template'''

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

class UserRecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'project/user_recipe_list.html'
    context_object_name = 'userrecipes'

    def get_queryset(self):
        # Get the ProjectProfile for the logged-in user
        profile = ProjectProfile.objects.get(project_user=self.request.user)
        # Filter the recipes by the logged-in user's profile
        return Recipe.objects.filter(created_by=profile)

class RecipeDetailView(DetailView):
    '''Define a view class to show a singular recipe page'''

    model = Recipe
    template_name = 'project/recipe_detail.html'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        '''Provide additional context to template'''

        context = super().get_context_data(**kwargs)

        # Add the ingredients related to this recipe to the context
        recipe = self.get_object()
        context['ingredients'] = recipe.ingredients.all()

        return context

class RecipeCreateView(LoginRequiredMixin, CreateView):
    '''Define a class to create a recipe page'''

    model = Recipe
    form_class = RecipeForm
    template_name = 'project/create_recipe.html'
    
    def form_valid(self, form):
        user_profile = get_object_or_404(ProjectProfile, project_user=self.request.user)
        form.instance.profile = user_profile
        form.instance.created_by = user_profile
        recipe = form.save()
        return redirect('create_ingredient', recipe_id=recipe.pk)
    
    def get_success_url(self):
        return reverse_lazy('project/recipe_list')
    
class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    '''Define a class to update a recipe page'''

    model = Recipe
    form_class = RecipeForm
    template_name = 'project/update_recipe.html'
    
    def get_queryset(self):
        # Ensure the recipe belongs to the logged-in user
        user_profile = get_user_profile(self.request.user)
        return Recipe.objects.filter(created_by=user_profile)
    
    def get_success_url(self):
        return reverse_lazy('user_recipe_list')
    
class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    '''Define a class to delete a recipe page'''

    model = Recipe
    template_name = 'project/delete_recipe.html'
    context_object_name = 'recipe'

    def get_queryset(self):
        '''Provide additional context to template'''

        # Ensure the recipe belongs to the logged-in user
        user_profile = get_user_profile(self.request.user)
        return Recipe.objects.filter(created_by=user_profile)

    def get_success_url(self):
        return reverse_lazy('user_recipe_list')
    
class ItemCreateView(LoginRequiredMixin, CreateView):
    '''Define a class to create a recipe page'''

    model = OwnedItem
    form_class = ItemForm
    template_name = 'project/create_item.html'
    
    def form_valid(self, form):
        user_profile = get_object_or_404(ProjectProfile, project_user=self.request.user)
        form.instance.profile = user_profile
        form.instance.created_by = user_profile
        owneditem = form.save()
        return redirect('item_list')
    
    def get_success_url(self):
        return reverse_lazy('item_list')

class ItemDeleteView(LoginRequiredMixin, DeleteView):
    '''Define a class to delete a recipe page'''

    model = OwnedItem
    template_name = 'project/delete_item.html'
    context_object_name = 'owneditem'

    def get_queryset(self):
        # Ensure the item belongs to the logged-in user
        user_profile = get_user_profile(self.request.user)
        return OwnedItem.objects.filter(profile=user_profile)

    def get_success_url(self):
        return reverse_lazy('item_list')
    
class IngredientCreateView(LoginRequiredMixin, CreateView):
    '''Define a class to create ingredients for a recipe'''

    model = Ingredient
    form_class = IngredientForm
    template_name = 'project/create_ingredient.html'

    def dispatch(self, request, *args, **kwargs):
        # Get the recipe from the URL
        self.recipe = get_object_or_404(Recipe, pk=self.kwargs['recipe_id'])
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        recipe = get_object_or_404(Recipe, pk=self.kwargs['recipe_id'])
        form.instance.recipe = recipe
        return super().form_valid(form)
    
    def get_success_url(self):
        # Redirect to the recipe detail page after successful ingredient creation
        return reverse_lazy('recipe_detail', kwargs={'pk': self.recipe.pk})
    
    def get_context_data(self, **kwargs):
        '''Provide additional context to template'''

        context = super().get_context_data(**kwargs)
        recipe = get_object_or_404(Recipe, pk=self.kwargs['recipe_id'])
        context['recipe'] = recipe
        context['form'] = self.get_form()
        return context

class RecipeCollectionListView(ListView):
    '''Define a view class to show all recipe collections'''

    model = RecipeCollection
    template_name = 'project/collection_list.html'
    context_object_name = 'collections'

class UserCollectionListView(LoginRequiredMixin, ListView):
    model = RecipeCollection
    template_name = 'project/user_collection_list.html'
    context_object_name = 'usercollections'

    def get_queryset(self):
        # Get the ProjectProfile for the logged-in user
        profile = ProjectProfile.objects.get(project_user=self.request.user)
        # Filter the recipes by the logged-in user's profile
        return RecipeCollection.objects.filter(collected_by=profile)

class RecipeCollectionDetailView(DetailView):
    '''Define a view class to show a singular recipe collection page'''

    model = RecipeCollection
    template_name = 'project/collection_detail.html'
    context_object_name = 'collection'

    def get_context_data(self, **kwargs):
        '''Provide additional context to template'''

        context = super().get_context_data(**kwargs)
        # Get the current collection instance
        collection = self.object
        # Get only recipes for this specific collection
        recipe_links = RecipeCollectionRecipe.objects.filter(collection=collection)
        context['recipe_links'] = recipe_links
        return context
    
class RecipeCollectionCreateView(LoginRequiredMixin, CreateView):
    '''Define a class to create recipe collections'''

    model = RecipeCollection
    form_class = RecipeCollectionForm
    template_name = 'project/recipe_collection_form.html'

    def form_valid(self, form):
        user_profile = get_object_or_404(ProjectProfile, project_user=self.request.user)
        form.instance.collected_by = user_profile
        collection = form.save()
        return super().form_valid(form)
        
    def get_success_url(self):
        return reverse_lazy('collection_list')

class RecipeCollectionDeleteView(LoginRequiredMixin, DeleteView):
    '''Define a class to delete a recipe collection'''

    model = RecipeCollection
    template_name = 'project/delete_collection.html'
    context_object_name = 'collection'

    def get_queryset(self):
        # Ensure the collection belongs to the logged-in user
        user_profile = get_user_profile(self.request.user)
        return RecipeCollection.objects.filter(collected_by=user_profile)

    def get_success_url(self):
        return reverse_lazy('user_collection_list')

def add_recipe_to_collection(request, recipe_id):
    """Function-based view for adding a recipe to a collection"""

    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if request.method == 'POST':
        
        collection_id = request.POST.get('collection_id')

        if not collection_id:
            messages.error(request, "No collection was selected.")
            return redirect('recipe_detail', pk=recipe.pk)

        project_profile = get_object_or_404(ProjectProfile, project_user=request.user)
        collection = get_object_or_404(RecipeCollection, collection_name=collection_id, collected_by=project_profile)

        # Check if the recipe is already in the selected collection
        if RecipeCollectionRecipe.objects.filter(recipe=recipe, collection=collection).exists():
            messages.warning(request, "This recipe is already in this collection.")
            return redirect('recipe_detail', pk=recipe.pk)
        
        # Create a new RecipeCollectionRecipe object and associate it with the recipe and collection
        recipecollectionrecipe = RecipeCollectionRecipe(recipe=recipe, collection=collection)
        recipecollectionrecipe.save()

        messages.success(request, f'Added {recipe.recipe_name} to the collection "{collection.collection_name}".')
        return redirect('recipe_list')

    else:
        project_profile = get_object_or_404(ProjectProfile, project_user=request.user)
        collections = RecipeCollection.objects.filter(collected_by=project_profile)

        return render(request, 'project/add_recipe_to_collection.html', {
            'recipe': recipe,
            'collections': collections
        })

# Function that will check if a user can make a recipe
def can_make_recipe(user_profile, recipe):
    required_ingredients = Ingredient.objects.filter(recipe=recipe)

    for ingredient in required_ingredients:
        owned_item = OwnedItem.objects.filter(profile=user_profile, item_name=ingredient.ingredient_name).first()

        if not owned_item or owned_item.quantity < ingredient.amount_required:
            return False

    return True

# Function to check for a user's missing ingredients
def check_missing_ingredients(user_profile, recipe):
    missing_ingredients = []
    required_ingredients = Ingredient.objects.filter(recipe=recipe)

    for ingredient in required_ingredients:
        owned_item = OwnedItem.objects.filter(profile=user_profile, item_name=ingredient.ingredient_name).first()

        if not owned_item:
            missing_ingredients.append(ingredient)
        elif owned_item.quantity < ingredient.amount_required:
            missing_ingredients.append(ingredient)

    return missing_ingredients

def recipe_list(request):
    user_profile = ProjectProfile.objects.filter(user=request.user).first()
    recipes = Recipe.objects.all()

    recipes_user_can_make = []

    for recipe in recipes:
        missing_ingredients = check_missing_ingredients(user_profile, recipe)
        if not missing_ingredients:
            recipes_user_can_make.append({
                'recipe': recipe,
                'missing_ingredients': missing_ingredients
            })
    return render(request, 'project/feasible_recipes.html', {
        'recipes': recipes_user_can_make,
    })

class FeasibleRecipesPageView(TemplateView):
    '''Define a view class to display the feasible recipes for a user'''

    template_name = 'project/feasible_recipes.html'

    def get_context_data(self, **kwargs):
        user_profile = ProjectProfile.objects.filter(project_user=self.request.user).first()
        
        if not user_profile:
            return {}

        recipes_user_can_make = []
        recipes_user_cannot_make = []
        
        recipes = Recipe.objects.prefetch_related('ingredients').all()

        owned_items_dict = {item.item_name: item for item in OwnedItem.objects.filter(profile=user_profile)}

        for recipe in recipes:
            missing_ingredients = []

            for ingredient in recipe.ingredients.all():
                owned_item = owned_items_dict.get(ingredient.ingredient_name)

                if not owned_item or owned_item.quantity < ingredient.amount_required:
                    missing_ingredients.append(ingredient)

            if not missing_ingredients:
                recipes_user_can_make.append({
                    'recipe': recipe,
                    'missing_ingredients': missing_ingredients
                })
            else:
                recipes_user_cannot_make.append({
                    'recipe': recipe,
                    'missing_ingredients': missing_ingredients
                })

        context = super().get_context_data(**kwargs)
        context['recipes_user_can_make'] = recipes_user_can_make
        context['recipes_user_cannot_make'] = recipes_user_cannot_make
        return context

class LogoutConfirmationView(TemplateView):
    '''Define a view class to show a logout confirmation page'''
    model = ProjectProfile
    template_name = "project/logged_out.html"
    context_object_name = "profile"