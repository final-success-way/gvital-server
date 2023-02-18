from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from orders.models import *
from services.serializers import ServiceSerializer


class OrderSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = Order
        exclude = ['user']
        depth = 2
