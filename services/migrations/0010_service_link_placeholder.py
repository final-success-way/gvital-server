# Generated by Django 2.2.16 on 2022-03-05 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0009_service_link_regex_validate'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='link_placeholder',
            field=models.TextField(blank=True),
        ),
    ]