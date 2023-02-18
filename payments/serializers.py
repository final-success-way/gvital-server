from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from orders.models import *
from payments.models import Discount


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        exclude = ['created_at', 'id', 'active']
        depth = 2
