# Generated by Django 2.2.16 on 2022-03-04 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_auto_20220303_1936'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='is_general',
            field=models.BooleanField(default=True),
        ),
    ]