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
import plotly.offline as plotly
import plotly.graph_objs as go

from django.db import models

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

        if 'min_dob' in self.request.GET and self.request.GET['min_dob']:
            min_year = int(self.request.GET['min_dob'])
            results = results.filter(dob__year__gte=min_year)

        if 'max_dob' in self.request.GET and self.request.GET['max_dob']:
            max_year = int(self.request.GET['max_dob'])
            results = results.filter(dob__year__lte=max_year)

        if 'party_aff' in self.request.GET:
            party_aff = self.request.GET['party_aff']
            if party_aff:
                if party_aff == "not_rdu":
                    results = results.exclude(party_aff__in=['R ', 'D ', 'U '])
                else:
                    results = results.filter(party_aff=party_aff)
        if 'voter_score' in self.request.GET:
            voter_score = self.request.GET['voter_score']
            if voter_score:
                results = results.filter(voter_score=voter_score)

        if 'v20state' in self.request.GET:
            v20state = self.request.GET['v20state']
            if v20state.lower() == 'on':  # Checkbox checked
                results = results.filter(v20state=True)
            elif v20state.lower() == 'off': # Checkbox unchecked
                results = results.filter(v20state=False)
            
        if 'v21town' in self.request.GET:
            v21town = self.request.GET['v21town']
            if v21town.lower() == 'on':  # Checkbox checked
                results = results.filter(v21town=True)
            elif v21town.lower() == 'off': # Checkbox unchecked
                results = results.filter(v21town=False)

        if 'v21primary' in self.request.GET:
            v21primary = self.request.GET['v21primary']
            if v21primary.lower() == 'on':  # Checkbox checked
                results = results.filter(v21primary=True)
            elif v21primary.lower() == 'off':  # Checkbox unchecked
                results = results.filter(v21primary=False)

        if 'v22general' in self.request.GET:
            v22general = self.request.GET['v22general']
            if v22general.lower() == 'on':  # Checkbox checked
                results = results.filter(v22general=True)
            elif v22general.lower() == 'off':  # Checkbox unchecked
                results = results.filter(v22general=False)

        if 'v23town' in self.request.GET:
            v23town = self.request.GET['v23town']
            if v23town.lower() == 'on':  # Checkbox checked
                results = results.filter(v23town=True)
            elif v23town.lower() == 'off':  # Checkbox unchecked
                results = results.filter(v23town=False)
                
        return results
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the filter parameters to the context to retain them in the form after submission
        context['party_aff'] = self.request.GET.get('party_aff', '')
        context['dob'] = self.request.GET.get('dob', '')
        context['voter_score'] = self.request.GET.get('voter_score', '')
        context['v20state'] = self.request.GET.get('v20state', '')
        context['v21town'] = self.request.GET.get('v21town', '')
        context['v21primary'] = self.request.GET.get('v21primary', '')
        context['v22general'] = self.request.GET.get('v22general', '')
        context['v23town'] = self.request.GET.get('v23town', '')

        years = list(range(1920, 2026))
        context['years'] = years

        return context
    
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
    
class GraphsView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_context_data(self, **kwargs):
        '''Providing context variables for use in the template'''
        
        context = super().get_context_data(**kwargs)

        results = self.get_queryset()

        # Pass the filter parameters to the context to retain them in the form after submission
        context['party_aff'] = self.request.GET.get('party_aff', '')
        context['dob'] = self.request.GET.get('dob', '')
        context['voter_score'] = self.request.GET.get('voter_score', '')
        context['v20state'] = self.request.GET.get('v20state', '')
        context['v21town'] = self.request.GET.get('v21town', '')
        context['v21primary'] = self.request.GET.get('v21primary', '')
        context['v22general'] = self.request.GET.get('v22general', '')
        context['v23town'] = self.request.GET.get('v23town', '')

        years = list(range(1920, 2026))
        context['years'] = years

        # 1. Histogram: Distribution of Voters by Birth Year
        birth_years = results.values_list('dob', flat=True)
        birth_years = [dob.year for dob in birth_years]

        birth_year_counts = {}
        for year in birth_years:
            birth_year_counts[year] = birth_year_counts.get(year, 0) + 1

        x = list(birth_year_counts.keys())
        y = list(birth_year_counts.values())

        fig_birth_year = go.Bar(x=x, y=y, name='Voters by Birth Year')
        title_birth_year = 'Distribution of Voters by Birth Year'

        graph_div_birth_year = plotly.plot({
            'data': [fig_birth_year],
            'layout': {'title': title_birth_year}
        }, auto_open=False, output_type='div')

        context['graph_div_birth_year'] = graph_div_birth_year

        # 2. Pie Chart: Distribution of Voters by Party Affiliation
        party_affiliations = results.values_list('party_aff', flat=True)
        party_counts = {}
        for party in party_affiliations:
            party_counts[party] = party_counts.get(party, 0) + 1

        labels = list(party_counts.keys())
        values = list(party_counts.values())

        fig_party_affiliation = go.Pie(labels=labels, values=values, name='Voters by Party Affiliation')
        title_party_affiliation = 'Distribution of Voters by Party Affiliation'

        graph_div_party_affiliation = plotly.plot({
            'data': [fig_party_affiliation],
            'layout': {'title': title_party_affiliation}
        }, auto_open=False, output_type='div')

        context['graph_div_party_affiliation'] = graph_div_party_affiliation
        
        # 3. Histogram: Distribution of Voters by Election Participation
        election_participation = {
            'v20state': 0,
            'v21town': 0,
            'v21primary': 0,
            'v22general': 0,
            'v23town': 0
        }

        voters = results.all()
        for voter in voters:
            for election in election_participation.keys():
                if getattr(voter, election, False):
                    election_participation[election] += 1

        x_elections = list(election_participation.keys())
        y_elections = list(election_participation.values())

        fig_election_participation = go.Bar(x=x_elections, y=y_elections, name='Voter Participation in Elections')
        title_election_participation = 'Distribution of Voters by Election Participation'

        graph_div_election_participation = plotly.plot({
            'data': [fig_election_participation],
            'layout': {'title': title_election_participation}
        }, auto_open=False, output_type='div')

        context['graph_div_election_participation'] = graph_div_election_participation

        return context
    
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

        if 'min_dob' in self.request.GET and self.request.GET['min_dob']:
            min_year = int(self.request.GET['min_dob'])
            results = results.filter(dob__year__gte=min_year)

        if 'max_dob' in self.request.GET and self.request.GET['max_dob']:
            max_year = int(self.request.GET['max_dob'])
            results = results.filter(dob__year__lte=max_year)

        if 'party_aff' in self.request.GET:
            party_aff = self.request.GET['party_aff']
            if party_aff:
                if party_aff == "not_rdu":
                    results = results.exclude(party_aff__in=['R ', 'D ', 'U '])
                else:
                    results = results.filter(party_aff=party_aff)
        if 'voter_score' in self.request.GET:
            voter_score = self.request.GET['voter_score']
            if voter_score:
                results = results.filter(voter_score=voter_score)

        if 'v20state' in self.request.GET:
            v20state = self.request.GET['v20state']
            if v20state.lower() == 'on':  # Checkbox checked
                results = results.filter(v20state=True)
            elif v20state.lower() == 'off': # Checkbox unchecked
                results = results.filter(v20state=False)
            
        if 'v21town' in self.request.GET:
            v21town = self.request.GET['v21town']
            if v21town.lower() == 'on':  # Checkbox checked
                results = results.filter(v21town=True)
            elif v21town.lower() == 'off': # Checkbox unchecked
                results = results.filter(v21town=False)

        if 'v21primary' in self.request.GET:
            v21primary = self.request.GET['v21primary']
            if v21primary.lower() == 'on':  # Checkbox checked
                results = results.filter(v21primary=True)
            elif v21primary.lower() == 'off':  # Checkbox unchecked
                results = results.filter(v21primary=False)

        if 'v22general' in self.request.GET:
            v22general = self.request.GET['v22general']
            if v22general.lower() == 'on':  # Checkbox checked
                results = results.filter(v22general=True)
            elif v22general.lower() == 'off':  # Checkbox unchecked
                results = results.filter(v22general=False)

        if 'v23town' in self.request.GET:
            v23town = self.request.GET['v23town']
            if v23town.lower() == 'on':  # Checkbox checked
                results = results.filter(v23town=True)
            elif v23town.lower() == 'off':  # Checkbox unchecked
                results = results.filter(v23town=False)
                
        return results