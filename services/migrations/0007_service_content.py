# Generated by Django 2.2.16 on 2022-03-05 20:52

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0006_auto_20220304_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='content',
            field=ckeditor.fields.RichTextField(blank=True, max_length=5000, null=True),
        ),
    ]