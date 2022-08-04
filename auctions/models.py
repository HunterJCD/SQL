from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    listing_name = models.CharField(max_length=64)
    starting_bid = models.FloatField()
    listing_description = models.CharField(max_length=240)
   
    def __str__(self):
       return f"{self.listing_name}"
    
   