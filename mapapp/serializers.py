

from dataclasses import fields
from rest_framework import serializers
import uuid
from django.db import models
# from django.contrib.auth.models import User
from .models import User


class LowerCaseEmailField(serializers.EmailField):
    def to_internal_value(self, data):
        return super().to_internal_value(data).lower()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password")


class UserAddressSerializer(serializers.ModelSerializer):
    user = UserSerializer

    class Meta:
        model = User
        fields = ("first_line", "second_line", "town_city", "postcode", "user")
