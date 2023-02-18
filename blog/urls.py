from django.urls import re_path
from blog import views
urlpatterns = [
        re_path(r'^posts/$', views.GetPosts.as_view(),
            name=views.GetPosts.name),
        ]