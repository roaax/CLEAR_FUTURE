from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import Appointment, Comment , Like
from django.contrib.auth.models import User
from accounts.models import Profile

# Create your views here.

def home(request : HttpRequest):
    ''' Home Page Function'''
    #advisers = User.objects.all()
    
    advisers = Profile.objects.filter(role="Adviser")
    return render(request, "AppClear/home.html", {'advisers': advisers} )


def checkout(request : HttpRequest):
    ''' Checkout Page Function'''
    return render(request, "AppClear/checkout.html" )

