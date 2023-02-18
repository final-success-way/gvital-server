import datetime

from bitfield import BitField
from django.contrib.auth.models import User
from django.db import models
import uuid
# Create your models here.

class Meta(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now=True)
    uid = models.UUIDField(default=uuid.uuid4, unique=True)
    active = models.BooleanField(default=False)

    class Meta:
        abstract = True

class TempToken(Meta):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return '%s %s' % (self.user.email, self.token)

class Profile(Meta):
    name = models.CharField(max_length=50, blank=True)
    meta = models.CharField(max_length=150, blank=True)
    email = models.CharField(max_length=100, blank=True, unique=True)
    city = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=50, blank=True)
    picture_url = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_email_verified = models.BooleanField(default=False)
    flags = BitField(flags=(
        'is_user',
        'is_staff'),
        null=True, blank=True)


    def __str__(self):
        show = self.email
        if self.name:
            show = self.name
        return '%s' % (show)



class Funds(Meta):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.CharField(max_length=10, blank=False, default='0')

    def __str__(self):
        email = self.user.email
        return '%s %s' % (email, self.amount)


