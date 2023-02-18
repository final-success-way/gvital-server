from django.urls import re_path
from ticketing import views
urlpatterns = [
        re_path(r'^contact-request/$', views.ContactRequest.as_view(),
            name=views.ContactRequest.name),
        re_path(r'^raise-issue/$', views.RaiseIssue.as_view(),
            name=views.RaiseIssue.name),
        re_path(r'^message-support/$', views.UpdateTicket.as_view(),
            name=views.UpdateTicket.name),
        re_path(r'^get-tickets/$', views.GetTickets.as_view(),
            name=views.GetTickets.name),
        ]