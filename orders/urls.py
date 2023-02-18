from django.urls import re_path
from orders import views
urlpatterns = [
        re_path(r'^create-order/$', views.CreateOrder.as_view(),
            name=views.CreateOrder.name),
        re_path(r'^repeat-order/$', views.RepeatOrder.as_view(),
            name=views.RepeatOrder.name),
        re_path(r'^get-orders/$', views.GetOrders.as_view(),
            name=views.GetOrders.name),
        ]