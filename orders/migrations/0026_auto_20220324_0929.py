# Generated by Django 2.2.16 on 2022-03-24 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0025_auto_20220321_0811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(blank=True, default='2UHKlyRYIr', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='statuscheck',
            name='order_id',
            field=models.CharField(blank=True, default='2UHKlyRYIr', max_length=100, null=True),
        ),
    ]
