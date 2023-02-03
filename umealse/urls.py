from django.urls import path
from . import views


app_name = 'umealse'

urlpatterns = [
    path('', views.event_list, name="event_list"),
    path('event/<int:id>', views.event_detail, name="event_detail"),
]