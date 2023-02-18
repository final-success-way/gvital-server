from django.db.models import Q
from rest_framework.authentication import (TokenAuthentication,
                                           SessionAuthentication)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from strgen import StringGenerator

from accounts.models import *
from orders.serializers import OrderSerializer
from payments.models import ActivePaymentGateway
from payments.views import *
from services.models import Service, Varient
from utils.views import *
from django_q.models import Schedule
from django_q.tasks import schedule

schedule("orders.services.sync_all_orders", '',
         hook="orders.services.sync_done",
         schedule_type=Schedule.HOURLY)

schedule("orders.services.retry_all_failed_orders", '',
         hook="orders.services.sync_done",
         schedule_type=Schedule.HOURLY)


class CreateOrder(generics.CreateAPIView):
    name = 'create-order'

    def sendOrderDetailsNewUser(self, subject, txtmes, fromUser, to, password):
        html_content = render_to_string('welcome-password.html', {'password': password})
        # txtmes = render_to_string('text-message.html')
        with get_connection(
                host=settings.EMAIL_HOST,
                port=settings.EMAIL_PORT,
                username=settings.EMAIL_HOST_USER_SUPPORT,
                password=settings.EMAIL_HOST_PASSWORD_SUPPORT,
                use_tls=settings.EMAIL_USE_TLS
        ) as connection:
            mail = send_mail(subject,
                             message=txtmes,
                             recipient_list=[to],
                             from_email='Support Buyrealfollows <%s>' % settings.EMAIL_HOST,
                             connection=connection,
                             fail_silently=False,
                             html_message=html_content)
            print(mail)

    def requestOrderCreateApi(self, varient, service, meta, order):

        try:
            api = service.api_order_create
            print(service.platform.name + " " + service.name)
            vendor = api.vendor
            url = api.vendor.api_base
            data = {}
            print(meta)
            print(api.parameters.all())
            for t in api.parameters.all():
                if t.parameter_type == 'number':
                    data.update({t.parameter: int(t.value)})
                else:
                    data.update({t.parameter: t.value})
            print(data)
            data["key"] = vendor.api_key
            print(data)
            data.update(
                {'link': meta.get('link'), 'username': meta.get('username'), 'quantity': meta.get('quantity')})
            print(data)
            payload = json.dumps(data)
            order.request_raw = payload
            order.save()
            headers = {
                'content-type': 'application/json'
            }
            # import pdb;pdb.set_trace()
            response = requests.request("POST", url, headers=headers, data=payload)
            order.request_raw = payload
            order.response_raw = json.dumps(response.json())
            order.save()
            resp = response.json()
            print(type(resp))
            print(resp)
            print(str(resp and resp.get("order") is not None))
            if resp and resp.get("order") is not None:
                order.status = Order.PROCESSING
                order.user_visible_status = Order.PROCESSING
                order.save()
            if response.status_code == 200:
                return True
            return False
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(str(e))
            return False

    @action(methods=['post'], detail=True)
    def create(self, request, *args, **kwargs):
        response = {
            'message': '',
            'success': False
        }

        email = request.data.get('email', '')
        meta = request.data.get('meta', '')
        # current_order = request.data.get('current_order', None)
        product_id = request.data.get('product_id', '')
        status_code = status.HTTP_400_BAD_REQUEST
        try:

            temp_profile = Profile.objects.filter(email=email)
            varient = Varient.objects.filter(uid=product_id)
            # import pdb;pdb.set_trace()
            if len(varient) == 0:
                raise Exception("Product not found")
            varient = varient[0]
            services = Service.objects.filter(varients__uid=product_id)
            order = None
            if len(temp_profile) > 0:
                user = temp_profile[0].user
            else:
                password = StringGenerator("[\d\w]{10}").render()
                user = User.objects.create_user(
                    username=email, email=email, password=password)

                profile = Profile.objects.create(user=user, email=email, meta=meta)
                profile.is_email_verified = False
                profile.flags.is_user = True
                profile.save()

            if len(services) > 0:
                service = services[0]
                free = float(varient.discounted_price) == float(0)
                print('Pricing ' + varient.discounted_price)
                if free:
                    orders = Order.objects.filter(
                        Q(product__uid=product_id, user=user) | Q(product__uid=product_id, meta=meta)
                    )
                    if len(orders) > 0:
                        response.update({
                            "message": "You have already availed this offer, you can now browse our other services",
                            "success": False
                        })
                        return Response(response, status=status_code)

                    order = Order.objects.create(service=service, amount=varient.discounted_price, meta=meta, user=user,
                                                 status=Order.PENDING)
                    metadata = {
                        "link": meta,
                        "quantity": int(varient.quantity),
                        "username": meta,
                    }
                    order.quantity = int(varient.quantity)
                    order.raw_metadata = json.dumps(metadata)
                    order.save()
                    self.requestOrderCreateApi(varient=varient, service=service, meta=metadata, order=order)
                # elif current_order is not None:
                #     order = Order.objects.filter(uid=current_order)
                #     if len(order) > 0:
                #         order = order[0]
                #         if order.status == Order.PENDING:
                #             order.service = service
                #             order.varient = varient
                #             order.amount = varient.discounted_price
                #             order.meta = meta
                #             order.user = user
                #             order.status = Order.PENDING
                #             order.quantity = int(varient.quantity)
                #             order.save()
                #
                #             metadata = {
                #                 "link": meta,
                #                 "quantity": int(varient.quantity),
                #                 "username": meta,
                #             }
                #             order.raw_metadata = json.dumps(metadata)
                #             order.save()
                #     else:
                #         order = Order.objects.create(service=service, varient=varient, amount=varient.discounted_price,
                #                                      meta=meta, user=user,
                #                                      status=Order.PENDING)
                #         order.quantity = int(varient.quantity)
                #         order.save()
                #
                #         metadata = {
                #             "link": meta,
                #             "quantity": int(varient.quantity),
                #             "username": meta,
                #         }
                #         order.raw_metadata = json.dumps(metadata)
                #         order.save()

                else:
                    order = Order.objects.create(service=service, varient=varient, amount=varient.discounted_price,
                                                 meta=meta, user=user,
                                                 status=Order.PENDING)
                    order.quantity = int(varient.quantity)
                    order.save()

                    metadata = {
                        "link": meta,
                        "quantity": int(varient.quantity),
                        "username": meta,
                    }
                    order.raw_metadata = json.dumps(metadata)
                    order.save()
                active_payment = None
                active_payments = ActivePaymentGateway.objects.filter(active=True,
                                                                      payment_method='STRIPE')
                if len(active_payments) > 0:
                    active_payment = active_payments[0]

                status_code = status.HTTP_200_OK
                if not free:
                    response.update({
                        "message": "Your order has started processing, please continue for payment",
                        "success": True,
                        "payment_url": active_payment.url if active_payment is not None else 'https://www.nvmservers.com/stripe/',
                        "order_id": order.uid,
                    })
                else:
                    response.update({
                        "message": "Your order has successfully been placed",
                        "success": True,
                        "payment_url": False,
                        "order_id": order.uid
                    })
                return Response(response, status=status_code)

            status_code = status.HTTP_400_BAD_REQUEST
            response.update({
                "message": "Product doesn't exist thanks",
                "success": False
            })
            return Response(response, status=status_code)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(str(e))
            response.update({
                "message": str(e) or "Something wrong happened",
                "success": False,
                "server_response": str(e)
            })

        return Response(response, status=status_code)


class RepeatOrder(generics.CreateAPIView):
    name = 'repeat-order'
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def requestProductApi(self, product):

        return ""

    @action(methods=['post'], detail=True)
    def create(self, request, *args, **kwargs):
        response = {
            'message': '',
            'success': False
        }

        # email = request.data.get('email', '')
        # meta = request.data.get('meta', '')
        # full_name = request.data.get('full_name', '')
        # create_account = request.data.get('create_account', '0')
        order_id = request.data.get('order_id', '')
        selected = request.data.get('selected', '')
        source = request.data.get('source', '')
        status_code = status.HTTP_400_BAD_REQUEST
        # import pdb;pdb.set_trace()
        try:
            temp_user = request.user

            status_code = status.HTTP_400_BAD_REQUEST
            profile = Profile.objects.filter(user=temp_user)

            orders = Order.objects.filter(uid=order_id)
            varients = Varient.objects.filter(uid=order_id)
            if len(varients) > 0:
                varient = varients[0]
                free = int(varient.discounted_price) == 0
                print('Pricing ' + varient.discounted_price)
                if free:
                    if len(orders) > 0:
                        response.update({
                            "message": "You have already availed this offer, you can now buy the same order for ",
                            "success": False
                        })
                        return Response(response, status=status_code)

                order = Order.objects.create(product=varient, amount=varient.discounted_price,
                                             user=temp_user,
                                             status='PROCESSING')
                order.quantity = int(varient.quantity)
                order.save()

                # if create_account == 1:
                #     password = StringGenerator("[\d\w]{10}").render()
                #     temp_user.set_password(password)
                #     temp_user.save()
                #     print("New Password sent")
                #     self.sendWelcomeEmail("Welcome to Buyrealfollows", "", "no-reply@kollect.ai", email, password)

                payment = CreatePayment()
                result = payment.createPaypalPayment(amount=varient.discounted_price, order=order.uid)
                print(result)
                status_code = status.HTTP_200_OK
                response.update({
                    "message": "Your order has successfully been placed",
                    "success": True,
                    "payment_url": result
                })

                return Response(response, status=status_code)

            response.update({
                "message": "Product doesn't exist thanks",
                "success": False
            })
            return Response(response, status=status_code)

        except Exception as e:
            response.update({
                "message": "Something wrong happened",
                "success": False,
                "server_response": str(e)
            })
            return Response(response, status=status_code)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10


class GetOrders(generics.ListAPIView):
    name = 'get-user-info'
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = StandardResultsSetPagination

    # filterset_fields = ['shop__', 'status']

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.filter(user=user).exclude(status=Order.PENDING).order_by('-updated_at')
        return queryset