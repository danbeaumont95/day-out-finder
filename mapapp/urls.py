from django.urls import re_path, path
from .views import ListView, save_users_home, get_my_addresses, get_me, get_my_saved_addresses

urlpatterns = [
    path(r"save_details", save_users_home, name="save users details"),
    path(r"get_my_addresses", get_my_addresses, name="get my addresses"),
    path(r"get_me", get_me, name="get me"),
    path(r"get_my_saved_addresses", get_my_saved_addresses,
         name="get my saved addresses"),
    re_path(r"^(?P<api_name>[a-z]+)", ListView, name='user-objects'),
]
