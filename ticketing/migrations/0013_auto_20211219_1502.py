# Generated by Django 2.2.16 on 2021-12-19 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0012_auto_20211219_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='uid',
            field=models.CharField(blank=True, default='IXBXRLIJR2', max_length=100, null=True, unique=True),
        ),
    ]
