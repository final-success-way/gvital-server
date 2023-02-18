from rest_framework.authentication import (TokenAuthentication,
                                           SessionAuthentication)
from rest_framework.permissions import IsAuthenticated
from payments.views import *
from services.models import Service, Platform, FAQ
from services.serializers import PlatformSerializer, ServiceSerializer, ServiceProductSerializer, FAQSerializer


class PlatformServiceList(generics.ListAPIView):
    name = 'get-services-list'
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    search_fields = ['slug']

    def get_queryset(self):
        slug = self.request.query_params.get('slug', '')
        queryset = Service.objects.filter(Q(active=True, slug=slug) | Q(active=True, platform__slug=slug))
        return queryset


class FAQList(generics.ListAPIView):
    name = 'get-faq-list'
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def get_queryset(self):
        queryset = FAQ.objects.all(is_general=True)
        return queryset


class OrderStatus(generics.CreateAPIView):
    name = 'get-order-status'
    queryset = FAQ.objects.all()
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    @action(methods=['post'], detail=True)
    def create(self, request, *args, **kwargs):
        order_id = request.data.get('order_id', '')
        service_id = request.data.get('service_id', '')
        response = {
            'message': '',
            'success': False
        }
        status_code = status.HTTP_400_BAD_REQUEST
        # import pdb;pdb.set_trace()
        try:
            user = request.user
            if user.is_superuser:
                services = Service.objects.filter(uid=service_id)
                if len(services) == 0:
                    raise Exception("Service not found")

                service = services[0]
                api = service.api_order_status
                print(service.platform.name + " " + service.name)
                order = Order.objects.filter(uid=order_id)
                if len(order) > 0:
                    vendor = api.vendor
                    url = api.vendor.api_base
                    data = {}
                    print(api.parameters.all())
                    for t in api.parameters.all():
                        if t.parameter_type == 'number':
                            data.update({t.parameter: int(t.value)})
                        else:
                            data.update({t.parameter: t.value})
                    print(data)
                    data["key"] = vendor.api_key
                    data["order"] = order_id
                    print(data)
                    headers = {
                        'content-type': 'application/json'
                    }
                    payload = json.dumps(data)
                    resp = requests.request("POST", url, headers=headers, data=payload)
                    order_status = resp.json()
                    if order_status["status"] == "In progress":
                        order[0].status = Order.PROCESSING
                    if order_status["status"] == "Partial":
                        order[0].status = Order.PARTIAL
                    if order_status["status"] == "Processing":
                        order[0].status = Order.PROCESSING
                    if order_status["status"] == "Completed":
                        order[0].status = Order.COMPLETED
                    order[0].save()

                    print(type(order_status))
                    print(order_status)
                    print(str(order_status and order_status.get("order") is not None))
                    status_code = status.HTTP_200_OK
                    return Response(response, status=status_code)
                else:
                    raise Exception("")

            else:
                raise Exception("Unauthorized")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(str(e))
            response = {
                "message": str(e),
                "success": False,
            }
            return Response(response, status=status_code)


class PlatformList(generics.ListAPIView):
    name = 'get-platform-list'
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    search_fields = ['exclude']

    def get_queryset(self):
        exclude = self.request.query_params.get('exclude', '')
        exclude_list = exclude.split(',')
        queryset = Platform.objects.all().order_by('order').exclude(name__in=exclude_list)
        return queryset
