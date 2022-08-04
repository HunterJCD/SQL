from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from re import M
from django import urls
from django.shortcuts import render
from markdown2 import Markdown
from django import forms 
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse 
import random 
import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


from .models import User, Listing

class NewListingForm(forms.Form):
    listing_name = forms.CharField(label="New Listing")
    starting_bid = forms.IntegerField()
    listing_description = forms.CharField(widget=forms.Textarea())

def createnewlisting(request):
    if request.method == "POST":
        entry = NewListingForm(request.POST)
        if entry.is_valid():
            listing_name = entry.cleaned_data["listing_name"]
            starting_bid = entry.cleaned_data["starting_bid"]
            listing_description = entry.cleaned_data["listing_description"]
            listing = Listing(listing_name, starting_bid, listing_description)
            listing.save()
            
        return render(request, "auctions/createnewlisting.html", {
            "newlisting": entry
        })
    return render(request, "auctions/createnewlisting.html")
    


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })




def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
