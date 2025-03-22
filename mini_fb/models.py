# mini_fb/models.py
# Made by Annelise Schreiber, aschreib@bu.edu
# Friday, February 21, 2025
# Description: making/defining the Profile model for mini_fb application

from django.db import models
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    '''Encapsulate the data of a profile on a mini_fb app.'''

    #define the data attributes of the Profile object
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    city = models.TextField(blank=True)
    email_address = models.TextField(blank=True)
    #profile_image_url = models.URLField(blank=True)
    #published = models.DateTimeField(auto_now=True)
    image_file = models.ImageField(blank=True) #an actual image

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name}'
    
    def get_absolute_url(self):
        '''Return a URL to display one instance of this object.'''
        return reverse('show_profile', kwargs={'pk':self.pk})
    
    def get_status_messages(self):
        '''Return a QuerySet of status messages for this profile.'''
        #use the object manager to retrieve comments about this article
        statusMessages = StatusMessage.objects.filter(profile=self)
        return statusMessages
    
    def get_friends(self):
        '''Return a list of the friends' Profiles.'''
        #use the object manager to filter/retrieve matching Friend records
        friends = Friend.objects.filter(profile1=self) | Friend.objects.filter(profile2=self)

        friend_profiles = []
        for friend in friends:
            if friend.profile1 != self:
                friend_profiles.append(friend.profile1)
            elif friend.profile2 != self:
                friend_profiles.append(friend.profile2)

        return friend_profiles
    
    def add_friend(self, other):
        '''Add a Friend relation for two Profiles: self and other.'''
        #using Friend model to create a friendship between two unique profiles that doesn't already exist
        if self == other:
            raise ValueError("Can't add yourself as a friend.")

        existing_friendship = (Friend.objects.filter(profile1=self, profile2=other) | 
        Friend.objects.filter(profile1=other, profile2=self)).exists()

        if existing_friendship:
            print("This friendship already exists.")
            return

        new_friend = Friend(profile1=self, profile2=other)
        new_friend.save()
        print(f"Friendship between {self} and {other} created.")

    def get_friend_suggestions(self):
        '''Getting recommended friend Profiles.'''
        potential_friends = Profile.objects.exclude(pk=self.pk)
        already_friends = self.get_friends()
        already_friends_ids = [friend.pk for friend in already_friends]
        potential_friends = potential_friends.exclude(pk__in=already_friends_ids)

        return potential_friends
    
    def get_news_feed(self):
        ''' Return all StatusMessages for the profile on which the method was called, as well
        as all of the friends of that profile.'''
        friends = self.get_friends()
        status_messages = (StatusMessage.objects.filter(profile=self) | 
                        StatusMessage.objects.filter(profile__in=friends)).order_by('-timestamp')
        
        return status_messages

    
class StatusMessage(models.Model):
    '''Model the attributes of the Facebook status message'''

    #define the data attributes of the StatusMessage object:
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE) # cascade --> can't have status w/o profile

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.message}'
    
    def get_images(self):
        '''Method to find all Images that are related to a StatusMessage, and then return a
        list or QuerySetof those Image(s).'''
        return Image.objects.filter(statusimage__status_message_id=self.id)


class Image(models.Model):
    '''Model for encapsulating the idea of an image file (not a URL) that is 
    stored in the Django media directory and some meta-data about that image file.'''

    #defining the data attributes of the Image object:
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='images/')
    timestamp = models.DateTimeField(auto_now=True)
    caption = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f"Image uploaded at {self.timestamp}"


class StatusImage(models.Model):
    '''Model for providing a way to find Images that relate to a StatusMessage,
    and vice versa, to find the StatusMessage to which an Image is related.'''

    #defining the data attributes of the StatusImage object:
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE, related_name='status_images')

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f"Image {self.image.id} linked to StatusMessage {self.status_message.id}"
    
class Friend(models.Model):
    '''Model for encapsulating the idea of an edge connecting two nodes within the 
    social network (e.g., two Profiles that are friends with each other).'''

    #defining the data attributes of the Friend object:
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile1')
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile2')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''Reutrn a string representation of this model instance.'''
        return f"{self.profile1} & {self.profile2}"