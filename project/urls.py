## project/urls.py
# Made by Annelise Schreiber, aschreib@bu.edu
# Friday, April 18, 2025
# Description: url patterns for the project application

from django.urls import path
from django.conf import settings
from .views import *
from django.contrib.auth import views as auth_views

# URL patterns for this app:
urlpatterns = [
    path(r'', HomePageView.as_view(), name='homepage'),
    path('profiles/', ProfileListView.as_view(), name='profile_list'),
    path('profiles/<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('create_profile', CreateProfileView.as_view(), name="create_profile"),
    path('items/', owned_items_view, name='item_list'),
    path('recipes/', RecipeListView.as_view(), name='recipe_list'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('collections/', RecipeCollectionListView.as_view(), name='collection_list'),
    path('collections/<int:pk>/', RecipeCollectionDetailView.as_view(), name='collection_detail'),
    path('collections/create/', RecipeCollectionCreateView.as_view(), name='collection_create'),
    path('collections/<int:pk>/edit/', RecipeCollectionUpdateView.as_view(), name='collection_update'),
    #authorization-related URLS:
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page="logout_confirmation"), name='logout'),
    path('logout_confirmation/', LogoutConfirmationView.as_view(), name="logout_confirmation"),
]