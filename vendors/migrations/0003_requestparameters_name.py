# Generated by Django 2.2.16 on 2022-03-03 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0002_auto_20201117_0628'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestparameters',
            name='name',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
