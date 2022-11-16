from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login, logout
from .models import Profile
from django.contrib.auth.decorators import login_required

# Create your views here.

def register_user(request : HttpRequest):
    ''' Register User Function '''

    if request.user.is_authenticated:
        return redirect("AppClear:home")
    if request.method == "POST":
        #creating the user
        new_user = User.objects.create_user(username=request.POST["username"], email= request.POST["email"], first_name=request.POST["first_name"], last_name=request.POST["last_name"], password=request.POST["password"]   )
        new_user.save()
        #creating the Profile
        if request.POST.get("role") == Profile.user_type_choices.Adviser:
            profile = Profile( user=new_user , image= request.FILES["image"], age= request.POST["age"], role = request.POST["role"], specialization= request.POST["specialization"] , session_salary=request.POST.get("session_salary", 0.0), description=request.POST["description"] , cv= request.FILES["cv"]  )
        else:
            profile = Profile(user=new_user , image= request.FILES["image"], age= request.POST["age"], role = request.POST["role"], specialization= request.POST["specialization"] , description=request.POST["description"])
        profile.save()

    
    return render(request, "accounts/register.html")


def login_user(request : HttpRequest):
    ''' Login User Function '''
    if request.user.is_authenticated:
        return redirect("AppClear:home")
    msg = ""
    if request.method == "POST":
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        
        if user:
            login(request, user)
            return redirect("AppClear:home")
        else:
            msg = "User Not Found , check your credentials"

    return render(request, "accounts/login.html", {"msg" : msg})


def logout_user(request: HttpRequest):
    ''' Logout User Function '''
    logout(request)

    return redirect("AppClear:home")

@login_required(login_url="login/")
def update_profile(request : HttpRequest , user_id : int):
    ''' Update User Profile Function '''
    # user_id : User= request.user

    user = User.objects.get(id= user_id)
    profile = Profile.objects.get(user=user)
    if request.method == "POST":
        if request.POST.get("role") == Profile.user_type_choices.Adviser:
            user.first_name=request.POST["first_name"]
            user.last_name=request.POST["last_name"]
            user.username=request.POST["username"]
            user.email=request.POST["email"]
            profile.age= request.POST["age"]
            profile.session_salary=request.POST.get("session_salary", 0.0) 
            profile.description=request.POST["description"]
            profile.cv= request.FILES["cv"]
            user.save()
            profile.save() 
        else:
            user.first_name=request.POST["first_name"]
            user.last_name=request.POST["last_name"]
            user.username=request.POST["username"]
            user.email=request.POST["email"]
            profile.age= request.POST["age"]
            profile.description=request.POST["description"]
            user.save()
            profile.save()

    
    return render(request, "AppClear/update_profile.html", {"user" : user})
