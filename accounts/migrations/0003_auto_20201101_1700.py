# Generated by Django 2.2.16 on 2020-11-01 17:00

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20201031_2103'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='insta_username',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
