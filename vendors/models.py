from django.db import models
import uuid


class Meta(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now=True)
    uid = models.UUIDField(default=uuid.uuid4, unique=True)
    active = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Vendor(Meta):
    name = models.CharField(max_length=50, blank=True)
    main_url = models.CharField(max_length=100, blank=True)
    api_base = models.CharField(max_length=200, blank=True)
    api_key = models.CharField(max_length=200, blank=True)

    def __str__(self):
        show = self.name
        if self.name:
            show = self.name
        return '%s' % (show)


class RequestParameters(models.Model):
    name = models.CharField(max_length=50, blank=True)
    parameter = models.CharField(max_length=50, blank=True)
    parameter_type = models.CharField(max_length=50, blank=True)
    value = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s => %s Type=> %s' % (self.name, self.parameter, self.value, self.parameter_type)


class ResponseParameters(models.Model):
    name = models.CharField(max_length=50, blank=True)
    parameter = models.CharField(max_length=50, blank=True)
    parameter_type = models.CharField(max_length=50, blank=True)
    value = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s => %s Type=> %s' % (self.name, self.parameter, self.value, self.parameter_type)


class VendorApi(Meta):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    UPDATE = 'UPDATE'
    ORDERS_STATUS = 'ORDERS_STATUS'
    ORDERS_PLACE = 'ORDERS_PLACE'
    MULTI_ORDERS_STATUS = 'MULTI_ORDERS_STATUS'
    CREATE_REFILL = 'CREATE_REFILL'
    USER_BALANCE = 'USER_BALANCE'
    REFILL_STATUS = 'REFILL_STATUS'

    API_TYPES_CHOICES = [
        (ORDERS_PLACE, 'ORDERS_PLACE'),
        (ORDERS_STATUS, 'ORDERS_STATUS'),
        (MULTI_ORDERS_STATUS, 'MULTI_ORDERS_STATUS'),
        (CREATE_REFILL, 'CREATE_REFILL'),
        (REFILL_STATUS, 'REFILL_STATUS'),
        (USER_BALANCE, 'USER_BALANCE'),
    ]

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, default=None)
    api_name = models.CharField(max_length=200, blank=True)
    api_url = models.CharField(max_length=250, blank=True)
    api_type = models.CharField(max_length=100,
                                choices=API_TYPES_CHOICES,
                                default=ORDERS_PLACE, )
    HTTP_METHODS = [
        (GET, 'GET'),
        (POST, 'POST'),
        (PUT, 'PUT'),
        (DELETE, 'DELETE'),
        (UPDATE, 'UPDATE'),
    ]
    http_method = models.CharField(
        max_length=50,
        choices=HTTP_METHODS,
        default=GET,
    )
    parameters = models.ManyToManyField(RequestParameters)
    params = models.TextField(blank=True, null=True)
    response_params = models.ManyToManyField(ResponseParameters)
    resp_params = models.TextField(blank=True, null=True)

    def __str__(self):
        return '%s --> %s -->%s -->%s' % (self.vendor.name, self.api_name, self.api_type, self.params)
