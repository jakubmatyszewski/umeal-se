from django.urls import path, include
from . import views


urlpatterns = [
    # auth urls
    path('', include('django.contrib.auth.urls')),
    path('register', views.register, name='register'),
    path('profile/edit', views.edit_profile, name='edit_profile'),

    # umealse
    path('', views.landing_page, name="landing_page"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('events/', views.event_list, name="event_list"),

    # events urls
    path('tag/<slug:tag_slug>/', views.event_list, name="event_list_by_tag"),
    path('event/<int:id>', views.event_detail, name="event_detail"),
]
