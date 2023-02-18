# from django.apps import AppConfig
# from django_q.models import Schedule
# from django_q.tasks import schedule
#
#
# class MyAppConfig(AppConfig):
#     name = 'myapp'
#     verbose_name = "My Application"
#
#     def ready(self):
#         schedule("orders.services.sync_all_orders", '',
#                  hook="orders.services.sync_done",
#                  schedule_type=Schedule.HOURLY)
#         pass
