from django.contrib import admin
from orders.models import *
from bitfield import BitField

from bitfield.forms import BitFieldCheckboxSelectMultiple



# Register your models here.
from payments.models import StripeProductMap, Payment, PaymentGateway, Discount, ActivePaymentGateway

admin.site.register(Payment)
admin.site.register(StripeProductMap)
admin.site.register(PaymentGateway)
admin.site.register(Discount)
admin.site.register(ActivePaymentGateway)

