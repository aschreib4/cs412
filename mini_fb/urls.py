## mini_fb/urls.py
# Made by Annelise Schreiber, aschreib@bu.edu
# Friday, February 21, 2025
# Description: url patterns for the mini_fb application

from django.urls import path
from django.conf import settings
from .views import * #ShowAllProfilesView, ShowProfilePageView

# URL patterns for this app:
urlpatterns = [ 
    path(r'', ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name="show_profile"),
    path('create_profile', CreateProfileView.as_view(), name="create_profile"),
    path('profile/<int:pk>/create_status', CreateStatusMessageView.as_view(), name="create_status"),
]