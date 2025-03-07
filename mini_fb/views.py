# mini_fb/views.py
# Made by Annelise Schreiber, aschreib@bu.edu
# Friday, February 21, 2025
# Description: views for the mini_fb application

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, StatusMessage
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm
from django.urls import reverse

# Create your views here.
def show_all_profiles(request):
    '''Respond to the URL 'show_all_profiles', delegate work to a template.'''

    template_name = 'mini_fb/show_all_profiles.html'
    
    return render(request, template_name)

class ShowAllProfilesView(ListView):
    '''Define a view class to show all profiles'''
    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "profiles"

class ShowProfilePageView(DetailView):
    '''Define a view class to show a singular profile page'''
    model = Profile
    template_name = "mini_fb/show_profile.html"
    context_object_name = "profile" # note singular variable name

# Define a subclass of CreateView to handle creation of Profile objects
class CreateProfileView(CreateView):
    '''A view to handle creation of a new Profile.
    (1) Display the HTML form to the user (GET)
    (2) Process the form submission and store the new Profile object (POST)
    '''
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

    def form_valid(self, form):
        '''Override the default method to add some debug information.'''

        #print out the form data:
        print(f'CreateProfileView.form_valid(): {form.cleaned_data}')

        #delegate work to the superclass to do the rest:
        return super().form_valid(form)

# Define a subclass of CreateView to handle creation of StatusMessage objects
class CreateStatusMessageView(CreateView):
    '''A view to handle creation of a new Status Messgae on a Profile.
    (1) Display the HTML form to the user (GET)
    (2) Process the form submission and store the new StatusMessage object (POST)
    '''
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new Status Message.'''

        #create and return a URL:
        #retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        #call reverse to generate the URL for this Profile
        return reverse('show_profile', kwargs={'pk':pk})
    
    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''

        #calling the superclass method
        context = super().get_context_data()

        #find/add the profile to the context data
        #retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        #add this profile into the context dictionary:
        context['profile'] = profile
        return context
    
    def form_valid(self, form):
        '''This method handles the form submission and saves the
        new object to the Django database.
        We need to add the foreign key (of the Profile) to the Status Message
        object before saving it to the database.'''

        print(form.cleaned_data)
        #retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        #attach this profile to the status message
        form.instance.profile = profile #set the FK

        #delegate the work to the superclass method form_valid:
        return super().form_valid(form)

class UpdateProfileView(UpdateView):
    '''View class to handle update of a profile based on its PK.'''

    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"

class DeleteStatusMessageView(DeleteView):
    '''View class to delete a status message on a Profile.'''

    model = StatusMessage
    template_name = "mini_fb/delete_status_form.html"
    context_object_name = 'statusMessage'


    def get_success_url(self):
        '''Return the URL to redirect to after a successful delete.'''

        #find the PK for this statusMessage:
        pk = self.kwargs['pk']
        #find the statusMessage object:
        statusMessage = StatusMessage.objects.get(pk=pk)
        #find the PK of the Profile to which this status message is associated:
        profile = statusMessage.profile
        #return the URL to redirect to:
        return reverse('show_profile', kwargs={'pk':profile.pk})