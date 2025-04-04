# voter_analytics/views.py
# Made by Annelise Schreiber, aschreib@bu.edu
# Friday, April 4, 2025
# Description: views for the voter_analytics application

from django.shortcuts import render

# Create your views here.
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . models import Voter

# Import plotly library for graphing
import plotly
import plotly.graph_objs as go

class VoterRecordsListView(ListView):
    '''View to display voter records.'''

    template_name = 'voter_analytics/voter_records.html'
    model = Voter
    context_object_name = 'results'
    paginate_by = 100 # how many records per page

    def get_queryset(self):
        
        # start with entire queryset
        results = super().get_queryset()

        # filter results by these field(s):
        if 'first_name' in self.request.GET:
            first_name = self.request.GET['first_name']
            if first_name:
                results = results.filter(first_name=first_name)
        if 'last_name' in self.request.GET:
            last_name = self.request.GET['last_name']
            if last_name:
                results = results.filter(last_name=last_name)
        if 'street_num' in self.request.GET:
            street_num = self.request.GET['street_num']
            if street_num:
                results = results.filter(street_num=street_num)
        if 'street_name' in self.request.GET:
            street_name = self.request.GET['street_name']
            if street_name:
                results = results.filter(street_name=street_name)
        if 'apt_num' in self.request.GET:
            apt_num = self.request.GET['apt_num']
            if apt_num:
                results = results.filter(apt_num=apt_num)
        if 'zip_code' in self.request.GET:
            zip_code = self.request.GET['zip_code']
            if zip_code:
                results = results.filter(zip_code=zip_code)
        if 'dob' in self.request.GET:
            dob = self.request.GET['dob']
            if dob:
                results = results.filter(dob=dob)
        if 'party_aff' in self.request.GET:
            party_aff = self.request.GET['party_aff']
            if party_aff:
                results = results.filter(party_aff=party_aff)
        if 'voter_score' in self.request.GET:
            voter_score = self.request.GET['voter_score']
            if voter_score:
                results = results.filter(voter_score=voter_score)
                
        return results
    
class VoterDetailView(DetailView):
    '''Display the voter record for a single person.'''

    model = Voter
    context_object_name = 'r' #short for record
    template_name = 'voter_analytics/record_detail.html'

    def get_context_data(self, **kwargs) :
        '''Provide context variables for use in template'''
        # start with superclass context
        context = super().get_context_data(**kwargs)
        r = context['r']

        return context