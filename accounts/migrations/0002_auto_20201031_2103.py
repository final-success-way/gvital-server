# Generated by Django 2.2.16 on 2020-10-31 21:03

import bitfield.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='flags',
            field=bitfield.models.BitField(('is_user', 'is_staff'), blank=True, default=None, null=True),
        ),
    ]