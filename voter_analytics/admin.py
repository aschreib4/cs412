# voter_analytics/admin.py
# Made by Annelise Schreiber, aschreib@bu.edu
# Friday, April 4, 2025
# Description: registering the Profile model for voter_analytics application

from django.contrib import admin

# Register your models here.

from .models import Voter
admin.site.register(Voter)