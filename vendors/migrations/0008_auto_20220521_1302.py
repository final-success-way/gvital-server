# Generated by Django 2.2.16 on 2022-05-21 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0007_auto_20220521_1244'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requestparameters',
            name='common',
        ),
        migrations.RemoveField(
            model_name='responseparameters',
            name='common',
        ),
        migrations.AddField(
            model_name='vendorapi',
            name='params',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vendorapi',
            name='resp_params',
            field=models.TextField(blank=True, null=True),
        ),
    ]
