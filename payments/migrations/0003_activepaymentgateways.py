# Generated by Django 2.2.16 on 2022-03-25 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_auto_20220303_1328'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivePaymentGateways',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=False)),
                ('url', models.CharField(max_length=100)),
                ('payment_method', models.CharField(choices=[('PAYPAL', 'PAYPAL'), ('STRIPE', 'STRIPE'), ('UNITPAY', 'UNITPAY'), ('COINBASE', 'COINBASE'), ('PAYERR', 'PAYERR'), ('PAYOP', 'PAYOP')], default='PAYPAL', max_length=100)),
            ],
        ),
    ]