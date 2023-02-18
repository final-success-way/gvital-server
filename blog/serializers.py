from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from blog.models import *


class PostsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        exclude = ['active']
        depth = 1
