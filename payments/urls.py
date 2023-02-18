from django.urls import re_path
from django.urls import include

from payments import views

urlpatterns = [
        re_path(r'^create-payment/$', views.CreatePayment.as_view(),
            name=views.CreatePayment.name),
        re_path(r'^approve-payment/$', views.AuthorizePayment.as_view(),
            name=views.AuthorizePayment.name),
        re_path(r'^verify-payment/$', views.VerifyPayment.as_view(),
            name=views.VerifyPayment.name),
        re_path(r'^webhook-stripe/$', views.WebhookStripe.as_view(),
            name=views.WebhookStripe.name),
        # re_path(r'^webhook-paypal/$', views.WebhookPaypal.as_view(),
        #     name=views.WebhookPaypal.name),
        # re_path(r'^webhook-unitpay/$', views.WebhookUnitPay.as_view(),
        #     name=views.WebhookUnitPay.name),
        # re_path(r'^webhook-coinbase/$', views.WebhookCoinbase.as_view(),
        #     name=views.WebhookCoinbase.name),
        re_path(r'^stripe-key/$', views.StripePublishableKey.as_view(),
            name=views.StripePublishableKey.name),
        re_path(r'^gateway-discount/$', views.GatewayDiscount.as_view(),
            name=views.GatewayDiscount.name),
        ]