import decimal
import json
import random, string
import hashlib
import uuid
import datetime
from django.conf import settings
from django.core.mail import send_mail, get_connection
import requests
from django.contrib.auth.models import User

def update_order_status():
    return


def get_uid():
    uid_obj = uuid.uuid4()
    uid = str(uid_obj.int)
    return uid


def check_authentication(request):
    user = request.user
    access = False
    if user.is_authenticated():
        access = True

    return access


def get_order_id():
    trans_id = random.randrange(
        1000000, 9999999)
    return trans_id


def convert_utc_to_ist(utc_object):
    delay = datetime.timedelta(
        hours=5, minutes=30)
    ist_object = utc_object + delay
    return ist_object



class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            # wanted a simple yield str(o) in the next line,
            # but that would mean a yield on the line with super(...),
            # which wouldn't work (see my comment below), so...
            return (str(o) for o in [o])
        return super(DecimalEncoder, self).default(o)


def make_cache_key(key, key_prefix, version):
    return key


def requestOrderCreateApi(service, varient, meta, order):
    api = service.api_order_create

    vendor = api.vendor
    url = api.vendor.api_base
    data = {}
    print(meta)
    print(api.parameters.all())
    for t in api.parameters.all():
        print(t.parameter)
        print(t.value)
        if t.parameter_type == 'number':
            data.update({t.parameter: int(t.value)})
        else:
            data.update({t.parameter: t.value})
    data["key"] = vendor.api_key
    data.update({'link': meta['link'], 'quantity': meta['quantity']})

    print(data)
    payload = json.dumps(data)
    headers = {
        'content-type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.json())
    order.request_raw = response.json()
    order.save()
    if response.status_code == 200:
        return True
    return False


# from services.models import Service
#
# service = Service.objects.all()[0]
# meta = {'link': 'https://www.instagram.com/p/CJ5keooJINX', 'quantity': 500, 'username': 'https://www.instagram.com/p/CJ5keooJINX'}
# # requestOrderCreateApi(service=service,varient=None,meta=meta,order=None)
# with get_connection(
#             host=settings.EMAIL_HOST,
#             port=settings.EMAIL_PORT,
#             username=settings.EMAIL_HOST_USER_SUPPORT,
#             password=settings.EMAIL_HOST_PASSWORD_SUPPORT,
#             use_tls=settings.EMAIL_USE_TLS
#     ) as connection:
#         mail = send_mail("Buyrealfollows Order Issue",
#                          message="Hi amirsuliqi,\n Thanks for reaching out. We just checked your instagram account is private. We won't be able to process your order until you make your account public.\nLet us know once you make your account public and we will process your order asap. Usually it takes 2-3 days to process.\n\nThanks\nBuyrealfollows Team",
#                          recipient_list=['karnamit2105@gmail.com'],
#                          from_email='Support Buyrealfollows <%s>' % settings.EMAIL_HOST,
#                          connection=connection,
#                          fail_silently=False)
