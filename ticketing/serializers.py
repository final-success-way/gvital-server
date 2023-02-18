from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from ticketing.models import *


class TicketSerializer(serializers.ModelSerializer):
    # messages = serializers.SerializerMethodField()
    #
    # def get_messages(self, services):
    #     services = Product.objects.filter(service__uid=services.uid).order_by('quantity')
    #     serializer = ProductSerializer(instance=services, many=True)
    #     return serializer.data

    class Meta:
        model = Ticket
        exclude = ['id', 'active']
        depth = 2