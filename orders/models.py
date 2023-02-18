import datetime

from bitfield import BitField
from django.contrib.auth.models import User
from django.db import models

from payments.models import Payment
from services.models import Service, Varient
import uuid
from nanoid import generate


class Meta(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now=True)
    uid = models.UUIDField(default=uuid.uuid4, unique=True)
    active = models.BooleanField(default=False)
    order_id = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        abstract = True


class StatusCheck(Meta):
    last_checked = models.DateTimeField(auto_now=False)

    def __str__(self):
        return "%s" % (self.last_checked)


class Order(Meta):
    COMPLETED = "COMPLETED"
    IN_PROGRESS = "IN PROGRESS"
    PROCESSING = "PROCESSING"
    PARTIAL = "PARTIAL"
    FAILED = "FAILED"
    PENDING = "PENDING"
    CANCELLED = "CANCELLED"
    service = models.ForeignKey(Service, on_delete=models.CASCADE, default=None)
    varient = models.ForeignKey(Varient, on_delete=models.CASCADE, default=None)
    quantity = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.CharField(max_length=10, blank=False, default='0')
    meta = models.CharField(blank=True, null=True, max_length=120)
    raw_metadata = models.TextField(blank=True, null=True)
    request_raw = models.TextField(blank=True, null=True)
    response_raw = models.TextField(blank=True, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    ORDER_STATUS = [
        (COMPLETED, 'COMPLETED'),
        (PROCESSING, 'PROCESSING'),
        (FAILED, 'FAILED'),
        (PENDING, 'PENDING'),
        (CANCELLED, 'CANCELLED'),
        (IN_PROGRESS, 'IN_PROGRESS'),
        (PARTIAL, 'PARTIAL'),
    ]
    status = models.CharField(
        max_length=50,
        choices=ORDER_STATUS,
        default=PENDING,
    )
    user_visible_status = models.CharField(
        max_length=50,
        choices=ORDER_STATUS,
        default=PENDING,
    )

    def __str__(self):
        if self.payment:
            return "%s %s Payment:%s" % (self.uid, self.status, self.payment)
        else:
            return "%s %s" % (self.uid, self.status)
