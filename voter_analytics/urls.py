## voter_analytics/urls.py
# Made by Annelise Schreiber, aschreib@bu.edu
# Friday, April 4, 2025
# Description: url patterns for the voter_analytics application

from django.urls import path
from django.conf import settings
from .views import *

# URL patterns for this app:
urlpatterns = [
    path(r'', VoterRecordsListView.as_view(), name='voters'),
    path(r'voter/<int:pk>', VoterDetailView.as_view(), name='voter'),
]