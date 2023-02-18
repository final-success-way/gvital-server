from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from orders.models import *
from services.models import Service, Platform, Varient


class ServiceProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        exclude = ['created_at', 'id', 'active']
        depth = 2


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        exclude = ['created_at', 'id', 'active', 'api_order_create', 'api_order_status', 'api_order_refill']
        depth = 2


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = False
        exclude = ['created_at', 'id', 'active', 'updated_at']
        depth = 2


class PlatformSerializer(serializers.ModelSerializer):
    services = serializers.SerializerMethodField()

    def get_services(self, platform):
        services = Service.objects.filter(active=True, platform__uid=platform.uid)
        serializer = ServiceSerializer(instance=services, many=True)
        return serializer.data

    class Meta:
        model = Platform
        exclude = ['created_at', 'id', 'active']
        depth = 2
