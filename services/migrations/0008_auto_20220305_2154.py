# Generated by Django 2.2.16 on 2022-03-05 21:54

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0007_service_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='content',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]