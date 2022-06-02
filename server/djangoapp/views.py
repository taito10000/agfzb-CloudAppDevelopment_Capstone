from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_request, get_dealer_by_id_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
import requests
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):

    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')


# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')


# Create a `registration_request` view to handle sign up request

def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html')

    elif request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
    
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp:registration', context)




# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://608f2dc9.us-south.apigw.appdomain.cloud/ibmcapstone/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        dealers = []
        for d in dealerships: 
            obj = CarDealer(d.address,d.city, d.full_name, d.id, d.lat, d.long, d.short_name, d.st, d.zip)
            dealers.append(obj)
        context['dealers'] = dealers
        # Concat all dealer's short name
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        #return HttpResponse(dealer_names)
        return render(request, 'djangoapp/index.html', context)




# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    url = "https://608f2dc9.us-south.apigw.appdomain.cloud/ibmcapstone/dealer"
    context = {}
    reviews = get_dealer_reviews_from_cf(url, dealer_id)
    print(dealer_id)
    print(reviews)
    context['reviews'] = reviews
    return render(request, 'djangoapp/dealer_details.html', context)
# Create a `add_review` view to submit a review




def add_review(request, dealer_id):

    context = {}
    if request.user.is_authenticated:
        url = "https://608f2dc9.us-south.apigw.appdomain.cloud/ibmcapstone/review"
        review = {
            'time': datetime.utcnow().isoformat(),
            'dealership': dealer_id,
            'review': "Test review"
        }
        
        json_payload = {
            'review': review
        }
        
        resp = post_request(url, json_payload, dealerId=dealer_id)
        print(resp.json())
        print(request.user)
        return render(request, 'djangoapp/add_review.html', context)
    
    
    else:
        print("NO USER")
        return render(request,'djangoapp/index.html', context)
    #if user:
    #    print("Auth ok!")
    #else: 
    #    print("Auth not ok")
    