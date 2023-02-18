import datetime

from bitfield import BitField
from django.contrib.auth.models import User
from django.db import models
import uuid
from nanoid import generate

from vendors.models import VendorApi, Vendor


class Meta(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now=True)
    uid = models.UUIDField(default=uuid.uuid4, unique=True)
    active = models.BooleanField(default=False)

    class Meta:
        abstract = True


class ContactMessage(Meta):
    message = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=150, blank=True, null=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    extra = models.TextField(blank=True, null=True)
    reply = models.TextField(blank=True, null=True)

    def __str__(self):
        return "%s %s %s" % (self.email, self.name, self.message)


class Message(Meta):
    message = models.TextField(blank=True, null=True)
    reply = models.TextField(blank=True, null=True)
    attachment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % (self.user.email)


class Ticket(Meta):
    ORDER = 'ORDER'
    PAYMENT = 'PAYMENT'
    SERVICE = 'SERVICE'
    CHILDPANEL = 'CHILDPANEL'
    OTHER = 'OTHER'

    SUBJECT_TYPES_CHOICES = [
        (ORDER, 'ORDER'),
        (PAYMENT, 'PAYMENT'),
        (SERVICE, 'SERVICE'),
        (CHILDPANEL, 'CHILDPANEL'),
        (OTHER, 'OTHER')
    ]

    subject = models.CharField(max_length=100,
                               choices=SUBJECT_TYPES_CHOICES,
                               default=ORDER, )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    messages = models.ManyToManyField(Message)

    def __str__(self):
        return "%s" % (self.subject)
