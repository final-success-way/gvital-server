# Generated by Django 2.2.16 on 2022-03-20 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0018_auto_20220318_0010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(blank=True, default='aXr8zcd4Sp', max_length=100, null=True),
        ),
    ]
