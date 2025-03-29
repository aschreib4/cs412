# mini_fb/views.py
# Made by Annelise Schreiber, aschreib@bu.edu
# Friday, February 21, 2025
# Description: views for the mini_fb application

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View, TemplateView
from .models import Profile, StatusMessage, Image, StatusImage
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin ## for authentication
from django.contrib.auth.forms import UserCreationForm ## for new User
from django.contrib.auth.models import User ## the Django user model

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

    def dispatch(self, request, *args, **kwargs):
        '''Override the dispatch method to add debugging information.'''
        if request.user.is_authenticated:
            print(f'ShowAllProfilesView.dispatch(): request.user={request.user}')
        else:
            print(f'ShowAllProfilesView.dispatch(): not logged in.')
        return super().dispatch(request, *args, **kwargs)

class ShowProfilePageView(DetailView):
    '''Define a view class to show a singular profile page'''
    model = Profile
    template_name = "mini_fb/show_profile.html"
    context_object_name = "profile" # note singular variable name

    def get_object(self):
        '''Get the Profile object associated with the logged-in user.'''
        try:
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            return redirect('create_profile')
        
    def get_context_data(self, **kwargs):
        '''Add context data to the template (user info).'''
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

# Define a subclass of CreateView to handle creation of Profile objects
class CreateProfileView(LoginRequiredMixin, CreateView):
    '''A view to handle creation of a new Profile.
    (1) Display the HTML form to the user (GET)
    (2) Process the form submission and store the new Profile object (POST)
    '''
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

    def get_object(self):
        '''Get the Profile object associated with the logged-in user.'''
        try:
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            return redirect('create_profile')

    def get_login_url(self):
        '''Return the URL for this app's login page.'''
        
        return reverse('login')
    
    def form_valid(self, form):
        '''Override the default method to add some debug information.'''

        #print out the form data:
        print(f'CreateProfileView.form_valid(): {form.cleaned_data}')

        #find the logged in user
        user = self.request.user
        print(f'CreateProfileView.form_valid(): {user}')

        #attach that user to the form instance (to the Profile object)
        form.instance.user = user

        #delegate work to the superclass to do the rest:
        return super().form_valid(form)

# Define a subclass of CreateView to handle creation of StatusMessage objects
class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    '''A view to handle creation of a new Status Messgae on a Profile.
    (1) Display the HTML form to the user (GET)
    (2) Process the form submission and store the new StatusMessage object (POST)
    '''
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_object(self):
        '''Get the Profile object associated with the logged-in user.'''
        try:
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            return redirect('create_profile')

    def get_login_url(self):
        '''Return the URL for this app's login page.'''
        
        return reverse('login')

    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new Status Message.'''

        user = self.request.user
        profile = get_object_or_404(Profile, user=user)

        #call reverse to generate the URL for this Profile
        return reverse('show_profile', kwargs={'pk': profile.pk})
    
    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''

        context = super().get_context_data(**kwargs)

        user = self.request.user
        profiles = Profile.objects.filter(user=user)
        context['profile'] = profiles
        return context
    
    def form_valid(self, form):
        '''This method handles the form submission and saves the
        new object to the Django database.
        We need to add the foreign key (of the Profile) to the Status Message
        object before saving it to the database.'''

        print(form.cleaned_data)
        
        user = self.request.user

        profile = get_object_or_404(Profile, user=user)

        #attach this profile to the status message
        form.instance.profile = profile

        # save the status message to database
        sm = form.save()

        # read the file from the form:
        files = self.request.FILES.getlist('files')

        #for each file in files:
        for file in files:
            image = Image(image_file=file, profile=sm.profile)
            image.save()

            status_image = StatusImage(status_message=sm, image=image)
            status_image.save()

        #delegate the work to the superclass method form_valid:
        return super().form_valid(form)

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    '''View class to handle update of a profile based on its PK.'''

    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"

    def get_object(self):
        '''Get the Profile object associated with the logged-in user.'''
        try:
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            return redirect('create_profile')

    def get_login_url(self):
        '''Return the URL for this app's login page.'''
        
        return reverse('login')

class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    '''View class to delete a status message on a Profile.'''

    model = StatusMessage
    template_name = "mini_fb/delete_status_form.html"
    context_object_name = 'statusMessage'

    def get_login_url(self):
        '''Return the URL for this app's login page.'''
        
        return reverse('login')

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
    
class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    '''View class to update a Status Message on a Profile based on its PK.'''

    model = StatusMessage
    fields = ['message']
    template_name = "mini_fb/update_status_form.html"
    context_object_name = 'statusMessage'

    def get_login_url(self):
        '''Return the URL for this app's login page.'''
        
        return reverse('login')

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
    
class AddFriendView(LoginRequiredMixin, View):
    '''View class to trigger the add_friend method to occur.'''

    def get_object(self):
        '''Get the Profile object associated with the logged-in user.'''
        try:
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            return redirect('create_profile')

    def get_login_url(self):
        '''Return the URL for this app's login page.'''
        
        return reverse('login')

    def dispatch(self, request, *args, **kwargs):
        friend_pk = kwargs['other_pk']

        user_profile = get_object_or_404(Profile, user=request.user)
        friend_profile = get_object_or_404(Profile, pk=friend_pk)

        if user_profile == friend_profile:
            return redirect('show_profile', pk=user_profile.pk)

        try:
            user_profile.add_friend(friend_profile)
        except ValueError as e:
            print(f"Error: {e}")
            return redirect('show_profile', pk=user_profile.pk)

        return redirect('show_profile', pk=user_profile.pk)
    
class ShowFriendSuggestionsView(DetailView):
    '''Define a view class to show friend suggestions for a Profile page'''
    model = Profile
    template_name = "mini_fb/friend_suggestions.html"
    context_object_name = "profile"

    def get_object(self):
        '''Get the Profile object associated with the logged-in user.'''
        try:
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            return redirect('create_profile')

class ShowNewsFeedView(DetailView):
    '''Define a view class to display the news feed for a Profile.'''
    model = Profile
    template_name = "mini_fb/news_feed.html"
    context_object_name = "profile"

    def get_object(self):
        '''Get the Profile object associated with the logged-in user.'''
        try:
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            return redirect('create_profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #get the profile object
        profile = self.get_object()
        #get the news feed for this profile
        context['status_messages'] = profile.get_news_feed()
        return context
    
class LogoutConfirmationView(TemplateView):
    '''Define a view class to show a logout confirmation page'''
    model = Profile
    template_name = "mini_fb/logged_out.html"
    context_object_name = "profile"

class UserRegistrationView(CreateView):
    '''A view to show/process the registration form to create a new User.'''

    template_name = 'mini_fb/register.html'
    form_class = UserCreationForm
    model = User

    def get_success_url(self):
        '''The url to redirect to after creaating a new User.'''
        return reverse('login')