from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import Appointment, Comment , Like
from django.contrib.auth.models import User
from accounts.models import Profile

# Create your views here.

def home(request : HttpRequest):
    ''' Home Page Function'''

    if "search" in request.GET:
        advisers = Profile.objects.filter(user__first_name__contains=request.GET["search"] ,role="Adviser")
    else:
        advisers = Profile.objects.filter(role="Adviser")

    specializations = Profile.objects.all()
    return render(request, "AppClear/home.html", {'advisers': advisers , 'specializations' : specializations} )


def checkout(request : HttpRequest , adviser_id : int ):
    ''' Checkout Page Function to Reserve a session with an advisor '''
    adviser = User.objects.get(id=adviser_id)
    if request.method == "POST":
        appointment = Appointment.objects.create(user = request.user , adviser = adviser , appointment_date =request.POST["appointment_date"])
        appointment.save()
        
        return redirect("AppClear:home")
    else:
        return render(request, "AppClear/checkout.html" , {"adviser" : adviser })

def reserve_session(request : HttpRequest , adviser_id : int):
    ''' Reserve a Session Page Function'''
    try:
        user= User.objects.get(id=adviser_id)
        adviser = Profile.objects.get(user=user)
        comments = Comment.objects.filter(adviser=adviser_id)
        likes = Like.objects.filter(liked_user=user);
        liked = False


        if not (request.user.is_authenticated and request.user.has_perm("AppClear.add_like")):
            liked_before = Like.objects.filter(liked_user=user)
            liked = False
        else:
            liked_before = Like.objects.filter(user=request.user, liked_user=user)
            if len(liked_before) > 0:
                liked = True
    except:
        return render(request , "AppClear/not_found.html")
    return render(request, "AppClear/reserve_session.html" ,  {"adviser" : adviser, "comments" : comments ,"likes":likes, "liked":liked})


def add_comment(request : HttpRequest , adviser_id : int):
    ''' Add Comment on Adviser Function'''
    user : User = request.user

    if not (user.is_authenticated and user.has_perm("AppClear.add_comment")):
        return redirect("accounts:login_user")

    if request.method == "POST":
        adviser = User.objects.get(id=adviser_id)
        comment = Comment(adviser=adviser,user=request.user, content= request.POST['content'])
        comment.save()
    return redirect("AppClear:reserve_session", adviser_id)


def add_like(request : HttpRequest , adviser_id : int):
    ''' Like an Adviser Function'''
    user : User = request.user

    if not (request.user.is_authenticated and request.user.has_perm("AppClear.add_like")):
        return redirect("accounts:login_user")

    adviser = User.objects.get(id=adviser_id)
    liked_before = Like.objects.filter(user=request.user,liked_user=adviser)
    if(len(liked_before) == 0):
        new_like = Like(user=user, liked_user=adviser)
        new_like.save()

    return redirect("AppClear:reserve_session", adviser_id)

def unlike(request : HttpRequest , adviser_id : int):
    ''' Like an Adviser Function'''
    user : User = request.user

    if not user.is_authenticated:
        return redirect("accounts:login_user")

    adviser = User.objects.get(id=adviser_id)
    liked_before = Like.objects.filter(user=request.user, liked_user=adviser)
    if (len(liked_before) > 0):
        liked_before.delete();

    return redirect("AppClear:reserve_session", adviser_id)



def delete_comment(request: HttpRequest, comment_id : int , adviser_id : int):
        '''Delete Comment Function '''
        try:
            comment = Comment.objects.get(id=comment_id)
            if comment.user == request.user:
                comment.delete()
        except:
            return render(request , "AppClear/not_found.html")

        return redirect("AppClear:reserve_session", adviser_id)


def view_profile(request : HttpRequest):
    ''' View Profile Function '''
    return render(request, "AppClear/view_profile.html", {"user" : request.user})

def update_profile(request : HttpRequest):
    ''' Update Profile Function '''
    return render(request, "AppClear/update_profile.html", {"user" : request.user})

def specializations(request : HttpRequest , specialization_name):
    ''' Search by specializations Function '''
    advisers = Profile.objects.filter(role="Adviser" ,specialization=specialization_name )
    return render(request, "AppClear/specializations.html", {'advisers': advisers, 'specialization': specialization_name})


def adviser_profile(request : HttpRequest ,adviser_id : int):
    ''' View an adviser profile Function '''
    user= User.objects.get(id=adviser_id)
    adviser = Profile.objects.get(user=user)
    return render(request, "AppClear/adviser_profile.html", {"adviser" : adviser})

def appointment(request : HttpRequest):
    ''' Appointment Function to List appointments '''
    if request.user.profile.role == Profile.user_type_choices.Adviser:
        pending_appointments = Appointment.objects.filter(adviser=request.user , status="Pending")
        Approved_appointments = Appointment.objects.filter(adviser=request.user , status="Approved")
        return render(request, "AppClear/appointment.html", {"pending_appointments" : pending_appointments , "Approved_appointments" : Approved_appointments})
    else:
        appointments = Appointment.objects.filter(user=request.user)
        return render(request, "AppClear/user_appointment.html", {  "appointments" : appointments})

def approved_appointment(request : HttpRequest , appointment_id : int):
    ''' Approved Appointment for Advisor Function '''
    if request.method == "POST":
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.status =  "Approved"
        appointment.save()
        return redirect("AppClear:appointment")

def reject_appointment(request : HttpRequest , appointment_id : int):
    '''Reject Appointment for Advisor'''
    if request.method == "POST":
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.status =  "Rejected"
        appointment.save()
        return redirect("AppClear:appointment")

def about(request : HttpRequest):
    ''' About Page Function '''
    return render(request, "AppClear/about.html")
