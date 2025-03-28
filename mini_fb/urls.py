## mini_fb/urls.py
# Made by Annelise Schreiber, aschreib@bu.edu
# Friday, February 21, 2025
# Description: url patterns for the mini_fb application

from django.urls import path
from django.conf import settings
from .views import * #ShowAllProfilesView, ShowProfilePageView
from django.contrib.auth import views as auth_views

# URL patterns for this app:
urlpatterns = [ 
    path(r'', ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name="show_profile"),
    path('create_profile', CreateProfileView.as_view(), name="create_profile"),
    path('profile/<int:pk>/create_status', CreateStatusMessageView.as_view(), name="create_status"),
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name='update_profile'),
    path('status/<int:pk>/delete', DeleteStatusMessageView.as_view(), name='delete_status'),
    path('status/<int:pk>/update', UpdateStatusMessageView.as_view(), name="update_status"),
    path('profile/<int:pk>/add_friend/<int:other_pk>', AddFriendView.as_view(), name="add_friend"),
    path('profile/<int:pk>/friend_suggestions', ShowFriendSuggestionsView.as_view(), name="friend_suggestions"),
    path('profile/<int:pk>/news_feed', ShowNewsFeedView.as_view(), name="news_feed"),
    #authorization-related URLS:
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page="logout_confirmation"), name='logout'),
    path('logout_confirmation/', LogoutConfirmationView.as_view(), name="logout_confirmation"),
    path('register/', UserRegistrationView.as_view(), name='register'),
]