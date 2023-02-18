from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import *
from rest_framework.response import Response
from accounts.models import *



class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        exclude=['created_at','updated_at','id','uid','active','city','gender','is_email_verified',
                 'flags','user']



class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    class Meta:
        model = User
        exclude = ['groups','user_permissions','password','last_login','is_superuser','username','first_name','last_name',
                   'email','is_staff','is_active','date_joined']

