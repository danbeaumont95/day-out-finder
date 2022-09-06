from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import User, UserAddress, UserLoginTokens
from .serializers import UserSerializer, UserAddressSerializer, UserLoginSerializer
from operator import itemgetter
from collections import namedtuple
from django.contrib.auth.hashers import make_password, check_password
from .helpers import signJWT

nt = namedtuple("object", ["model", "serializers"])
pattern = {
    "user": nt(User, UserSerializer),
    "address": nt(UserAddress, UserAddressSerializer),
    "login": nt(UserLoginTokens, UserLoginSerializer)
}


@api_view(["GET", "POST"])
def ListView(request, api_name):
    object = pattern.get(api_name, None)

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
        serializers = object.serializers(data=data)
        if api_name == 'user':
            first_name, last_name, email, password = itemgetter(
                'first_name', 'last_name', 'email', 'password')(request.data)
            hashed_password = make_password(password)

            # first is password to check (req.body.password), 2nd is password in db
            # check = check_password(password, hashed_password)

            new_user = User.objects.create(
                first_name=first_name, last_name=last_name, email=email, password=hashed_password)
            new_user.save()
            return Response({'Success': 'New user created'})
        if api_name == 'address':
            print('called123')
            bearer_token = request.headers.get('authorization')

            if bearer_token is None:
                return Response({'Error': 'Bearer Token required'})
            slice = bearer_token[7:]

            user_token = UserLoginTokens.objects.filter(
                access_token=slice).count()
            print(user_token, 'user_token321')
            if user_token == 0 or user_token < 1:
                return Response({'Error': 'No user found'})
            att = UserLoginTokens.objects.filter(
                access_token=slice).values('user_id').first()
            print(att, 'att123')
            user = User.objects.filter(id=att['user_id']).first()
            print(user, 'fuckinguser')
            first_line, second_line, town_city, postcode = itemgetter(
                'first_line', 'second_line', 'town_city', 'postcode'
            )(request.data)

            print(first_line, 'first_line123')
            try:

                created_address = UserAddress.objects.create(
                    first_line=first_line, second_line=second_line, town_city=town_city, postcode=postcode, user=user)
                print(created_address, 'created_address123')
                created_address.save()
                return Response({'Success': 'Address saved'})
            except:
                return Response({'Error': 'Unable to save address'})
            # print(created_address, 'created_address1234')
        if api_name == 'login':
            print(request.data, 'request.data123')
            user = User.objects.filter(email=request.data['username'])

            if not user:
                return Response({'Error': 'No user found with those details'})

            hashed_password = user[0].password
            user_id = user[0].id

            check = check_password(request.data['password'], hashed_password)
            print(check, 'check123')

            if check == False:
                return Response({'Error': 'No user found with those details'})

            token = signJWT(user_id)

            access_token = token['access_token']
            refresh_token = token['refresh_token']

            saved_token = UserLoginTokens.objects.create(
                access_token=access_token, refresh_token=refresh_token, user_id=user_id
            )
            saved_token.save()
            return Response({
                'access': access_token,
                'refresh': refresh_token,
                'id': user_id
            })

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
