# Generated by Django 2.2.16 on 2022-03-17 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_remove_order_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_id',
            field=models.CharField(blank=True, default='7jGhigrpd1', max_length=100, null=True),
        ),
    ]
