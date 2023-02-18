from django.db import models
import uuid

from services.models import Service


class Meta(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now=True)
    uid = models.UUIDField(default=uuid.uuid4, unique=True)
    active = models.BooleanField(default=False)

    class Meta:
        abstract = True


class StripeProductMap(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    stripe_payment_key = models.CharField(max_length=100, blank=False, null=False, default='0')

    def __str__(self):
        return '%s--> %s' % (
            self.service.name, self.stripe_payment_key)


class PaymentGateway(Meta):
    PAYPAL = 'PAYPAL'
    STRIPE = 'STRIPE'
    UNITPAY = 'UNITPAY'
    COINBASE = 'COINBASE'
    PAYERR = 'PAYERR'
    PAYOP = 'PAYOP'

    PAYMENT_METHOD_CHOICES = [
        (PAYPAL, 'PAYPAL'),
        (STRIPE, 'STRIPE'),
        (UNITPAY, 'UNITPAY'),
        (COINBASE, 'COINBASE'),
        (PAYOP, 'PAYOP'),
        (PAYERR, 'PAYERR'),
    ]

    name = models.CharField(max_length=100,
                            choices=PAYMENT_METHOD_CHOICES,
                            default=PAYPAL, )

    active = models.BooleanField(default=False)

    def __str__(self):
        return '%s, Enabled: %s' % (self.name, self.active)


class ActivePaymentGateway(models.Model):
    PAYPAL = 'PAYPAL'
    STRIPE = 'STRIPE'
    UNITPAY = 'UNITPAY'
    COINBASE = 'COINBASE'
    PAYERR = 'PAYERR'
    PAYOP = 'PAYOP'
    PAYMENT_METHOD_CHOICES = [
        (PAYPAL, 'PAYPAL'),
        (STRIPE, 'STRIPE'),
        (UNITPAY, 'UNITPAY'),
        (COINBASE, 'COINBASE'),
        (PAYERR, 'PAYERR'),
        (PAYOP, 'PAYOP'),
    ]

    active = models.BooleanField(default=False)
    url = models.TextField(null=True,blank=True)
    payment_method = models.CharField(max_length=100,
                                      choices=PAYMENT_METHOD_CHOICES,
                                      default=PAYPAL, )

    def __str__(self):
        return '%s, Enabled: %s %s' % (self.active, self.url, self.payment_method)


class Payment(Meta):
    COMPLETED = 'COMPLETED'
    PENDING = 'PENDING'
    PROCESSING = 'PROCESSING'
    FAILED = 'FAILED'
    PAYPAL = 'PAYPAL'
    STRIPE = 'STRIPE'
    UNITPAY = 'UNITPAY'
    COINBASE = 'COINBASE'
    PAYERR = 'PAYERR'
    PAYOP = 'PAYOP'

    PAYMENT_STATUS_CHOICES = [
        (COMPLETED, 'COMPLETED'),
        (PENDING, 'PENDING'),
        (FAILED, 'FAILED'),
        (PROCESSING, 'PROCESSING'),
    ]

    PAYMENT_METHOD_CHOICES = [
        (PAYPAL, 'PAYPAL'),
        (STRIPE, 'STRIPE'),
        (UNITPAY, 'UNITPAY'),
        (COINBASE, 'COINBASE'),
        (PAYERR, 'PAYERR'),
        (PAYOP, 'PAYOP'),
    ]

    payment_method = models.CharField(max_length=100,
                                      choices=PAYMENT_METHOD_CHOICES,
                                      default=PAYPAL, )
    amount = models.CharField(max_length=10, blank=False, default='0')
    meta = models.TextField(null=True, blank=True)
    payment_status = models.CharField(max_length=100,
                                      choices=PAYMENT_STATUS_CHOICES,
                                      default=PENDING, )
    gateway_ref = models.TextField(null=True, blank=True)

    def __str__(self):
        return '%s , %s--> %s' % (self.payment_method, self.gateway_ref, self.payment_status)


class Discount(Meta):
    PAYPAL = 'PAYPAL'
    STRIPE = 'STRIPE'
    UNITPAY = 'UNITPAY'
    COINBASE = 'COINBASE'
    PAYERR = 'PAYERR'
    PAYOP = 'PAYOP'

    PAYMENT_METHOD_CHOICES = [
        (PAYPAL, 'PAYPAL'),
        (STRIPE, 'STRIPE'),
        (UNITPAY, 'UNITPAY'),
        (COINBASE, 'COINBASE'),
        (PAYERR, 'PAYERR'),
        (PAYOP, 'PAYOP'),
    ]

    gateway = models.CharField(max_length=100,
                               choices=PAYMENT_METHOD_CHOICES,
                               default=PAYPAL, )
    discount_percent = models.CharField(max_length=10, blank=False, default='0')

    def __str__(self):
        return "%s %s" % (self.gateway, self.discount_percent)
