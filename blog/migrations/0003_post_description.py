# Generated by Django 2.2.16 on 2021-12-20 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20211220_0747'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='description',
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
    ]