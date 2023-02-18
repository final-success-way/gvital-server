import base64
import decimal
import json
import os

import requests
import sys

from django.conf import settings
from django.core.mail import send_mail, get_connection
from django.db.models import Q
from django.template.loader import render_to_string
from idna import unicode
import urllib

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment, LiveEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersAuthorizeRequest
import stripe
from paypalhttp import HttpError
# Create your views here.
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from strgen import StringGenerator

from brf import settings_stage
from brf import settings_dev
from orders.models import Order
from rest_framework.response import Response
import requests
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import HttpResponse
from payments.models import Payment, StripeProductMap, PaymentGateway, Discount
from payments.serializers import DiscountSerializer
from utils.views import DecimalEncoder
from utils.UnitPay import UnitPay
from coinbase_commerce.client import Client

API_KEY = settings_stage.COINBASE_API_KEY


def requestOrderCreateApi(service, varient, meta, order_id):
    try:
        api = service.api_order_create
        print(service.platform.name+" "+service.name)
        order = Order.objects.filter(uid=order_id)
        if len(order) > 0:
            vendor = api.vendor
            url = api.vendor.api_base
            data = {}
            print(meta)
            print(api.parameters.all())
            for t in api.parameters.all():
                if t.parameter_type == 'number':
                    data.update({t.parameter: t.value})
                else:
                    data.update({t.parameter: t.value})
            print(data)
            data["key"] = vendor.api_key
            print(data)
            data.update({'link': meta.get('link'), 'username': meta.get('username'), 'quantity': meta.get('quantity')})
            print(data)
            payload = json.dumps(data)
            order[0].request_raw = payload
            order[0].save()
            headers = {
                'content-type': 'application/json'
            }
            #import pdb;pdb.set_trace()
            response = requests.request("POST", url, headers=headers, data=payload)
            order[0].request_raw = payload
            order[0].response_raw = json.dumps(response.json())
            order[0].save()
            resp = response.json()
            print(type(resp))
            print(resp)
            print(str(resp and resp.get("order") is not None))
            if resp and resp.get("order") is not None:
                order[0].status = Order.PROCESSING
                order[0].user_visible_status = Order.PROCESSING
                order[0].save()
            if response.status_code == 200:
                return True
        return False
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(str(e))
        return False


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class CreatePayment(generics.CreateAPIView):
    name = "create-payment"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client_id = settings_stage.PAYPAL_CLIENT_ID_SAND
        self.client_secret = settings_stage.PAYPAL_CLIENT_SECRET_SAND

        """Set up and return PayPal Python SDK environment with PayPal access credentials.
           This sample uses SandboxEnvironment. In production, use LiveEnvironment."""

        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)

        """ Returns PayPal HTTP client instance with environment that has access
            credentials context. Use this instance to invoke PayPal APIs, provided the
            credentials have access. """
        self.client = PayPalHttpClient(self.environment)
        self.cBaseClient = Client(api_key=settings_stage.COINBASE_API_KEY)
        self.unitPayApi = UnitPay("unitpay.money", settings_stage.UNITPAY_PUBLIC)

    def object_to_json(self, json_data):
        """
        Function to print all json data in an organized readable manner
        """
        result = {}
        if sys.version_info[0] < 3:
            itr = json_data.__dict__.iteritems()
        else:
            itr = json_data.__dict__.items()
        for key, value in itr:
            # Skip internal attributes.
            if key.startswith("__"):
                continue
            result[key] = self.array_to_json_array(value) if isinstance(value, list) else \
                self.object_to_json(value) if not self.is_primittive(value) else \
                    value
        return result

    def array_to_json_array(self, json_array):
        result = []
        if isinstance(json_array, list):
            for item in json_array:
                result.append(self.object_to_json(item) if not self.is_primittive(item) \
                                  else self.array_to_json_array(item) if isinstance(item, list) else item)
        return result

    def is_primittive(self, data):
        return isinstance(data, str) or isinstance(data, unicode) or isinstance(data, int)

    @action(methods=['post'], detail=True)
    def create(self, request, *args, **kwargs):

        response = {
            'message': '',
            'success': False
        }
        status_code = status.HTTP_400_BAD_REQUEST
        order_id = request.data.get('order_id', '')
        email = request.data.get('email', '')
        redirect_url = request.data.get('redirect_url', 'order')
        method = request.data.get('method', 'PAYPAL')

        try:
            order = Order.objects.filter(uid=order_id)
            if len(order) > 0:
                order = order[0]
                if method == 'STRIPE':
                    payment = Payment.objects.create(amount=order.amount, payment_status=Payment.PENDING,
                                                     meta=str(order.uid), payment_method=Payment.STRIPE)
                    order.payment = payment
                    order.save()
                    payment.save()
                    status_code = status.HTTP_200_OK
                    response.update({
                        "message": "Checkout session fetched successfully",
                        "success": True,
                        "amount": order.amount
                    })
                    return Response(response, status=status_code)

            raise Exception("Order not found")

        except Exception as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            response.update({
                "message": "Something wrong happened",
                "success": False,
                "server_response": str(e),
            })
        return Response(response, status=status_code)


class AuthorizePayment(generics.CreateAPIView):
    name = "authorize-payment"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client_id = settings_stage.PAYPAL_CLIENT_ID
        self.client_secret = settings_stage.PAYPAL_CLIENT_SECRET

        """Set up and return PayPal Python SDK environment with PayPal access credentials.
           This sample uses SandboxEnvironment. In production, use LiveEnvironment."""

        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)

        """ Returns PayPal HTTP client instance with environment that has access
            credentials context. Use this instance to invoke PayPal APIs, provided the
            credentials have access. """
        self.client = PayPalHttpClient(self.environment)

    def object_to_json(self, json_data):
        """
        Function to print all json data in an organized readable manner
        """
        result = {}
        if sys.version_info[0] < 3:
            itr = json_data.__dict__.iteritems()
        else:
            itr = json_data.__dict__.items()
        for key, value in itr:
            # Skip internal attributes.
            if key.startswith("__"):
                continue
            result[key] = self.array_to_json_array(value) if isinstance(value, list) else \
                self.object_to_json(value) if not self.is_primittive(value) else \
                    value
        return result

    def array_to_json_array(self, json_array):
        result = []
        if isinstance(json_array, list):
            for item in json_array:
                result.append(self.object_to_json(item) if not self.is_primittive(item) \
                                  else self.array_to_json_array(item) if isinstance(item, list) else item)
        return result

    def is_primittive(self, data):
        return isinstance(data, str) or isinstance(data, unicode) or isinstance(data, int)

    @action(methods=['post'], detail=True)
    def create(self, request, *args, **kwargs):

        response = {
            'message': '',
            'success': False
        }
        status_code = status.HTTP_400_BAD_REQUEST
        order_id = request.data.get('order_id', '')
        method = request.data.get('method', 'PAYPAL')

        try:
            response = self.client.execute(request)

        except Exception as e:
            print(e)
            return ""


class WebhookStripe(generics.CreateAPIView):
    name = "webhook-stripe"

    def send_order_details(self, subject, txtmes, to, order_id, service_name, amount, txn_id, qty, pay_method,
                           order_status, card):
        html_content = render_to_string('order-conf.html',
                                        {"order_id": order_id, "service_name": service_name, "amount": amount,
                                         "txn_id": txn_id, "quantity": qty, "pay_method": pay_method,
                                         "order_status": order_status, "card": card})
        print(html_content)

        with get_connection(
                host=settings.EMAIL_HOST,
                port=settings.EMAIL_PORT,
                username=settings.EMAIL_HOST_USER_NOREPLY,
                password=settings.EMAIL_HOST_PASSWORD_NOREPLY,
                use_tls=settings.EMAIL_USE_TLS
        ) as connection:
            mail = send_mail(subject,
                             message=txtmes,
                             recipient_list=[to],
                             from_email='Buyrealfollows <%s>' % settings.EMAIL_HOST,
                             connection=connection,
                             fail_silently=True,
                             html_message=html_content)
            print(mail)

    def send_order_details_newuser(self, subject, txtmes, to, password, order_id, service_name, amount, txn_id, qty,
                                   pay_method, order_status, card):
        html_content = render_to_string('order-new-user.html',
                                        {"password": password, "order_id": order_id, "service_name": service_name,
                                         "amount": amount,
                                         "txn_id": txn_id, "quantity": qty, "pay_method": pay_method,
                                         "order_status": order_status, "card": card})
        print(html_content)

        with get_connection(
                host=settings.EMAIL_HOST,
                port=settings.EMAIL_PORT,
                username=settings.EMAIL_HOST_USER_NOREPLY,
                password=settings.EMAIL_HOST_PASSWORD_NOREPLY,
                use_tls=settings.EMAIL_USE_TLS
        ) as connection:
            mail = send_mail(subject,
                             message=txtmes,
                             recipient_list=[to],
                             from_email='Buyrealfollows <%s>' % settings.EMAIL_HOST,
                             connection=connection,
                             fail_silently=True,
                             html_message=html_content)
            print(mail)

    @action(methods=['post'], detail=True)
    def create(self, request, *args, **kwargs):

        response = {
            'message': '',
            'success': False
        }
        status_code = status.HTTP_200_OK

        try:
            request_data = request.data
            data = request_data['data']
            event_type = request_data['type']
            extra_data = request_data['extra_data']
            data_object = data['object']
            # print(extra_data)
            if event_type == 'checkout.session.completed':
                print('Payment succeeded!')
                order_id = data_object['client_reference_id']
                checkout_session_id = data_object['id']
                order = Order.objects.filter(uid=order_id)
                print(len(order))
                if len(order) > 0:
                    order = order[0]
                    payment = order.payment
                    email = order.user.email
                    service = extra_data["product"]
                    currency = extra_data["currency"]
                    card = extra_data["card_last_4"]
                    payment.gateway_ref = checkout_session_id
                    payment.payment_status = Payment.COMPLETED
                    payment.payment_method = Payment.STRIPE
                    print("Reached before dump")
                    payment.meta = json.dumps(extra_data)
                    payment.save()
                    has_token = Token.objects.filter(user=order.user)
                    orders_by_user = Order.objects.filter(user=order.user)
                    print(has_token)
                    if len(has_token) > 0 or len(orders_by_user) > 0:
                        self.send_order_details('Order Details', "", email, order_id=order_id, service_name=service,
                                                amount=str(currency).upper() + " " + str(order.amount),
                                                txn_id=checkout_session_id,
                                                qty=str(order.quantity),
                                                pay_method=Payment.STRIPE, order_status=order.status, card=card)
                    else:
                        password = StringGenerator("[\d\w]{10}").render()
                        user = order.user
                        user.set_password(password)
                        user.save()
                        self.send_order_details_newuser('Welcome to Buyrealfollows', "", email,
                                                        password=password,
                                                        order_id=order_id,
                                                        service_name=service,
                                                        amount=str(currency).upper() + " " + str(order.amount),
                                                        txn_id=checkout_session_id,
                                                        qty=str(order.quantity),
                                                        pay_method=Payment.STRIPE, order_status=order.status, card=card)
                    print("Creating order")
                    raw_metadata = order.raw_metadata.replace("\'", "\"")
                    requestOrderCreateApi(service=order.service, varient=order.varient, meta=json.loads(raw_metadata),
                                          order_id=order.uid)
            elif event_type == 'checkout.session.failed':
                order_id = data_object['client_reference_id']
                checkout_session_id = data_object['id']
                order = Order.objects.filter(uid=order_id)
                if len(order) > 0:
                    order = order[0]
                    payment = order.payment
                    payment.gateway_ref = checkout_session_id
                    payment.payment_status = Payment.FAILED
                    payment.payment_method = Payment.STRIPE
                    payment.save()

            response = {
                'message': 'Success',
                'success': True
            }
            return Response(response, status=status_code)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(str(e))
            response = {
                'message': str(e),
                'success': True
            }
        return Response(response, status=status_code)


class WebhookUnitPay(generics.CreateAPIView):
    name = "webhook-unitpay"

    @action(methods=['post'], detail=True)
    def create(self, request, *args, **kwargs):
        payload = request.body
        event = None

        response = {
            'message': '',
            'success': False
        }
        status_code = status.HTTP_200_OK

        response = {
            'message': '',
            'success': True
        }

        return Response(response, status=status_code)

    @action(methods=['get'], detail=True)
    def list(self, request, *args, **kwargs):
        payload = request.body
        event = None

        response = {
            'message': '',
            'success': False
        }
        status_code = status.HTTP_200_OK

        response = {
            'result': {
                "message": "Payment received"
            }
        }

        return Response(response, status=status_code)


class WebhookCoinbase(generics.CreateAPIView):
    name = "webhook-coinbase"

    @action(methods=['post'], detail=True)
    def create(self, request, *args, **kwargs):
        payload = request.body
        # sig_header = request.META['X-CC-Webhook-Signature']
        # sig_header = request.headers['X-CC-Webhook-Signature']
        event = None

        response = {
            'message': '',
            'success': False
        }
        status_code = status.HTTP_200_OK

        try:

            webhook_secret = settings_stage.STRIPE_LIVE_WEBHOOK_SECRET
            request_data = request.data

            # if webhook_secret:
            #     # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
            #     signature = request.headers.get('stripe-signature')
            #     print('signature' + signature)
            #     print('webhook_secret' + webhook_secret)
            #     event = None
            #     print(request.data)
            #     event = stripe.Webhook.construct_event(
            #         payload=payload, sig_header=sig_header, secret=webhook_secret
            #     )
            #     data = event['data']
            #     # Get the type of webhook event sent - used to check the status of PaymentIntents.
            #     event_type = event['type']
            # else:
            data = request_data['data']
            event_type = request_data['type']
            data_object = request_data['data']

            if event_type == 'charge:pending':
                print('Payment pending!')
                print(data_object)
                order_id = data_object['metadata']['order_id']
                checkout_session_id = data_object['id']
                order = Order.objects.filter(uid=order_id)
                if len(order) > 0:
                    order = order[0]
                    payment = order.payment
                    payment.gateway_ref = checkout_session_id
                    payment.payment_status = Payment.PROCESSING
                    payment.payment_method = Payment.COINBASE
                    payment.save()
                    # self.sendOrderDetails("Order details", "", "no-reply@buyrealfollows.com", email, )
                    # requestOrderCreateApi(service=order.service, varient=order.varient, meta=json.loads(order.raw_metadata), order_id=order.uid)

            if event_type == 'charge:confirmed':
                print(data_object)
                order_id = data_object['metadata']['order_id']
                checkout_session_id = data_object['id']
                order = Order.objects.filter(uid=order_id)
                if len(order) > 0:
                    order = order[0]
                    payment = order.payment
                    payment.gateway_ref = checkout_session_id
                    payment.payment_status = Payment.COMPLETED
                    payment.payment_method = Payment.COINBASE
                    payment.save()
                    raw_metadata = order.raw_metadata.replace("\'", "\"")
                    requestOrderCreateApi(service=order.service, varient=order.varient, meta=json.loads(raw_metadata),
                                          order_id=order.uid)

            response = {
                'message': '',
                'success': True
            }
            return Response(response, status=status_code)

        except Exception as e:
            response = {
                'message': '',
                'success': True
            }
        return Response(response, status=status_code)

    @action(methods=['get'], detail=True)
    def list(self, request, *args, **kwargs):
        payload = request.body
        event = None

        response = {
            'message': '',
            'success': False
        }
        status_code = status.HTTP_200_OK

        response = {
            'message': '',
            'success': True
        }

        return Response(response, status=status_code)


class VerifyPayment(generics.ListAPIView):
    name = "verify-payment"

    @action(methods=['get'], detail=True)
    def list(self, request, *args, **kwargs):
        response = {
            'message': '',
            'success': False
        }
        status_code = status.HTTP_400_BAD_REQUEST
        payment_ref = request.query_params.get('payment_ref', '')
        #import pdb;pdb.set_trace()
        try:
            payment = Payment.objects.filter(gateway_ref=payment_ref)

            if len(payment) > 0:

                payment = payment[0]
                orders = Order.objects.filter(payment__uid=payment.uid)
                if len(orders) > 0:
                    order = orders[0]
                    email = order.user.email
                    message = "Payment didn't receive yet"
                    if payment.payment_status == Payment.COMPLETED:
                        message = 'Payment received'
                    elif payment.payment_status == Payment.FAILED:
                        message = 'Payment failed'

                    response = {
                        'message': message,
                        'success': payment.payment_status == Payment.COMPLETED,
                        'payment_status': payment.payment_status,
                        'email': email,
                        'new_account': len(orders) <= 2,
                        'product_name': order.service.name,
                        'payment_method': payment.payment_method,
                        'product_pricing': order.varient.original_price,
                        'product_quantity': order.varient.quantity,
                        'order_id': order.order_id,
                        'product_discount': order.varient.percent_discount,
                        'order_amount': order.amount,
                        'product_platform': order.service.platform.name
                    }
                    status_code = status.HTTP_200_OK
                    return Response(response, status=status_code)

            else:
                response = {
                    'message': 'Something wrong happened',
                    'success': False
                }
                status_code = status.HTTP_400_BAD_REQUEST
                return Response(response, status=status_code)

        except Exception as e:

            response.update({

                "message": str(e) or "Something wrong happened",
                "success": False,
                "server_response": str(e)

            })

        return Response(response, status=status_code)


class StripePublishableKey(generics.CreateAPIView):
    name = "publishable-stripe"

    @action(methods=['get'], detail=True)
    def create(self, request, *args, **kwargs):
        response = {
            'message': '',
            'success': False
        }
        status_code = status.HTTP_400_BAD_REQUEST
        order_id = request.data.get('order_id', '')

        response = {
            'message': '',
            'success': True,
            'key': settings_stage.STRIPE_LIVE_PUBLIC_KEY
        }
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)


class GatewayDiscount(generics.ListAPIView):
    name = 'gateway-discount'
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer

    # filterset_fields = ['shop__', 'status']

    def get_queryset(self):
        print(self.request.query_params)
        queryset = Discount.objects.filter()
        return queryset
