import uuid

from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField


# Create your models here.
class Meta(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now=True)
    uid = models.UUIDField(default=uuid.uuid4, unique=True)
    active = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Post(Meta):
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(max_length=2000, blank=True, null=True)
    content = RichTextField(blank=True, null=True)
    slug = models.TextField(max_length=400, blank=True, null=True)
    imageUrl = models.TextField(max_length=400, blank=True, null=True)
    readingTime = models.CharField(max_length=50, blank=True, null=True)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "%s %s" % (self.title, self.author.email)
