# Generated by Django 2.2.16 on 2022-05-21 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0006_auto_20220321_0716'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestparameters',
            name='common',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='responseparameters',
            name='common',
            field=models.BooleanField(default=False),
        ),
    ]
