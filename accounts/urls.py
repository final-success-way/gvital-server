import socket

from django.urls import re_path
from accounts import views

urlpatterns = [
        re_path(r'^super/$', views.admin_login,
            name='Admin Login'),
        re_path(r'^login/$', views.LoginUser.as_view(),
            name=views.LoginUser.name),
        re_path(r'^register/$', views.RegisterUser.as_view(),
            name=views.RegisterUser.name),
        re_path(r'^profile-info/$', views.ProfileInfo.as_view(),
            name=views.ProfileInfo.name),
        re_path(r'^change-email/$', views.ChangeEmail.as_view(),
            name=views.ChangeEmail.name),
        re_path(r'^reset-password/$', views.ResetPassword.as_view(),
            name=views.ResetPassword.name),
        re_path(r'^password-reset/$', views.VerifyToken.as_view(),
            name=views.VerifyToken.name),
        re_path(r'^user/$', views.GetUserInfo.as_view(),
            name=views.GetUserInfo.name),
        re_path(r'^change-password/$', views.ChangePassword.as_view(),
            name=views.ChangePassword.name),
        re_path(r'^change-user-password/$', views.ChangeUserPassword.as_view(),
            name=views.ChangeUserPassword.name)
        ]