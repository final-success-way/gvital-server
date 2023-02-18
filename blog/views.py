from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from django_filters import rest_framework as filters

from blog.models import Post
from blog.serializers import PostsSerializer


class GetPosts(generics.ListAPIView):
    name = 'get-posts'
    queryset = Post.objects.all()
    serializer_class = PostsSerializer
    filterset_fields = ['slug', 'author']

    def get_queryset(self):
        print(self.request.query_params)
        queryset = Post.objects.all()
        return queryset
