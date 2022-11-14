from django.urls import path
from . import views

app_name = "AppClear"
urlpatterns = [
    path("", views.home, name="home"),
    path("reserve_session/<adviser_id>/", views.reserve_session, name="reserve_session"),
    path("add_comment/<adviser_id>/", views.add_comment, name="add_comment"),
    path("add_like/<adviser_id>/", views.add_comment, name="add_comment"),

    path("checkout/", views.checkout, name="checkout"),
    
    
]