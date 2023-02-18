from django.urls import re_path
from services import views
urlpatterns = [
        re_path(r'^platform-services-list/$', views.PlatformServiceList.as_view(),
            name=views.PlatformServiceList.name),
        re_path(r'^platform-list/$', views.PlatformList.as_view(),
            name=views.PlatformList.name),
        re_path(r'^faqs/$', views.FAQList.as_view(),
            name=views.FAQList.name),
        re_path(r'^order-status/$', views.OrderStatus.as_view(),
            name=views.OrderStatus.name)
        ]