from django.urls import path, include
from . import views


urlpatterns = [
    # auth urls
    path("", include("django.contrib.auth.urls")),
    path("register", views.register, name="register"),
    path("profile/edit", views.edit_profile, name="edit_profile"),
    # umealse
    path("", views.landing_page, name="landing_page"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/<str:username>", views.show_profile, name="profile"),
    path(
        "add_friend/<int:userID>", views.send_friend_request, name="send_friend_request"
    ),
    path(
        "accept_friend/<int:requestID>",
        views.accept_friend_request,
        name="accept_friend_request",
    ),
    path(
        "reject_friend/<int:requestID>",
        views.reject_friend_request,
        name="reject_friend_request",
    ),
    path("delete_friend/<int:userID>", views.delete_friend, name="delete_friend"),
    # events urls
    path("events/", views.event_list, name="event_list"),
    path("tag/<slug:tag_slug>/", views.event_list, name="event_list_by_tag"),
    path("event/<int:id>", views.event_detail, name="event_detail"),
]
