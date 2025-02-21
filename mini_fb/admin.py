# mini_fb/admin.py
# Made by Annelise Schreiber, aschreib@bu.edu
# Friday, February 21, 2025
# Description: registering the Profile model for mini_fb application

from django.contrib import admin

# Register your models here.
from .models import Profile
admin.site.register(Profile)