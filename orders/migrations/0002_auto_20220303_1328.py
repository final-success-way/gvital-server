# Generated by Django 2.2.16 on 2022-03-03 13:28

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_auto_20220303_1328'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='amount',
            field=models.CharField(default='0', max_length=10),
        ),
        migrations.AddField(
            model_name='order',
            name='meta',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='order_id',
            field=models.CharField(default=uuid.uuid4, max_length=100, unique=True),
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='payments.Payment'),
        ),
        migrations.AddField(
            model_name='order',
            name='raw_metadata',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='request_raw',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('COMPLETED', 'COMPLETED'), ('PROCESSING', 'PROCESSING'), ('FAILED', 'FAILED'), ('PENDING', 'PENDING')], default='PENDING', max_length=50),
        ),
    ]