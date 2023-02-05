from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('events/', views.event_list, name="event_list"),
    
    # login / logout urls
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    
    # events urls
    path('tag/<slug:tag_slug>/', views.event_list, name="event_list_by_tag"),
    path('event/<int:id>', views.event_detail, name="event_detail"),
]
