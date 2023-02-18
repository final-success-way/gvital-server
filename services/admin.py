from django.contrib import admin
from services.models import *
from bitfield import BitField

from bitfield.forms import BitFieldCheckboxSelectMultiple



# Register your models here.
admin.site.register(Varient)
admin.site.register(Service)
admin.site.register(Platform)
admin.site.register(FAQ)
admin.site.register(Review)

