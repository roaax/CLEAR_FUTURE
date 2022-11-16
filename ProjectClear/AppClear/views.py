from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import Appointment, Comment , Like
from django.contrib.auth.models import User
from accounts.models import Profile
import jwt
import requests
import json
from time import time
from dotenv import load_dotenv
import os

load_dotenv()

# ------------HOME PAGE----------------
def home(request : HttpRequest):
    ''' Home Page Function'''
    if "search" in request.GET:
        advisers = Profile.objects.filter(user__first_name__contains=request.GET["search"] ,role="Adviser")
    else:
        advisers = Profile.objects.filter(role="Adviser")

    specializations = Profile.objects.all()
    return render(request, "AppClear/home.html", {'advisers': advisers , 'specializations' : specializations} )

# ------------CHECKOUT PAGE----------------
def checkout(request : HttpRequest , adviser_id : int ):
    ''' Checkout Page Function to Reserve a session with an advisor '''
    adviser = User.objects.get(id=adviser_id)
    if not request.user.profile.role == Profile.user_type_choices.Adviser:
        if request.method == "POST":
            appointment = Appointment.objects.create(user = request.user , adviser = adviser , appointment_date =request.POST["appointment_date"])
            appointment.save()
            
            return redirect("AppClear:home")
        else:
            return render(request, "AppClear/checkout.html" , {"adviser" : adviser })
    return redirect("AppClear:home")

# ------------RESERVE SESSION PAGE----------------
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

# ------------ADD COMMENT TO ADVISOR----------------
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

# ------------ADD LIKE TO AN ADVISOR----------------
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

# ------------UNLIKE AN ADVISOR----------------
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


# ------------DELETE YOUR COMMENT ON ADVISOR----------------
def delete_comment(request: HttpRequest, comment_id : int , adviser_id : int):
        '''Delete Comment Function '''
        try:
            comment = Comment.objects.get(id=comment_id)
            if comment.user == request.user:
                comment.delete()
        except:
            return render(request , "AppClear/not_found.html")

        return redirect("AppClear:reserve_session", adviser_id)

# ------------VIEW YOUR PROFILE----------------
def view_profile(request : HttpRequest):
    ''' View Profile Function '''
    return render(request, "AppClear/view_profile.html", {"user" : request.user})

# ------------UPDATE YOUR PROFILE----------------
def update_profile(request : HttpRequest):
    ''' Update Profile Function '''
    return render(request, "AppClear/update_profile.html", {"user" : request.user})


# ------------SEARCH BY SPECIALIZATION----------------
def specializations(request : HttpRequest , specialization_name):
    ''' Search by specializations Function '''
    advisers = Profile.objects.filter(role="Adviser" ,specialization=specialization_name )
    return render(request, "AppClear/specializations.html", {'advisers': advisers, 'specialization': specialization_name})

# ------------VIEW SPECIFIC ADVISOR PROFIL----------------
def adviser_profile(request : HttpRequest ,adviser_id : int):
    ''' View an adviser profile Function '''
    user= User.objects.get(id=adviser_id)
    adviser = Profile.objects.get(user=user)
    return render(request, "AppClear/adviser_profile.html", {"adviser" : adviser})

# ------------LIST APPOINTMENT PAGE----------------
def appointment(request : HttpRequest):
    ''' Appointment Function to List appointments '''
    if request.user.profile.role == Profile.user_type_choices.Adviser:
        pending_appointments = Appointment.objects.filter(adviser=request.user , status="Pending")
        Approved_appointments = Appointment.objects.filter(adviser=request.user , status="Approved")
        return render(request, "AppClear/appointment.html", {"pending_appointments" : pending_appointments , "Approved_appointments" : Approved_appointments})
    else:
        appointments = Appointment.objects.filter(user=request.user)
        return render(request, "AppClear/user_appointment.html", {  "appointments" : appointments})

# ------------APPROVE APPOINTMENT FROM ADVISOR SIDE----------------
def approved_appointment(request : HttpRequest , appointment_id : int):
    ''' Approved Appointment for Advisor Function '''
    if request.method == "POST":
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.status =  "Approved"
        appointment.save()
        createMeeting(appointment)
        return redirect("AppClear:appointment")
        
# ------------REJECT APPOINTMENT FROM ADVISOR SIDE----------------
def reject_appointment(request : HttpRequest , appointment_id : int):
    '''Reject Appointment for Advisor'''
    if request.method == "POST":
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.status =  "Rejected"
        appointment.save()
        return redirect("AppClear:appointment")

# ------------ABOUT PAGE----------------
def about(request : HttpRequest):
    ''' About Page Function '''
    return render(request, "AppClear/about.html")


# -------------Zoom API ----------------


# create a function to generate a token
# using the pyjwt library

def generateToken():
	token = jwt.encode(

		# Create a payload of the token containing
		# API Key & expiration time
		{'iss': os.getenv('API_KEY'), 'exp': time() + 5000},

		# Secret used to generate token signature
		os.getenv('API_SEC'),

		# Specify the hashing alg
		algorithm='HS256'
	)
	return token


# send a request with headers including
# a token and meeting details


def createMeeting(appointment):

    # create json data for post requests
    meetingdetails = {"topic": "Zoom Meeting for Appointment Number " + str(appointment.id),
                    "type": 2,
                    "start_time": str(appointment.appointment_date),
                    "duration": "45",
                    "timezone": "Europe/Madrid",
                    "agenda": "test",

                    "recurrence": {"type": 1,
                                    "repeat_interval": 1
                                    },
                    "settings": {"host_video": "true",
                                "participant_video": "true",
                                "join_before_host": "False",
                                "mute_upon_entry": "False",
                                "watermark": "true",
                                "audio": "voip",
                                "auto_recording": "cloud"
                                }
                    }

    headers = {'authorization': 'Bearer ' + generateToken(),
            'content-type': 'application/json'}
    r = requests.post(
        f'https://api.zoom.us/v2/users/me/meetings',
        headers=headers, data=json.dumps(meetingdetails))

    # print(r.text)
    # converting the output into json and extracting the details
    y = json.loads(r.text)
    join_URL = y["join_url"]
    meetingPassword = y["password"]
    appointment.url=join_URL
    appointment.meeting_pwd = meetingPassword
    appointment.save()


