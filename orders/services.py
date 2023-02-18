import json
import os
import sys
import time

from django.db.models import Q
import requests
from orders.models import Order
from payments.models import Payment


def requestOrderStatusApi(service, order):
    try:
        api = service.api_order_status
        print(service.platform.name + " " + service.name)
        # vendor = api.vendor
        url = api.vendor.api_base
        order_response = json.loads(order.response_raw)
        data = json.loads(api.params)

        headers = {
            'content-type': 'application/json'
        }
        data['order'] = order_response.get('order')
        payload = json.dumps(data)
        with open('/root/payload.txt', 'w') as outfile:
            outfile.write(str(payload))
        # import pdb;pdb.set_trace()
        response = requests.request("POST", url, headers=headers, data=payload)
        with open('/root/log.txt', 'w') as outfile:
            outfile.write(str(response.text))

        if response.status_code == 200:
            resp = response.json()

            resp_schema = api.resp_params
            if resp and resp.get(resp_schema) is not None:
                if resp.get(resp_schema) == 'Partial':

                    order.status = Order.PARTIAL
                    order.user_visible_status = Order.IN_PROGRESS

                elif resp.get(resp_schema) == 'Completed':
                    order.status = Order.COMPLETED
                    order.user_visible_status = Order.COMPLETED

                elif resp.get(resp_schema) == 'In progress':
                    order.status = Order.IN_PROGRESS
                    order.user_visible_status = Order.IN_PROGRESS

                elif resp.get(resp_schema) == 'Processing':
                    order.status = Order.PROCESSING
                    order.user_visible_status = Order.PROCESSING

                elif resp.get(resp_schema) == 'Canceled':
                    order.status = Order.CANCELLED
                    order.user_visible_status = Order.IN_PROGRESS

                order.save()
                return True
        return False
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(str(e))
        return False


def requestOrderCreateApi(service, meta, order):
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


def retryFailedOrderApi(service, order):
    try:
        requestOrderCreateApi(service=service, meta=json.loads(order.raw_metadata), order=order)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(str(e))
        return False


def sync_all_orders(args):
    orders = Order.objects.filter(
        Q(status=Order.PROCESSING, payment__payment_status=Payment.COMPLETED) | Q(status=Order.PENDING,
                                                                                  payment__payment_status=Payment.COMPLETED) | Q(
            status=Order.PARTIAL,
            payment__payment_status=Payment.COMPLETED))
    if len(orders) > 0:
        for order in orders:
            service = order.service
            requestOrderStatusApi(service=service, order=order)
            time.sleep(4)
    return True


def retry_all_failed_orders(args):
    orders = Order.objects.filter(
        Q(status=Order.PROCESSING, payment__payment_status=Payment.COMPLETED) | Q(status=Order.PENDING,
                                                                                  payment__payment_status=Payment.COMPLETED) | Q(
            status=Order.PARTIAL,
            payment__payment_status=Payment.COMPLETED))
    if len(orders) > 0:
        for order in orders:
            service = order.service
            if order.response_raw is not None and order.response_raw.find("error") != -1:
                retryFailedOrderApi(service=service, order=order)
                time.sleep(4)
    return True


def sync_done(task):
    with open('/root/error.txt', 'w') as outfile:
        outfile.write(str(task.result))
    print(task.result)
