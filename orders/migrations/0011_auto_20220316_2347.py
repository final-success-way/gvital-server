# Generated by Django 2.2.16 on 2022-03-16 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_auto_20220316_2322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(blank=True, default='j0PJvbUQvD', max_length=100, null=True),
        ),
    ]
