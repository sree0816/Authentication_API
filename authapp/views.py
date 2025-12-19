from http.client import responses

from django.shortcuts import render
from authapp.models import User
from authapp.serializers import User_serializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
import datetime,jwt

# Create your views here.

class RegisterAPI(APIView):
    def post(self,request):
        obj=User_serializer(data=request.data)
        obj.is_valid(raise_exception=True)
        obj.save()
        return Response(obj.data)
class LoginAPI(APIView):
    def post(self,request):
        email=request.data['email']
        pswd=request.data['password']
        #tries to find the user with follwing  credentials in the User DB
        #  first() returns the first matching user
        x=User.objects.filter(email=email).first()
        if x is None:
            raise AuthenticationFailed('User not found..')
        if not x.check_password(pswd):
#In Django, check_password is used to verify whether a plain-text password matches a hashed password stored in the database.
            raise AuthenticationFailed(' invalid password')
        payload={'id':x.id,'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60),'iat':datetime.datetime.utcnow()
        }

        #returns the current date and time in utc (cordinated universal time)
        # iat means issued at ,timestamp at which the token is created
        token=jwt.encode(payload,'secret',algorithm='HS256')
        response=Response()
        response.set_cookie(key='jwt',value=token,httponly=True)
        response.data={"your token :":token}

        return response

class userview(APIView):
    def get(self,request):
        token=request.COOKIES.get('jwt')
        if not token :
            raise AuthenticationFailed("unauthorised..")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("unauthorised...")

        user=User.objects.filter(id=payload['id']).first()
        obj=User_serializer(user)
        return Response(obj.data)

class Logout(APIView):
    def post(self,request):
        response=Response()
        response.delete_cookie('jwt')
        response.data={
            "logout":"success"
        }
        return response



