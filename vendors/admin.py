from django.contrib import admin
from vendors.models import *
from bitfield import BitField

from bitfield.forms import BitFieldCheckboxSelectMultiple



# Register your models here.
admin.site.register(Vendor)
admin.site.register(VendorApi)
admin.site.register(RequestParameters)
admin.site.register(ResponseParameters)

