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
    specializations = Profile.objects.filter(role="specialization")
    return render(request, "AppClear/home.html", {'advisers': advisers , 'specializations' : specializations} )


def checkout(request : HttpRequest):
    ''' Checkout Page Function'''
    return render(request, "AppClear/checkout.html" )

def reserve_session(request : HttpRequest , adviser_id : int):
    ''' Reserve a Session Page Function'''
    
    try:
        user= User.objects.get(id=adviser_id)
        adviser = Profile.objects.get(user=user)
        comments = Comment.objects.filter(user= user)
        liked_before = Like.objects.filter(user= request.user, liked_user=user).exists()
        if request.method == 'POST':
            add_comment(request , user)
        if not liked_before:
            add_like(request , user)
    except:
        return render(request , "AppClear/not_found.html")

    likes = Like.objects.filter(liked_user=user)

    return render(request, "AppClear/reserve_session.html" ,  {"adviser" : adviser, "comments" : comments , "likes":likes})


def add_comment(request : HttpRequest , adviser : User):
    ''' Add Comment on Adviser Function'''
    comment = Comment(user=adviser, content= request.POST['content'])
    print(request.user)
    comment.save()


def add_like(request : HttpRequest , adviser : User):
    ''' Like an Adviser Function'''
    new_like = Like(user = request.user, liked_user=adviser)
    new_like.save()
