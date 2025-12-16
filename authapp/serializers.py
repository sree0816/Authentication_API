from authapp.models import User
from rest_framework import serializers

class User_serializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','name','email','password']

