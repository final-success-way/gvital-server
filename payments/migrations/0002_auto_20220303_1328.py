# Generated by Django 2.2.16 on 2022-03-03 13:28

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('active', models.BooleanField(default=False)),
                ('gateway', models.CharField(choices=[('PAYPAL', 'PAYPAL'), ('STRIPE', 'STRIPE'), ('UNITPAY', 'UNITPAY'), ('COINBASE', 'COINBASE'), ('PAYERR', 'PAYERR'), ('PAYOP', 'PAYOP')], default='PAYPAL', max_length=100)),
                ('discount_percent', models.CharField(default='0', max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PaymentGateway',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('name', models.CharField(choices=[('PAYPAL', 'PAYPAL'), ('STRIPE', 'STRIPE'), ('UNITPAY', 'UNITPAY'), ('COINBASE', 'COINBASE'), ('PAYOP', 'PAYOP'), ('PAYERR', 'PAYERR')], default='PAYPAL', max_length=100)),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='payment',
            name='meta',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(choices=[('PAYPAL', 'PAYPAL'), ('STRIPE', 'STRIPE'), ('UNITPAY', 'UNITPAY'), ('COINBASE', 'COINBASE'), ('PAYERR', 'PAYERR'), ('PAYOP', 'PAYOP')], default='PAYPAL', max_length=100),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_status',
            field=models.CharField(choices=[('COMPLETED', 'COMPLETED'), ('PENDING', 'PENDING'), ('FAILED', 'FAILED'), ('PROCESSING', 'PROCESSING')], default='PENDING', max_length=100),
        ),
    ]