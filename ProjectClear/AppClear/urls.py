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
    path("checkout/", views.checkout, name="checkout"),
]