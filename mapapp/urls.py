from django.urls import re_path, path
from .views import ListView, save_users_home

urlpatterns = [
    path(r"save_details", save_users_home, name="save users details"),
    re_path(r"^(?P<api_name>[a-z]+)", ListView, name='user-objects'),
]
