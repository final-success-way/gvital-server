from django.contrib import admin
from orders.models import *
from bitfield import BitField

from bitfield.forms import BitFieldCheckboxSelectMultiple
from django_q import models as q_models
from django_q import admin as q_admin


admin.site.unregister([q_models.Failure])
@admin.register(q_models.Failure)
class ChildClassAdmin(q_admin.FailAdmin):
    list_display = (
        'name',
        'func',
        'result',
        'started',
        # add attempt_count to list_display
        'attempt_count'
    )


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('service',)
    list_display = (
        'uid', 'email', 'service', 'varient', 'amount', 'quantity', 'raw_metadata', 'response_raw', 'payment', 'status', 'user_visible_status')
    search_fields = ['uid', 'email', 'response_raw', 'payment', 'status', 'user_visible_status']

    def email(self, obj):
        return obj.user.email


# Register your models here.
admin.site.register(Order, OrderAdmin)
