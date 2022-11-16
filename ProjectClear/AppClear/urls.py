from django.urls import path
from . import views

app_name = "AppClear"
urlpatterns = [
    path("", views.home, name="home"),
    path("specializations/<specialization_name>", views.specializations, name="specializations"),
    path("reserve_session/<adviser_id>/", views.reserve_session, name="reserve_session"),
    path("add_comment/<adviser_id>/", views.add_comment, name="add_comment"),
    path("add_like/<adviser_id>/", views.add_like, name="add_like"),
    path("unlike/<adviser_id>/", views.unlike, name="unlike"),
    path("delete/<adviser_id>/<comment_id>/", views.delete_comment, name="delete_comment"),
    path("profile/", views.view_profile, name="view_profile"),
    path("profile/update/", views.update_profile, name="update_profile"),
    path("adviser_profile/<adviser_id>/", views.adviser_profile, name="adviser_profile"),
    path("checkout/<adviser_id>/", views.checkout, name="checkout"),
    path("appointment/approve/<appointment_id>/", views.approved_appointment, name="approved_appointment"),
    path("appointment/reject/<appointment_id>/", views.reject_appointment, name="reject_appointment"),
    path("appointment/", views.appointment, name="appointment"),
    path("about/", views.about, name="about"),

]