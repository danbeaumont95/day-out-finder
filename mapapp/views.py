from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import User, UserAddress
from .serializers import UserSerializer, UserAddressSerializer
from operator import itemgetter
from collections import namedtuple
from django.contrib.auth.hashers import make_password, check_password

nt = namedtuple("object", ["model", "serializers"])
pattern = {
    "user": nt(User, UserSerializer),
    "user_address": nt(UserAddress, UserAddressSerializer),

}


@api_view(["GET", "POST"])
def ListView(request, api_name):
    print(api_name, 'api_name')
    object = pattern.get(api_name, None)
    print(object, 'object123')
    print(str(object.model), 'model123')
    # if api_name == 'user':
    #     print('user123')

    if object == None:
        return Response(
            data="Invalid URL",
            status=status.HTTP_404_NOT_FOUND,
        )
    if request.method == "GET":
        object_list = object.model.objects.all()
        serializers = object.serializers(object_list, many=True)
        return Response(serializers.data)

    if request.method == "POST":
        data = request.data
        print(data, 'data123')
        serializers = object.serializers(data=data)
        if api_name == 'user':
            first_name, last_name, email, password = itemgetter(
                'first_name', 'last_name', 'email', 'password')(request.data)
            hashed_password = make_password(password)

            # first is password to check (req.body.password), 2nd is password in db
            # check = check_password(password, hashed_password)
            print('got here 1')
            new_user = User.objects.create(
                first_name=first_name, last_name=last_name, email=email, password=hashed_password)
            new_user.save()
            return Response({'Success': 'New user created'})

        if not serializers.is_valid():
            return Response(
                data=serializers.error,
                status=status.HTTP_404_NOT_FOUND
            )
        serializers.save()
        return Response(
            data=serializers.error,
            status=status.HTTP_201_CREATED
        )
