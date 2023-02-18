# Generated by Django 2.2.16 on 2022-03-26 16:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0015_service_api_order_refill'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='api_order_create',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='api_order_create', to='vendors.VendorApi'),
        ),
        migrations.AlterField(
            model_name='service',
            name='api_order_refill',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='api_order_refill', to='vendors.VendorApi'),
        ),
        migrations.AlterField(
            model_name='service',
            name='api_order_status',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='api_order_status', to='vendors.VendorApi'),
        ),
    ]