# voter_analytics/models.py
# Made by Annelise Schreiber, aschreib@bu.edu
# Friday, April 4, 2025
# Description: making/defining the Profile model for voter_analytics application

from django.db import models
from datetime import datetime

# Create your models here.
class Voter(models.Model):
    '''
    Store/represent the data from registered voters from Newton, MA.
    Last Name, First Name, Residential Address - Street Number
    Residential Address - Street Name, Residential Address - Apartment Number
    Residential Address - Zip Code, Date of Birth, Date of Registration
    Party Affiliation (**note, this is a 2-character wide field**), Precinct Number
    '''
    # identification
    first_name = models.TextField()
    last_name = models.TextField()
    street_num = models.IntegerField()
    street_name = models.TextField()
    apt_num = models.TextField(max_length=50, blank=True, null=True)
    zip_code = models.IntegerField()
    dob = models.DateField()
    date_registration = models.DateField()
    party_aff = models.CharField(max_length=2)
    precinct_num = models.TextField()

    # how many of recent elections they voted in
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)

    # indicating how many of the past 5 elections the voter participated in
    voter_score = models.IntegerField(default=0)


    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name}'

def load_data():
    '''Function to load data records from CSV file into the Django database.'''

    # very dangerous line!
    Voter.objects.all().delete()

    filename = 'C:/Users/annel/django/newton_voters.csv'

    f = open(filename, 'r') #open the file for reading

    #discard headers:
    f.readline() #do nothing with it

    # read the entire file, one line at a time
    for line in f:
        
        fields = line.split(',')
        
        try:
            result = Voter(first_name = fields[2],
                            last_name = fields[1],
                            street_num = fields[3],
                            street_name = fields[4],
                            apt_num = fields[5],
                            zip_code = fields[6],
                            dob = datetime.strptime(fields[7], "%Y-%m-%d").date(),
                            date_registration = datetime.strptime(fields[8], "%Y-%m-%d").date(),
                            party_aff = fields[9],
                            precinct_num = fields[10],
                            v20state = fields[11].strip().upper() == 'TRUE',
                            v21town = fields[12].strip().upper() == 'TRUE',
                            v21primary = fields[13].strip().upper() == 'TRUE',
                            v22general = fields[14].strip().upper() == 'TRUE',
                            v23town = fields[15].strip().upper() == 'TRUE',
                            voter_score = int(fields[16]))
            result.save() #commit this result to the database
            # print(f'Created result: {result}')
        
        except Exception as e:
            print(f"Error processing line: {line}")
            print(f"Error details: {e}")

    print(f"Done. Created {len(Voter.objects.all())} Results")
