# Generated by Django 2.2.16 on 2021-12-07 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0007_auto_20211205_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='uid',
            field=models.CharField(blank=True, default='GA4BCX0ZNM', max_length=100, null=True, unique=True),
        ),
    ]
