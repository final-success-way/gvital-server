from django.contrib import admin
from ticketing.models import *
from bitfield import BitField

from bitfield.forms import BitFieldCheckboxSelectMultiple



# Register your models here.
admin.site.register(Ticket)
admin.site.register(Message)
admin.site.register(ContactMessage)

